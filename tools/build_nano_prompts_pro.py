#!/usr/bin/env python3
"""Construye prompts de imagen pro y agnosticos para Nano Banana."""

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


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def safe_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    return {}


def infer_topic_entities(theme: str, policy: dict[str, Any]) -> list[str]:
    must_include = safe_list(policy.get("must_include_terms"))
    tl = theme.lower()
    auto_map = [
        ("zombie", "zombies clearly visible"),
        ("vampiro", "vampire-like entities if relevant"),
        ("robot", "robotic elements aligned to theme"),
        ("cocina", "food and kitchen props"),
        ("fitness", "fitness equipment and active poses"),
        ("finanzas", "financial context props, charts, or work scenes"),
    ]
    for key, phrase in auto_map:
        if key in tl and phrase not in must_include:
            must_include.append(phrase)
    return must_include


def scene_pack(pattern: str, focus: str) -> dict[str, str]:
    pattern_map: dict[str, dict[str, str]] = {
        "hero_split": {
            "subject": "main protagonist or representative avatar of the offer promise",
            "environment": "theme-relevant environment with clear narrative context",
            "action": "executing the first decisive action tied to the page goal",
            "composition": "hero composition with clear foreground-midground-background separation",
            "camera": "35mm look, medium framing, slight dynamic angle",
            "props": "3-5 props directly connected to the page topic and outcome",
        },
        "alert_grid": {
            "subject": "same protagonist facing multiple risks or blockers",
            "environment": "high-tension but readable context related to the theme",
            "action": "spotting and correcting critical mistakes",
            "composition": "modular composition with 3-4 visual zones that signal problems",
            "camera": "28mm look, medium-wide framing, clear lines and contrast",
            "props": "warning cues, decision markers, practical tools linked to the niche",
        },
        "checklist_cards": {
            "subject": "hands or character organizing key implementation elements",
            "environment": "clean workspace relevant to the topic",
            "action": "assembling a practical checklist in priority order",
            "composition": "grid-like composition with object hierarchy and clean spacing",
            "camera": "40mm look, close-medium shot with crisp detail",
            "props": "items that represent setup, execution, and validation steps",
        },
        "route_map": {
            "subject": "individual or small team planning execution path",
            "environment": "theme-based decision setting with clear options",
            "action": "choosing between primary and fallback routes",
            "composition": "directional composition with leading lines and branching paths",
            "camera": "32mm look, medium-long shot, controlled depth",
            "props": "map-like aids, markers, notes, directional cues tied to niche",
        },
        "framework_stack": {
            "subject": "expert figure presenting a structured framework",
            "environment": "briefing or planning context aligned with theme",
            "action": "stacking priorities in a sequence that feels executable",
            "composition": "layered composition with hierarchy from top priority to support items",
            "camera": "35mm look, documentary editorial style",
            "props": "boards, cards, documents, symbolic tools from the domain",
        },
        "energy_meter": {
            "subject": "operator optimizing performance and continuity",
            "environment": "controlled environment that suggests pacing and sustainment",
            "action": "managing effort, time, or resources for long-term progress",
            "composition": "balanced frame with progress indicators and rest/action contrast",
            "camera": "50mm look, medium shot, selective focus",
            "props": "tracking aids, timer elements, resources linked to continuity",
        },
        "comparison_split": {
            "subject": "same persona in two contrasting decision outcomes",
            "environment": "mirrored context where wrong vs right approach is visible",
            "action": "left side flawed approach, right side improved approach",
            "composition": "split composition with mirrored framing and clear contrast",
            "camera": "35mm look, consistent framing for both sides",
            "props": "parallel props that highlight contrast in approach quality",
        },
        "offer_stack": {
            "subject": "confident presenter showcasing offer deliverables",
            "environment": "professional and aspirational setup for conversion",
            "action": "presenting core assets and immediate next step",
            "composition": "product-forward composition with CTA-ready negative space",
            "camera": "45mm look, medium-close editorial framing",
            "props": "deliverable stack, toolkit visuals, proof artifacts",
        },
    }
    scene = pattern_map.get(pattern, pattern_map["hero_split"]).copy()
    if focus == "conversion":
        scene["lighting_hint"] = "warmer key light for trust and decisive action"
    elif focus == "dolor":
        scene["lighting_hint"] = "higher contrast to highlight friction and urgency"
    elif focus == "accion":
        scene["lighting_hint"] = "clear and functional lighting for operational readability"
    else:
        scene["lighting_hint"] = "cinematic but readable lighting with strong focal clarity"
    return scene


def mk_style_anchor(theme: str, data: dict[str, Any], policy: dict[str, Any]) -> str:
    custom = str(policy.get("style_anchor", "")).strip()
    if custom:
        return custom
    brand = safe_dict(data.get("brand"))
    style = str(brand.get("style", "editorial_modular")).strip() or "editorial_modular"
    realism = str(policy.get("realism_level", "high")).strip() or "high"
    return (
        f"Editorial campaign style '{style}' for theme '{theme}', "
        f"visual consistency across all pages, realism level {realism}, "
        "high readability, coherent lens language, and conversion-oriented storytelling."
    )


def mk_negative_constraints(policy: dict[str, Any], entities: list[str]) -> str:
    constraints = []
    if not bool(policy.get("allow_logos", False)):
        constraints.append("No logos")
    if not bool(policy.get("allow_watermarks", False)):
        constraints.append("No watermarks")
    if not bool(policy.get("allow_text_overlay", False)):
        constraints.append("No embedded text")
    if not bool(policy.get("allow_ui_elements", False)):
        constraints.append("No UI mockups")
    if not bool(policy.get("allow_distorted_anatomy", False)):
        constraints.append("No deformed hands or extra fingers")
    if not bool(policy.get("allow_gore", False)):
        constraints.append("No explicit gore")
    if not bool(policy.get("allow_nsfw", False)):
        constraints.append("No NSFW content")

    avoid_terms = safe_list(policy.get("avoid_terms"))
    if avoid_terms:
        constraints.append("Avoid: " + ", ".join(avoid_terms))

    if entities and not bool(policy.get("allow_theme_entities_removal", False)):
        constraints.append("Do not remove required theme entities")

    return "; ".join(constraints)


def mk_prompt(
    *,
    theme: str,
    page: dict[str, Any],
    style_anchor: str,
    aspect_ratio: str,
    entities: list[str],
    policy: dict[str, Any],
) -> str:
    section = str(page.get("section_title", "scene"))
    headline = str(page.get("headline", ""))
    focus = str(page.get("focus", "accion"))
    pattern = str(page.get("design_pattern", "hero_split"))
    goal = str(page.get("page_goal", "avanzar"))
    icon = str(page.get("icon_hint", "info"))
    bullets = safe_list(page.get("bullets"))
    bullet_focus = bullets[0] if bullets else "clear transformation from problem to outcome"
    visual_hint = str(page.get("image_prompt", "")).strip()

    scene = scene_pack(pattern, focus)
    palette_hint = str(policy.get("palette_hint", "balanced contrast, readable highlights, controlled shadows"))
    mood_hint = str(policy.get("mood_hint", "confident, actionable, and story-driven"))
    quality_target = str(
        policy.get(
            "quality_target",
            "Commercial editorial quality with coherent details and realistic material behavior",
        )
    )
    entities_block = ", ".join(entities) if entities else "None"
    negatives = mk_negative_constraints(policy, entities)

    return (
        f"[SERIES STYLE ANCHOR]\n{style_anchor}\n\n"
        f"[THEME]\n{theme}\n\n"
        f"[PAGE MISSION]\nSection: {section}\nHeadline cue: {headline}\nBusiness goal: {goal}\nIcon cue: {icon}\n\n"
        f"[VISUAL HINT FROM COPY]\n{visual_hint}\n\n"
        f"[REQUIRED THEME ENTITIES]\n{entities_block}\n\n"
        f"[SUBJECT]\n{scene['subject']}\n\n"
        f"[ENVIRONMENT]\n{scene['environment']}\n\n"
        f"[ACTION]\n{scene['action']}. Must communicate this message: {bullet_focus}\n\n"
        f"[COMPOSITION]\n{scene['composition']}. Horizontal frame {aspect_ratio}. Keep intentional negative space for future cover text.\n\n"
        f"[CAMERA]\n{scene['camera']}. Sharp focal subject, clean depth separation, no unwanted blur.\n\n"
        f"[LIGHTING]\n{scene['lighting_hint']}. Readable faces, readable key objects, controlled contrast.\n\n"
        f"[COLOR AND TEXTURE]\n{palette_hint}. Subtle texture, realistic materials, premium finish.\n\n"
        f"[PROPS]\n{scene['props']}.\n\n"
        f"[MOOD]\n{mood_hint}\n\n"
        f"[QUALITY TARGET]\n{quality_target}\n\n"
        f"[NEGATIVE CONSTRAINTS]\n{negatives}"
    )


def main() -> None:
    args = parse_args()
    data = load_json(Path(args.input))

    theme = str(data.get("theme", "Infoproducto digital")).strip()
    pages = data.get("pages", [])
    if not isinstance(pages, list) or not pages:
        raise ValueError("No hay paginas en el JSON de entrada.")

    policy = safe_dict(data.get("prompting"))
    entities = infer_topic_entities(theme, policy)
    style_anchor = mk_style_anchor(theme, data, policy)

    prompts = []
    for page in pages:
        n = int(page.get("page_number", len(prompts) + 1))
        prompts.append(
            {
                "page": n,
                "title": str(page.get("section_title", f"Pagina {n}")),
                "prompt": mk_prompt(
                    theme=theme,
                    page=page,
                    style_anchor=style_anchor,
                    aspect_ratio=args.aspect_ratio,
                    entities=entities,
                    policy=policy,
                ),
                "filename": f"page_{n:02d}.png",
                "aspect_ratio": args.aspect_ratio,
                "image_size": args.image_size,
                "design_pattern": str(page.get("design_pattern", "")),
                "focus": str(page.get("focus", "")),
            }
        )

    output = {
        "meta": {
            "theme": theme,
            "style_anchor": style_anchor,
            "required_theme_entities": entities,
            "policy": policy,
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
