#!/usr/bin/env python3
"""Genera un infoproducto con copy de conversion (no esquema tecnico)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera copy marketero por pagina para infoproductos."
    )
    parser.add_argument("--input", required=True, help="Brief JSON de entrada.")
    parser.add_argument(
        "--output",
        default=".tmp/infoproduct/infoproduct_marketing.json",
        help="Salida JSON marketera.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def pick(items: list[str], idx: int, fallback: str) -> str:
    if not items:
        return fallback
    return items[idx % len(items)]


def page_blueprint(page_count: int) -> list[dict[str, str]]:
    if page_count == 5:
        return [
            {"title": "Impacto inicial", "focus": "urgencia"},
            {"title": "Errores que te eliminan", "focus": "dolor"},
            {"title": "Plan 72H", "focus": "accion"},
            {"title": "Checklist tactico", "focus": "ejecucion"},
            {"title": "Oferta y cierre", "focus": "conversion"},
        ]
    return [
        {"title": "Impacto inicial", "focus": "urgencia"},
        {"title": "Error 1: entrar en panico", "focus": "dolor"},
        {"title": "Error 2: improvisar sin kit", "focus": "dolor"},
        {"title": "Error 3: moverte sin ruta", "focus": "dolor"},
        {"title": "Marco de supervivencia", "focus": "estrategia"},
        {"title": "Paso 1: asegurar lo basico", "focus": "accion"},
        {"title": "Paso 2: moverte con criterio", "focus": "accion"},
        {"title": "Paso 3: sostenerte 30 dias", "focus": "accion"},
        {"title": "Objeciones y respuesta", "focus": "credibilidad"},
        {"title": "Cierre con oferta", "focus": "conversion"},
    ]


def build_marketing_pages(brief: dict[str, Any]) -> list[dict[str, Any]]:
    topic = str(brief.get("topic", "Supervivencia extrema")).strip()
    offer_name = str(brief.get("offer_name", "Manual de Supervivencia")).strip()
    cta = str(brief.get("cta", "Escribe AHORA para obtener acceso inmediato.")).strip()
    page_count = int(brief.get("page_count", 10))

    research = brief.get("research", {})
    if not isinstance(research, dict):
        research = {}

    pains = safe_list(research.get("pain_points"))
    outcomes = safe_list(research.get("desired_outcomes"))
    objections = safe_list(research.get("objections"))
    proofs = safe_list(research.get("proof_points"))

    default_pain = "La mayoria pierde el control en los primeros minutos."
    default_outcome = "Tomar decisiones frias cuando todos improvisan."
    default_objection = "No tengo experiencia ni equipo avanzado."
    default_proof = "Checklist practico con pasos accionables."

    blueprints = page_blueprint(page_count)
    pages: list[dict[str, Any]] = []

    for i, bp in enumerate(blueprints, start=1):
        pain = pick(pains, i - 1, default_pain)
        outcome = pick(outcomes, i - 1, default_outcome)
        objection = pick(objections, i - 1, default_objection)
        proof = pick(proofs, i - 1, default_proof)

        headline = f"{offer_name}: {bp['title'].upper()}"
        subheadline = f"Resultado clave: {outcome}"

        if bp["focus"] == "urgencia":
            body = [
                f"Las primeras 72 horas en un evento extremo no se ganan con fuerza, se ganan con decision. En '{topic}', el error mas caro es este: {pain}",
                f"Este manual te da estructura inmediata para responder sin congelarte. Si piensas '{objection}', esta es la prueba de que si puedes actuar: {proof}",
            ]
        elif bp["focus"] == "dolor":
            body = [
                f"La mayoria cae por errores previsibles, no por falta de valor. Aqui atacamos uno de los mas frecuentes: {pain}",
                f"Con una correccion puntual puedes pasar de reaccionar tarde a tomar control rapido. Objecion comun: {objection}. Resultado que buscamos: {outcome}",
            ]
        elif bp["focus"] == "estrategia":
            body = [
                f"Sin metodo, todo se vuelve ruido. Esta seccion te entrega el marco para priorizar decisiones cuando cada minuto cuenta.",
                f"Tomamos el problema central ({pain}) y lo convertimos en una ruta de accion concreta orientada a {outcome}.",
            ]
        elif bp["focus"] == "accion":
            body = [
                f"Aqui no hay teoria infinita: hay ejecucion. Este paso existe para resolver {pain} con instrucciones directas.",
                f"Tu objetivo en esta fase es simple: {outcome}. Si aparece la duda '{objection}', usa la regla operativa y continua.",
            ]
        elif bp["focus"] == "credibilidad":
            body = [
                f"Antes de cerrar, desactivamos las dudas que sabotean la accion. La mas comun en este punto es: {objection}",
                f"La evidencia practica que respalda este metodo: {proof}. Lo importante es que avances con criterio, no con improvisacion.",
            ]
        else:
            body = [
                f"Si llegaste hasta aqui, ya tienes la base para pasar del miedo al control. Falta una cosa: ejecutar sin postergar.",
                f"Esta oferta convierte todo lo anterior en un sistema aplicable desde hoy. Problema que resuelve: {pain}. Resultado final: {outcome}.",
            ]

        bullets = [
            f"Que evitar desde el minuto 1: {pain}",
            f"Meta practica de esta seccion: {outcome}",
            f"Respuesta directa a la duda comun: {objection}",
            f"Prueba y respaldo: {proof}",
        ]

        action_steps = [
            "Respira, evalua riesgo y define prioridad inmediata.",
            "Ejecuta una accion concreta en menos de 5 minutos.",
            "Prepara el siguiente movimiento antes de agotarte.",
        ]

        micro_cta = "Aplica esto hoy en modo simulacion y mide tu tiempo de respuesta."
        if i == len(blueprints):
            micro_cta = f"{cta} Incluye checklist, plan de ruta y protocolo de 72 horas."

        pages.append(
            {
                "page_number": i,
                "section_title": bp["title"],
                "headline": headline,
                "subheadline": subheadline,
                "body": body,
                "bullets": bullets,
                "action_title": "Accion inmediata",
                "action_steps": action_steps,
                "micro_cta": micro_cta,
                "image_prompt": (
                    f"Escena cinematografica postapocaliptica para '{bp['title']}' en el tema '{topic}', "
                    "contraste alto, composicion dinamica, tono dramatico, sin logos, sin texto largo."
                ),
            }
        )

    return pages


def main() -> None:
    args = parse_args()
    brief = read_json(Path(args.input))

    page_count = int(brief.get("page_count", 10))
    if page_count not in (5, 10):
        raise ValueError("page_count debe ser 5 o 10.")

    pages = build_marketing_pages(brief)
    result = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "theme": brief.get("topic", ""),
        "offer_name": brief.get("offer_name", ""),
        "page_count": page_count,
        "brand": {
            "palette": {
                "bg": "#101319",
                "surface": "#1C222B",
                "accent": "#E94E1B",
                "accent_2": "#F6C945",
                "text": "#F4F6F8",
                "muted": "#B8C0CC",
            }
        },
        "pages": pages,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"[OK] Infoproducto marketero generado: {out_path}")


if __name__ == "__main__":
    main()
