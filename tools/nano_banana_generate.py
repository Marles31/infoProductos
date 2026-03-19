#!/usr/bin/env python3
"""Genera imagenes con Nano Banana (Gemini image models) por lote.

Uso rapido:
    python tools/nano_banana_generate.py \
      --prompts .tmp/infoproduct/nano_prompts.json \
      --output-dir .tmp/infoproduct/images
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


API_URL_TEMPLATE = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera imagenes con Nano Banana via REST.")
    parser.add_argument(
        "--prompts",
        required=True,
        help="JSON con lista de prompts (lista o {'prompts': [...]})",
    )
    parser.add_argument(
        "--output-dir",
        default=".tmp/infoproduct/images",
        help="Carpeta de salida de imagenes.",
    )
    parser.add_argument(
        "--manifest",
        default=".tmp/infoproduct/images/manifest.json",
        help="JSON de resultados de ejecucion.",
    )
    parser.add_argument(
        "--model",
        default="gemini-2.5-flash-image",
        help="Modelo Nano Banana. Ej: gemini-2.5-flash-image o gemini-3.1-flash-image-preview.",
    )
    parser.add_argument("--api-key", default="", help="API key opcional.")
    parser.add_argument(
        "--timeout-sec",
        type=int,
        default=90,
        help="Timeout HTTP por imagen.",
    )
    parser.add_argument(
        "--sleep-ms",
        type=int,
        default=0,
        help="Pausa entre requests para evitar burst.",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=0,
        help="Limite opcional de imagenes (0 = sin limite).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="No llama API; solo valida y escribe manifest.",
    )
    return parser.parse_args()


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        cleaned = line.strip()
        if not cleaned or cleaned.startswith("#") or "=" not in cleaned:
            continue
        key, value = cleaned.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def read_prompts(path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        prompts = raw
    elif isinstance(raw, dict) and isinstance(raw.get("prompts"), list):
        prompts = raw["prompts"]
    else:
        raise ValueError("El archivo de prompts debe ser lista o {'prompts': [...]} ")
    if not prompts:
        raise ValueError("No hay prompts para procesar.")
    return prompts


def sanitize_filename(filename: str, fallback: str) -> str:
    clean = "".join(ch for ch in filename if ch.isalnum() or ch in ("-", "_", "."))
    clean = clean.strip(".")
    return clean or fallback


def extension_from_mime(mime_type: str) -> str:
    ext = mimetypes.guess_extension(mime_type or "")
    return ext if ext else ".png"


def build_payload(prompt_item: dict[str, Any]) -> dict[str, Any]:
    prompt_text = str(prompt_item.get("prompt", "")).strip()
    if not prompt_text:
        raise ValueError("Cada item de prompt debe contener 'prompt'.")

    payload: dict[str, Any] = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt_text}],
            }
        ],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }

    aspect_ratio = str(prompt_item.get("aspect_ratio", "")).strip()
    image_size = str(prompt_item.get("image_size", "")).strip()
    if aspect_ratio or image_size:
        payload["generationConfig"]["imageConfig"] = {}
        if aspect_ratio:
            payload["generationConfig"]["imageConfig"]["aspectRatio"] = aspect_ratio
        if image_size:
            payload["generationConfig"]["imageConfig"]["imageSize"] = image_size

    return payload


def parse_image_from_response(data: dict[str, Any]) -> tuple[bytes | None, str, str]:
    candidates = data.get("candidates", [])
    text_chunks: list[str] = []

    for candidate in candidates:
        content = candidate.get("content", {})
        parts = content.get("parts", [])
        for part in parts:
            txt = part.get("text")
            if isinstance(txt, str) and txt.strip():
                text_chunks.append(txt.strip())

            inline = part.get("inlineData") or part.get("inline_data")
            if isinstance(inline, dict):
                b64_data = inline.get("data")
                mime_type = str(inline.get("mimeType") or inline.get("mime_type") or "image/png")
                if isinstance(b64_data, str) and b64_data:
                    return base64.b64decode(b64_data), mime_type, "\n".join(text_chunks)

    return None, "image/png", "\n".join(text_chunks)


def main() -> None:
    args = parse_args()

    prompts_path = Path(args.prompts)
    output_dir = Path(args.output_dir)
    manifest_path = Path(args.manifest)

    load_env_file(Path(".env"))
    api_key = args.api_key.strip() or os.getenv("GEMINI_API_KEY", "").strip()
    if not args.dry_run and not api_key:
        raise ValueError("Falta API key. Define GEMINI_API_KEY o usa --api-key.")

    prompts = read_prompts(prompts_path)
    if args.max_images > 0:
        prompts = prompts[: args.max_images]

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    endpoint = API_URL_TEMPLATE.format(model=args.model)
    headers = {
        "Content-Type": "application/json",
    }
    if api_key:
        headers["x-goog-api-key"] = api_key

    results: list[dict[str, Any]] = []
    for idx, item in enumerate(prompts, start=1):
        page = int(item.get("page", idx))
        fallback_filename = f"page_{page:02d}.png"
        filename = sanitize_filename(str(item.get("filename", fallback_filename)), fallback_filename)
        payload = build_payload(item)

        if args.dry_run:
            results.append(
                {
                    "page": page,
                    "filename": filename,
                    "status": "DRY_RUN",
                    "model": args.model,
                    "endpoint": endpoint,
                }
            )
            continue

        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=args.timeout_sec,
            )
            if response.status_code >= 400:
                results.append(
                    {
                        "page": page,
                        "filename": filename,
                        "status": "ERROR_HTTP",
                        "status_code": response.status_code,
                        "response_text": response.text[:600],
                    }
                )
                continue

            data = response.json()
            image_bytes, mime_type, model_text = parse_image_from_response(data)
            if image_bytes is None:
                results.append(
                    {
                        "page": page,
                        "filename": filename,
                        "status": "ERROR_NO_IMAGE",
                        "model_text": model_text[:500],
                    }
                )
                continue

            ext = extension_from_mime(mime_type)
            output_path = output_dir / filename
            if output_path.suffix.lower() != ext.lower():
                output_path = output_path.with_suffix(ext)

            output_path.write_bytes(image_bytes)
            results.append(
                {
                    "page": page,
                    "filename": output_path.name,
                    "status": "OK",
                    "mime_type": mime_type,
                    "model_text": model_text[:500],
                    "size_bytes": len(image_bytes),
                }
            )
        except requests.RequestException as exc:
            results.append(
                {
                    "page": page,
                    "filename": filename,
                    "status": "ERROR_REQUEST",
                    "error": str(exc),
                }
            )

        if args.sleep_ms > 0:
            time.sleep(args.sleep_ms / 1000.0)

    ok_count = sum(1 for r in results if r["status"] == "OK")
    dry_run_count = sum(1 for r in results if r["status"] == "DRY_RUN")
    failed_count = len(results) - ok_count - dry_run_count
    manifest = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "total": len(results),
        "ok": ok_count,
        "dry_run_count": dry_run_count,
        "failed": failed_count,
        "dry_run": args.dry_run,
        "results": results,
    }

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )
    print(f"[OK] Manifest: {manifest_path}")
    if args.dry_run:
        print(f"[OK] Dry-run validado: {dry_run_count}/{len(results)} prompts")
    else:
        print(f"[OK] Imagenes generadas: {ok_count}/{len(results)}")


if __name__ == "__main__":
    main()
