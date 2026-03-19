#!/usr/bin/env python3
"""Construye un infoproducto (5 o 10 paginas) y sus prompts de imagen.

Uso rapido:
    python tools/build_infoproduct.py \
      --input tools/examples/infoproduct_brief.sample.json \
      --out-json .tmp/infoproduct/infoproduct.json \
      --out-md .tmp/infoproduct/infoproduct.md \
      --prompts-json .tmp/infoproduct/nano_prompts.json
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera estructura, copy base y prompts para infoproducto."
    )
    parser.add_argument("--input", required=True, help="JSON del brief.")
    parser.add_argument(
        "--out-json",
        default=".tmp/infoproduct/infoproduct.json",
        help="Salida JSON con paginas y metadatos.",
    )
    parser.add_argument(
        "--out-md",
        default=".tmp/infoproduct/infoproduct.md",
        help="Salida Markdown para lectura humana.",
    )
    parser.add_argument(
        "--prompts-json",
        default=".tmp/infoproduct/nano_prompts.json",
        help="Salida JSON de prompts listos para Nano Banana.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def safe_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(v).strip() for v in value if str(v).strip()]


def pick(items: list[str], idx: int, fallback: str) -> str:
    if not items:
        return fallback
    return items[idx % len(items)]


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "infoproduct"


def validate_brief(brief: dict[str, Any]) -> None:
    required = ["topic", "audience", "page_count"]
    for key in required:
        if key not in brief:
            raise ValueError(f"Falta campo requerido: '{key}'.")
    if brief["page_count"] not in (5, 10):
        raise ValueError("'page_count' debe ser 5 o 10.")


def build_page_blocks(brief: dict[str, Any]) -> list[dict[str, Any]]:
    topic = str(brief["topic"]).strip()
    audience = str(brief["audience"]).strip()
    page_count = int(brief["page_count"])
    offer_name = str(brief.get("offer_name", f"Guia de {topic}")).strip()
    goal = str(brief.get("goal", "vender")).strip()
    cta = str(brief.get("cta", "Escribe AHORA para obtener la guia completa.")).strip()

    research = brief.get("research", {})
    if not isinstance(research, dict):
        research = {}

    pains = safe_list(research.get("pain_points", []))
    outcomes = safe_list(research.get("desired_outcomes", []))
    objections = safe_list(research.get("objections", []))
    proofs = safe_list(research.get("proof_points", []))

    default_pain = f"La audiencia de {topic} se siente estancada por falta de metodo claro."
    default_outcome = f"Conseguir resultados medibles en {topic} en menos tiempo."
    default_objection = "No tengo tiempo para aplicar algo complejo."
    default_proof = "Metodo aplicado en casos reales con progreso visible."

    if page_count == 5:
        titles = [
            "Promesa central y resultado tangible",
            "Diagnostico del problema real",
            "Metodo simple en 3 pasos",
            "Plan accionable de 7 dias",
            "Cierre y llamada a la accion",
        ]
    else:
        titles = [
            "Promesa central y contexto",
            "Error #1 que bloquea resultados",
            "Error #2 que hace perder tiempo",
            "Error #3 que quema energia",
            "Marco estrategico de solucion",
            "Paso 1: base minima",
            "Paso 2: ejecucion guiada",
            "Paso 3: optimizacion y continuidad",
            "Objeciones y respuestas directas",
            "Oferta final y llamado a accion",
        ]

    pages: list[dict[str, Any]] = []
    for i, title in enumerate(titles, start=1):
        pain = pick(pains, i - 1, default_pain)
        outcome = pick(outcomes, i - 1, default_outcome)
        objection = pick(objections, i - 1, default_objection)
        proof = pick(proofs, i - 1, default_proof)

        hook = f"{offer_name}: {outcome}"
        body = (
            f"Esta pagina explica a {audience} como avanzar en '{topic}' sin "
            f"complicarse. Se aborda el dolor principal: {pain}. "
            f"Tambien se responde la objecion clave: {objection}. "
            f"Prueba de respaldo: {proof}. "
            f"Objetivo comercial: {goal}."
        )

        bullets = [
            f"Dolor real: {pain}",
            f"Resultado deseado: {outcome}",
            f"Respuesta a objecion: {objection}",
            f"Soporte/credibilidad: {proof}",
        ]

        image_brief = (
            f"Representar '{title}' para audiencia '{audience}' en el tema '{topic}', "
            "con estilo editorial limpio, composicion clara y foco en conversion."
        )

        pages.append(
            {
                "page_number": i,
                "title": title,
                "hook": hook,
                "body_copy": body,
                "bullets": bullets,
                "image_brief": image_brief,
            }
        )

    if pages:
        pages[-1]["body_copy"] += f" CTA final: {cta}"
        pages[-1]["bullets"].append(f"CTA: {cta}")

    return pages


def build_nano_prompts(
    pages: list[dict[str, Any]], brief: dict[str, Any]
) -> list[dict[str, Any]]:
    topic = str(brief["topic"]).strip()
    style = str(
        brief.get(
            "visual_style",
            "editorial minimalista, iluminacion suave, composicion limpia, alta legibilidad",
        )
    ).strip()
    aspect_ratio = str(brief.get("aspect_ratio", "3:2")).strip()
    image_size = str(brief.get("image_size", "1K")).strip()

    prompts: list[dict[str, Any]] = []
    for page in pages:
        page_no = page["page_number"]
        prompt = (
            f"Crear imagen para infoproducto de '{topic}'. "
            f"Pagina {page_no}: {page['title']}. "
            f"Concepto: {page['image_brief']} "
            f"Estilo visual: {style}. "
            "Incluir solo texto corto si es necesario, no logos, no marcas de agua."
        )
        prompts.append(
            {
                "page": page_no,
                "title": page["title"],
                "prompt": prompt,
                "filename": f"page_{page_no:02d}.png",
                "aspect_ratio": aspect_ratio,
                "image_size": image_size,
            }
        )
    return prompts


def to_markdown(brief: dict[str, Any], pages: list[dict[str, Any]]) -> str:
    topic = str(brief["topic"])
    audience = str(brief["audience"])
    page_count = int(brief["page_count"])

    lines: list[str] = []
    lines.append(f"# Infoproducto: {topic}")
    lines.append("")
    lines.append(f"- Audiencia: **{audience}**")
    lines.append(f"- Paginas: **{page_count}**")
    lines.append("")
    for page in pages:
        lines.append(f"## Pagina {page['page_number']}: {page['title']}")
        lines.append("")
        lines.append(f"**Hook:** {page['hook']}")
        lines.append("")
        lines.append(page["body_copy"])
        lines.append("")
        lines.append("Puntos clave:")
        for bullet in page["bullets"]:
            lines.append(f"- {bullet}")
        lines.append("")
        lines.append(f"Direccion visual: {page['image_brief']}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_prompts = Path(args.prompts_json)

    brief = read_json(input_path)
    validate_brief(brief)

    pages = build_page_blocks(brief)
    nano_prompts = build_nano_prompts(pages, brief)

    product_id = slugify(str(brief["topic"]))
    result = {
        "product_id": product_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "topic": brief["topic"],
        "audience": brief["audience"],
        "page_count": brief["page_count"],
        "offer_name": brief.get("offer_name", f"Guia de {brief['topic']}"),
        "pages": pages,
    }

    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_prompts.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
    out_md.write_text(to_markdown(brief, pages), encoding="utf-8")
    out_prompts.write_text(
        json.dumps({"prompts": nano_prompts}, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )

    print(f"[OK] Infoproducto JSON: {out_json}")
    print(f"[OK] Infoproducto Markdown: {out_md}")
    print(f"[OK] Prompts Nano Banana: {out_prompts}")


if __name__ == "__main__":
    main()
