#!/usr/bin/env python3
"""Genera un infoproducto marketero agnostico, claro y parametrizable."""

from __future__ import annotations

import argparse
import colorsys
import hashlib
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


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))


def hsl_to_hex(h: float, s: float, l: float) -> str:
    hh = (h % 360.0) / 360.0
    r, g, b = colorsys.hls_to_rgb(hh, clamp01(l), clamp01(s))
    return f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"


def infer_palette(topic: str, brand: dict[str, Any]) -> dict[str, str]:
    explicit = brand.get("palette")
    if isinstance(explicit, dict) and all(
        k in explicit for k in ("bg", "surface", "accent", "accent_2", "text", "muted")
    ):
        return {
            "bg": str(explicit["bg"]),
            "surface": str(explicit["surface"]),
            "accent": str(explicit["accent"]),
            "accent_2": str(explicit["accent_2"]),
            "text": str(explicit["text"]),
            "muted": str(explicit["muted"]),
        }

    topic_l = topic.lower()
    presets: list[tuple[list[str], dict[str, str]]] = [
        (
            ["zombie", "horror", "terror", "suspenso", "apocalipsis"],
            {"bg": "#12131B", "surface": "#1D2330", "accent": "#D85A36", "accent_2": "#9DC7FF", "text": "#F2F5F9", "muted": "#BCC6D3"},
        ),
        (
            ["finanzas", "dinero", "inversion", "negocio", "ventas", "marketing"],
            {"bg": "#101826", "surface": "#1A2538", "accent": "#2DBA8B", "accent_2": "#F2C14E", "text": "#F4F7FA", "muted": "#B9C5D3"},
        ),
        (
            ["salud", "fitness", "bienestar", "nutricion"],
            {"bg": "#0F1C1C", "surface": "#1A2B2A", "accent": "#27AE7E", "accent_2": "#7ED6C5", "text": "#F3F9F8", "muted": "#B8CCC9"},
        ),
        (
            ["belleza", "moda", "estilo", "makeup"],
            {"bg": "#1B141C", "surface": "#2A1E2B", "accent": "#E06BA8", "accent_2": "#F5C1D9", "text": "#FAF4F7", "muted": "#D8C4CF"},
        ),
        (
            ["tecnologia", "ia", "ai", "software", "programacion"],
            {"bg": "#0D1523", "surface": "#17243A", "accent": "#3FA9F5", "accent_2": "#7CDAFF", "text": "#EFF5FC", "muted": "#B5C5D7"},
        ),
    ]
    for keywords, palette in presets:
        if any(k in topic_l for k in keywords):
            return palette

    seed = int(hashlib.sha256(topic.encode("utf-8")).hexdigest()[:8], 16)
    hue = seed % 360
    mode = str(brand.get("mode", "dark")).lower()
    if mode == "light":
        return {
            "bg": hsl_to_hex(hue, 0.22, 0.96),
            "surface": hsl_to_hex(hue, 0.28, 0.99),
            "accent": hsl_to_hex(hue, 0.64, 0.49),
            "accent_2": hsl_to_hex(hue + 36, 0.66, 0.52),
            "text": hsl_to_hex(hue, 0.18, 0.14),
            "muted": hsl_to_hex(hue, 0.14, 0.36),
        }
    return {
        "bg": hsl_to_hex(hue, 0.24, 0.09),
        "surface": hsl_to_hex(hue, 0.24, 0.15),
        "accent": hsl_to_hex(hue, 0.64, 0.54),
        "accent_2": hsl_to_hex(hue + 40, 0.68, 0.58),
        "text": "#F4F6F8",
        "muted": hsl_to_hex(hue, 0.14, 0.74),
    }


def fallback_blueprint(page_count: int) -> list[dict[str, str]]:
    if page_count == 5:
        return [
            {"title": "Impacto inicial", "focus": "urgencia", "pattern": "hero_split", "icon": "pulse", "goal": "capturar atencion"},
            {"title": "Error principal", "focus": "dolor", "pattern": "alert_grid", "icon": "alert", "goal": "romper el bloqueo clave"},
            {"title": "Marco de solucion", "focus": "estrategia", "pattern": "framework_stack", "icon": "shield", "goal": "dar estructura accionable"},
            {"title": "Implementacion guiada", "focus": "accion", "pattern": "checklist_cards", "icon": "check", "goal": "acelerar ejecucion"},
            {"title": "Oferta y CTA", "focus": "conversion", "pattern": "offer_stack", "icon": "target", "goal": "convertir en lead o compra"},
        ]
    return [
        {"title": "Impacto inicial", "focus": "urgencia", "pattern": "hero_split", "icon": "pulse", "goal": "capturar atencion"},
        {"title": "Error #1", "focus": "dolor", "pattern": "alert_grid", "icon": "alert", "goal": "eliminar el primer bloqueo"},
        {"title": "Error #2", "focus": "dolor", "pattern": "checklist_cards", "icon": "check", "goal": "evitar desgaste innecesario"},
        {"title": "Error #3", "focus": "dolor", "pattern": "route_map", "icon": "map", "goal": "reducir decisiones ciegas"},
        {"title": "Marco de solucion", "focus": "estrategia", "pattern": "framework_stack", "icon": "shield", "goal": "ordenar prioridades"},
        {"title": "Paso 1", "focus": "accion", "pattern": "checklist_cards", "icon": "check", "goal": "activar la base minima"},
        {"title": "Paso 2", "focus": "accion", "pattern": "route_map", "icon": "route", "goal": "ejecutar con criterio"},
        {"title": "Paso 3", "focus": "accion", "pattern": "energy_meter", "icon": "bolt", "goal": "optimizar continuidad"},
        {"title": "Objeciones y respuestas", "focus": "credibilidad", "pattern": "comparison_split", "icon": "chat", "goal": "desactivar dudas"},
        {"title": "Oferta final y CTA", "focus": "conversion", "pattern": "offer_stack", "icon": "target", "goal": "cerrar conversion"},
    ]


def resolve_blueprint(brief: dict[str, Any], page_count: int) -> list[dict[str, str]]:
    custom = brief.get("page_blueprint")
    if not isinstance(custom, list):
        return fallback_blueprint(page_count)

    normalized: list[dict[str, str]] = []
    for idx, item in enumerate(custom, start=1):
        if not isinstance(item, dict):
            continue
        normalized.append(
            {
                "title": str(item.get("title", f"Pagina {idx}")).strip(),
                "focus": str(item.get("focus", "accion")).strip() or "accion",
                "pattern": str(item.get("pattern", "hero_split")).strip() or "hero_split",
                "icon": str(item.get("icon", "info")).strip() or "info",
                "goal": str(item.get("goal", "avanzar")).strip() or "avanzar",
            }
        )
    if len(normalized) < page_count:
        normalized.extend(fallback_blueprint(page_count)[len(normalized):page_count])
    return normalized[:page_count]


def action_steps_for_focus(focus: str) -> list[str]:
    if focus == "urgencia":
        return [
            "Elige una prioridad para los proximos 10 minutos.",
            "Haz una sola accion importante sin distraerte.",
            "Anota el resultado para repetirlo manana.",
        ]
    if focus == "dolor":
        return [
            "Detecta el error que mas te esta frenando.",
            "Corrigelo con un cambio pequeno y claro.",
            "Repite el cambio hasta que salga natural.",
        ]
    if focus == "estrategia":
        return [
            "Ordena el plan de mayor a menor impacto.",
            "Define quien hace cada parte.",
            "Revisa y mejora al final del dia.",
        ]
    if focus == "accion":
        return [
            "Haz este paso con un temporizador corto.",
            "Valida con checklist, no por intuicion.",
            "Pasa al siguiente paso sin pausar de mas.",
        ]
    if focus == "credibilidad":
        return [
            "Elige la duda mas comun de tu audiencia.",
            "Responde con ejemplo real o mini prueba.",
            "Convierte esa duda en una tarea concreta.",
        ]
    return [
        "Resume el valor principal en una frase.",
        "Muestra el beneficio mas fuerte de la oferta.",
        "Cierra con un CTA unico y directo.",
    ]


def hook_for_focus(focus: str, topic: str, pain: str, objection: str, proof: str) -> str:
    if focus == "urgencia":
        return f"Si esto empieza hoy en '{topic}', evita este error: {pain}."
    if focus == "dolor":
        return f"Este error te cuesta progreso: {pain}."
    if focus == "estrategia":
        return "Sin metodo hay caos. Con metodo hay avance."
    if focus == "accion":
        return "Menos teoria, mas accion: haz esto hoy."
    if focus == "credibilidad":
        return f"Duda real: {objection}. Respuesta practica: {proof}."
    return "Ya tienes el mapa. Solo falta ejecutar."


def body_for_focus(
    *,
    focus: str,
    topic: str,
    pain: str,
    outcome: str,
    objection: str,
    proof: str,
    goal: str,
    index: int,
) -> list[str]:
    openers = [
        "No necesitas mas complicacion; necesitas claridad.",
        "El progreso llega cuando el proceso es simple.",
        "Si entiendes que hacer, avanzas mas rapido.",
        "Un paso claro gana a diez ideas sueltas.",
    ]
    opener = pick(openers, index, openers[0])

    if focus == "urgencia":
        return [
            f"{opener} En '{topic}', el bloqueo mas comun es: {pain}.",
            f"Meta de esta pagina: {goal}. Resultado buscado: {outcome}.",
            f"Si dudas por '{objection}', usa esta prueba: {proof}.",
        ]
    if focus == "dolor":
        return [
            f"Problema real: {pain}.",
            f"Correccion propuesta: cambio simple para acercarte a {outcome}.",
            f"Cuando aparezca '{objection}', apoya tu decision con: {proof}.",
        ]
    if focus == "estrategia":
        return [
            f"Plan simple: primero {goal}, luego ejecucion paso a paso.",
            f"Este marco te ayuda a pasar de confusion a {outcome}.",
            f"Respaldo practico: {proof}.",
        ]
    if focus == "accion":
        return [
            f"Esta pagina es para hacer, no para acumular teoria.",
            f"Punto a resolver: {pain}.",
            f"Si aplicas este paso, te acercas a: {outcome}.",
        ]
    if focus == "credibilidad":
        return [
            f"Objecion principal: {objection}.",
            f"Respuesta directa: {proof}.",
            f"Objetivo de esta pagina: {goal} y mantener avance hacia {outcome}.",
        ]
    return [
        f"Ultimo freno: {pain}.",
        f"La oferta convierte aprendizaje en aplicacion para lograr {outcome}.",
        "Cierra con una accion hoy, no con una idea para despues.",
    ]


def build_marketing_pages(brief: dict[str, Any]) -> list[dict[str, Any]]:
    topic = str(brief.get("topic", "Infoproducto digital")).strip()
    cta = str(brief.get("cta", "Escribe AHORA y recibe acceso inmediato.")).strip()
    page_count = int(brief.get("page_count", 10))

    research = brief.get("research", {})
    if not isinstance(research, dict):
        research = {}

    pains = safe_list(research.get("pain_points"))
    outcomes = safe_list(research.get("desired_outcomes"))
    objections = safe_list(research.get("objections"))
    proofs = safe_list(research.get("proof_points"))
    hooks = safe_list(brief.get("headline_hooks"))

    default_pain = "No tener un paso claro para empezar."
    default_outcome = "Avanzar mas rapido con menos dudas."
    default_objection = "No tengo tiempo o experiencia."
    default_proof = "Checklist simple y aplicable."
    default_hooks = ["Guia Rapida", "Sistema Practico", "Ruta Clara", "Metodo Paso a Paso"]

    blueprints = resolve_blueprint(brief, page_count)
    pages: list[dict[str, Any]] = []

    for i, bp in enumerate(blueprints, start=1):
        pain = pick(pains, i - 1, default_pain)
        outcome = pick(outcomes, i - 1, default_outcome)
        objection = pick(objections, i - 1, default_objection)
        proof = pick(proofs, i - 1, default_proof)
        hook_prefix = pick(hooks or default_hooks, i - 1, default_hooks[0])

        headline = f"{hook_prefix}: {bp['title']}"
        subheadline = f"{bp['goal'].capitalize()} para llegar a {outcome}."
        hook = hook_for_focus(bp["focus"], topic, pain, objection, proof)
        one_liner = f"Resumen rapido: {bp['goal']} con pasos faciles de ejecutar."

        body = body_for_focus(
            focus=bp["focus"],
            topic=topic,
            pain=pain,
            outcome=outcome,
            objection=objection,
            proof=proof,
            goal=bp["goal"],
            index=i - 1,
        )

        bullets = [
            f"Bloqueo principal: {pain}",
            f"Objetivo de pagina: {bp['goal']}",
            f"Resultado esperado: {outcome}",
            f"Objecion cubierta: {objection}",
            f"Soporte: {proof}",
        ]

        quick_wins = [
            f"Empieza por: {bp['goal']}",
            f"Usa esta prueba: {proof}",
            "Mide el cambio en menos de 10 minutos",
        ]
        avoid_list = [
            pain,
            f"Detenerte por pensar: {objection}",
            "Querer hacerlo todo al mismo tiempo",
        ]

        action_steps = action_steps_for_focus(bp["focus"])
        micro_cta = str(brief.get("micro_cta_default", "Aplica este bloque hoy y mide el cambio."))
        if i == len(blueprints):
            suffix = str(brief.get("final_cta_suffix", "Incluye recursos descargables y plan de accion."))
            micro_cta = f"{cta} {suffix}".strip()

        pages.append(
            {
                "page_number": i,
                "section_title": bp["title"],
                "headline": headline,
                "subheadline": subheadline,
                "hook": hook,
                "one_liner": one_liner,
                "body": body,
                "bullets": bullets,
                "quick_wins": quick_wins,
                "avoid_list": avoid_list,
                "action_title": "Accion inmediata",
                "action_steps": action_steps,
                "micro_cta": micro_cta,
                "design_pattern": bp["pattern"],
                "icon_hint": bp["icon"],
                "focus": bp["focus"],
                "page_goal": bp["goal"],
                "image_prompt": (
                    f"Key visual para '{bp['title']}' en el tema '{topic}'. "
                    f"Diseno editorial limpio con patron {bp['pattern']} y jerarquia visual clara."
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

    brand = brief.get("brand", {})
    if not isinstance(brand, dict):
        brand = {}

    pages = build_marketing_pages(brief)
    result = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "theme": brief.get("topic", ""),
        "offer_name": brief.get("offer_name", ""),
        "page_count": page_count,
        "brand": {
            "style": str(brand.get("style", "editorial_modular")),
            "mode": str(brand.get("mode", "dark")),
            "palette": infer_palette(str(brief.get("topic", "")), brand),
            "typography": {
                "headline": str(brand.get("typography", {}).get("headline", "Anton")) if isinstance(brand.get("typography"), dict) else "Anton",
                "body": str(brand.get("typography", {}).get("body", "Manrope")) if isinstance(brand.get("typography"), dict) else "Manrope",
            },
        },
        "prompting": brief.get("prompting", {}) if isinstance(brief.get("prompting"), dict) else {},
        "pages": pages,
    }

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, ensure_ascii=True, indent=2), encoding="utf-8")
    print(f"[OK] Infoproducto marketero generado: {out_path}")


if __name__ == "__main__":
    main()
