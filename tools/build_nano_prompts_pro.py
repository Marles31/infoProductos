#!/usr/bin/env python3
"""Construye prompts de imagen pro para Nano Banana desde el JSON marketero."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera prompts avanzados y consistentes.")
    parser.add_argument("--input", required=True, help="JSON marketero de entrada")
    parser.add_argument("--output", required=True, help="JSON de prompts de salida")
    parser.add_argument("--aspect-ratio", default="3:2", help="Aspect ratio objetivo")
    parser.add_argument("--image-size", default="1K", help="Tamano imagen")
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def mk_prompt(theme: str, page: dict[str, Any], style_anchor: str, aspect_ratio: str) -> str:
    section = str(page.get("section_title", "scene"))
    headline = str(page.get("headline", ""))
    bullets = page.get("bullets", [])
    bullet_focus = bullets[0] if isinstance(bullets, list) and bullets else ""

    return (
        f"[SERIES STYLE ANCHOR] {style_anchor}\n"
        f"[THEME] {theme}\n"
        f"[PAGE CONCEPT] {section} | {headline}\n"
        f"[SUBJECT] Human survival scene with clear emotional tension, grounded realism, purposeful action.\n"
        f"[SCENE ACTION] Represent this focus point: {bullet_focus}\n"
        f"[COMPOSITION] Wide horizontal frame {aspect_ratio}, strong foreground-midground-background layering, leading lines toward the main subject, negative space reserved for future text overlay.\n"
        f"[CAMERA] 35mm lens look, slight low-angle perspective, medium depth of field, crisp focal subject.\n"
        f"[LIGHTING] Dramatic but readable: warm rim light + cool ambient fill, volumetric dust in air, controlled highlights.\n"
        f"[COLOR PALETTE] Charcoal black, steel blue, amber warning lights, muted skin tones; high contrast but natural skin rendering.\n"
        f"[TEXTURE & MOOD] Gritty cinematic realism, subtle film grain, post-crisis atmosphere, urgency without gore.\n"
        f"[QUALITY] Premium editorial campaign quality, highly detailed environment props, realistic materials.\n"
        f"[RESTRICTIONS] No logos, no watermark, no UI mockups, no long text, no extra typography, no cartoon style, no deformed anatomy."
    )


def main() -> None:
    args = parse_args()
    data = load_json(Path(args.input))

    theme = str(data.get("theme", "Survival guide"))
    pages = data.get("pages", [])
    if not isinstance(pages, list) or not pages:
        raise ValueError("No hay paginas en el JSON de entrada.")

    style_anchor = (
        "Cinematic post-crisis editorial campaign, realistic photography style, "
        "high detail props, consistent visual identity across all pages."
    )

    prompts = []
    for page in pages:
        n = int(page.get("page_number", len(prompts) + 1))
        prompts.append(
            {
                "page": n,
                "title": str(page.get("section_title", f"Pagina {n}")),
                "prompt": mk_prompt(theme, page, style_anchor, args.aspect_ratio),
                "filename": f"page_{n:02d}.png",
                "aspect_ratio": args.aspect_ratio,
                "image_size": args.image_size,
            }
        )

    output = {
        "meta": {
            "theme": theme,
            "style_anchor": style_anchor,
            "count": len(prompts),
        },
        "prompts": prompts,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"[OK] Prompts pro generados: {out}")


if __name__ == "__main__":
    main()
