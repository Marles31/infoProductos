#!/usr/bin/env python3
"""Renderiza un infoproducto visual en HTML desde JSON marketero."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera HTML visual de infoproducto.")
    parser.add_argument("--input", required=True, help="JSON generado por build_infoproduct_marketing.py")
    parser.add_argument("--output", required=True, help="Ruta HTML de salida")
    parser.add_argument(
        "--images-dir",
        default="",
        help="Directorio opcional de imagenes (page_01.png, etc.)",
    )
    parser.add_argument(
        "--title",
        default="",
        help="Titulo opcional del documento HTML",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    return []


def as_rgb(hex_color: str) -> tuple[int, int, int]:
    c = hex_color.strip().lstrip("#")
    if len(c) != 6:
        return (16, 19, 25)
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def to_hex(rgb: tuple[int, int, int]) -> str:
    return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    tt = max(0.0, min(1.0, t))
    return (
        int(c1[0] * (1 - tt) + c2[0] * tt),
        int(c1[1] * (1 - tt) + c2[1] * tt),
        int(c1[2] * (1 - tt) + c2[2] * tt),
    )


def find_image_rel(images_dir: Path, page_number: int, output_html: Path) -> str:
    patterns = [
        f"page_{page_number:02d}.png",
        f"page_{page_number:02d}.jpg",
        f"page_{page_number:02d}.jpeg",
        f"page_{page_number:02d}.webp",
    ]
    for name in patterns:
        candidate = images_dir / name
        if candidate.exists():
            rel = candidate.relative_to(output_html.parent)
            return rel.as_posix()
    return ""


def list_to_html(items: list[str], css_class: str) -> str:
    rows = []
    for item in items:
        rows.append(f"<li>{html.escape(item)}</li>")
    return f'<ul class="{css_class}">' + "".join(rows) + "</ul>"


def icon_text(icon_hint: str) -> str:
    mapping = {
        "pulse": "IMPACTO",
        "alert": "RIESGO",
        "bag": "KIT",
        "map": "RUTA",
        "route": "RUTA",
        "shield": "MARCO",
        "drop": "BASE",
        "boots": "ACCION",
        "bolt": "OPTIMIZ",
        "chat": "Q&A",
        "target": "CTA",
        "check": "CHECK",
    }
    return mapping.get(icon_hint, "INFO")


def short_items(page: dict[str, Any], count: int, fallback_prefix: str) -> list[str]:
    pool = safe_list(page.get("bullets")) + safe_list(page.get("action_steps"))
    items: list[str] = []
    for entry in pool:
        txt = entry
        if ":" in txt:
            txt = txt.split(":", 1)[1].strip()
        txt = txt[:26].strip()
        if txt:
            items.append(txt)
        if len(items) >= count:
            break
    if not items:
        items = [f"{fallback_prefix} {i + 1}" for i in range(count)]
    if len(items) < count:
        for i in range(len(items), count):
            items.append(f"{fallback_prefix} {i + 1}")
    return items


def placeholder_by_pattern(pattern: str, page: dict[str, Any]) -> str:
    labels4 = short_items(page, 4, "Bloque")
    labels3 = short_items(page, 3, "Item")

    if pattern == "alert_grid":
        return (
            '<div class="placeholder ph-alert">'
            + "".join([f'<div class="hazard">{html.escape(x.upper())}</div>' for x in labels4])
            + "</div>"
        )
    if pattern == "checklist_cards":
        return (
            '<div class="placeholder ph-checklist">'
            + "".join([f'<div class="check">[x] {html.escape(x)}</div>' for x in labels4])
            + "</div>"
        )
    if pattern == "route_map":
        return (
            '<div class="placeholder ph-route">'
            '<div class="node n1">A</div>'
            '<div class="node n2">B</div>'
            '<div class="node n3">C</div>'
            '<div class="line l1"></div>'
            '<div class="line l2"></div>'
            f'<p>{html.escape(labels3[0])} / {html.escape(labels3[1])}</p>'
            "</div>"
        )
    if pattern == "framework_stack":
        return (
            '<div class="placeholder ph-stack">'
            + "".join([f'<div class="card">{html.escape(x)}</div>' for x in labels3])
            + "</div>"
        )
    if pattern == "energy_meter":
        return (
            '<div class="placeholder ph-energy">'
            '<div class="meter m1"><span style="width:88%"></span></div>'
            '<div class="meter m2"><span style="width:64%"></span></div>'
            '<div class="meter m3"><span style="width:42%"></span></div>'
            f'<p>{html.escape(labels3[0])}</p>'
            "</div>"
        )
    if pattern == "comparison_split":
        return (
            '<div class="placeholder ph-compare">'
            f'<div class="side left"><h5>{html.escape(labels3[0])}</h5><p>antes</p></div>'
            f'<div class="side right"><h5>{html.escape(labels3[1])}</h5><p>despues</p></div>'
            "</div>"
        )
    if pattern == "offer_stack":
        return (
            '<div class="placeholder ph-offer">'
            + "".join([f'<div class="pack">{html.escape(x)}</div>' for x in labels3])
            + '<div class="buy">Accion inmediata</div>'
            "</div>"
        )
    return (
        '<div class="placeholder ph-hero">'
        '<div class="shape shape-a"></div>'
        '<div class="shape shape-b"></div>'
        '<p>Visual en preparacion</p>'
        "</div>"
    )


def page_block(page: dict[str, Any], image_rel: str) -> str:
    bullets = page.get("bullets", [])
    action_steps = page.get("action_steps", [])
    quick_wins = page.get("quick_wins", [])
    avoid_list = page.get("avoid_list", [])
    body = page.get("body", [])
    hook = str(page.get("hook", ""))
    one_liner = str(page.get("one_liner", ""))
    pattern = str(page.get("design_pattern", "hero_split"))
    icon = icon_text(str(page.get("icon_hint", "")))
    focus = str(page.get("focus", "accion"))
    goal = str(page.get("page_goal", "avanzar"))

    body_html = "".join([f"<p>{html.escape(p)}</p>" for p in body])
    bullet_html = list_to_html([str(x) for x in bullets], "bullet-list")
    action_html = list_to_html([str(x) for x in action_steps], "action-list")
    quick_html = list_to_html([str(x) for x in quick_wins], "quick-list")
    avoid_html = list_to_html([str(x) for x in avoid_list], "avoid-list")

    if image_rel:
        visual_html = f'<img src="{html.escape(image_rel)}" alt="Visual pagina {page["page_number"]}" />'
    else:
        visual_html = placeholder_by_pattern(pattern, page)

    return f"""
    <section class="page pattern-{html.escape(pattern)} focus-{html.escape(focus)}">
      <div class="page-top">
        <span class="chip">Pagina {page["page_number"]}</span>
        <span class="chip chip-alt">{html.escape(str(page.get("section_title", "")))}</span>
        <span class="chip chip-icon">{html.escape(icon)}</span>
        <span class="chip chip-soft">{html.escape(goal)}</span>
      </div>
      <h2>{html.escape(str(page.get("headline", "")))}</h2>
      <h3>{html.escape(str(page.get("subheadline", "")))}</h3>
      <div class="grid">
        <div class="content">
          <div class="hook">{html.escape(hook)}</div>
          {body_html}
          <div class="mini-note">{html.escape(one_liner)}</div>
          <div class="insights-grid">
            <div class="insight-card">
              <h4>Ganancias Rapidas</h4>
              {quick_html}
            </div>
            <div class="insight-card insight-warn">
              <h4>Evita Esto</h4>
              {avoid_html}
            </div>
          </div>
          {bullet_html}
          <div class="action-box">
            <h5>{html.escape(str(page.get("action_title", "Accion")))}</h5>
            {action_html}
          </div>
          <div class="cta">{html.escape(str(page.get("micro_cta", "")))}</div>
        </div>
        <div class="visual">{visual_html}</div>
      </div>
    </section>
    """


def build_html(data: dict[str, Any], output_path: Path, images_dir: Path | None, doc_title: str) -> str:
    palette = data.get("brand", {}).get("palette", {})
    bg = as_rgb(str(palette.get("bg", "#101319")))
    surface = as_rgb(str(palette.get("surface", "#1C222B")))
    accent = as_rgb(str(palette.get("accent", "#E94E1B")))
    accent2 = as_rgb(str(palette.get("accent_2", "#F6C945")))
    text = as_rgb(str(palette.get("text", "#F4F6F8")))
    muted = as_rgb(str(palette.get("muted", "#B8C0CC")))

    typography = data.get("brand", {}).get("typography", {})
    if not isinstance(typography, dict):
        typography = {}
    heading_font = str(typography.get("headline", "Anton"))
    body_font = str(typography.get("body", "Manrope"))

    bg_glow_a = to_hex(mix(accent, bg, 0.72))
    bg_glow_b = to_hex(mix(accent2, bg, 0.74))
    hero_top = to_hex(mix(accent, surface, 0.42))
    hero_bottom = to_hex(mix(surface, bg, 0.28))
    panel = to_hex(mix(surface, bg, 0.45))
    panel_alt = to_hex(mix(surface, bg, 0.63))
    text_soft = to_hex(mix(text, muted, 0.55))
    border_soft = to_hex(mix(text, bg, 0.84))

    pages = data.get("pages", [])
    pages_html: list[str] = []
    for page in pages:
        image_rel = ""
        if images_dir:
            image_rel = find_image_rel(images_dir, int(page["page_number"]), output_path)
        pages_html.append(page_block(page, image_rel))

    heading = doc_title or str(data.get("offer_name", "Infoproducto Visual"))
    theme = str(data.get("theme", ""))
    page_count = len(pages_html)

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(heading)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family={html.escape(heading_font).replace(' ', '+')}&family={html.escape(body_font).replace(' ', '+')}:wght@400;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: {to_hex(bg)};
      --surface: {to_hex(surface)};
      --accent: {to_hex(accent)};
      --accent-2: {to_hex(accent2)};
      --text: {to_hex(text)};
      --muted: {to_hex(muted)};
      --panel: {panel};
      --panel-alt: {panel_alt};
      --text-soft: {text_soft};
      --border-soft: {border_soft};
      --bg-glow-a: {bg_glow_a};
      --bg-glow-b: {bg_glow_b};
      --hero-top: {hero_top};
      --hero-bottom: {hero_bottom};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: '{html.escape(body_font)}', sans-serif;
      background:
        radial-gradient(circle at 15% 0%, var(--bg-glow-a) 0%, transparent 42%),
        radial-gradient(circle at 80% 8%, var(--bg-glow-b) 0%, transparent 36%),
        var(--bg);
      color: var(--text);
      line-height: 1.45;
    }}
    .wrap {{
      max-width: 1120px;
      margin: 0 auto;
      padding: 30px 20px 56px;
    }}
    .hero {{
      background:
        linear-gradient(120deg, color-mix(in srgb, var(--accent) 45%, transparent), transparent 54%),
        linear-gradient(180deg, var(--hero-top), var(--hero-bottom));
      border: 1px solid color-mix(in srgb, var(--text) 15%, transparent);
      border-radius: 24px;
      padding: 26px;
      margin-bottom: 18px;
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      width: 260px;
      height: 260px;
      right: -88px;
      top: -96px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--accent-2) 25%, transparent);
    }}
    .hero h1 {{
      margin: 0 0 8px;
      font-family: '{html.escape(heading_font)}', sans-serif;
      font-size: clamp(34px, 7vw, 66px);
      line-height: 0.95;
      letter-spacing: 0.35px;
      font-weight: 700;
    }}
    .hero p {{
      margin: 0;
      max-width: 790px;
      color: var(--muted);
      font-size: 14px;
    }}
    .hero-meta {{
      margin-top: 12px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .meta {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.3px;
      text-transform: uppercase;
      border: 1px solid color-mix(in srgb, var(--text) 20%, transparent);
      background: color-mix(in srgb, var(--surface) 55%, transparent);
    }}
    .page {{
      background: linear-gradient(180deg, color-mix(in srgb, var(--surface) 88%, transparent), color-mix(in srgb, var(--panel) 94%, transparent));
      border: 1px solid color-mix(in srgb, var(--text) 13%, transparent);
      border-radius: 18px;
      padding: 22px;
      margin-bottom: 16px;
    }}
    .page:nth-of-type(even) .content {{ order: 2; }}
    .page:nth-of-type(even) .visual {{ order: 1; }}
    .page-top {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin-bottom: 8px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      padding: 5px 10px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--accent) 24%, transparent);
      border: 1px solid color-mix(in srgb, var(--accent) 52%, transparent);
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.2px;
    }}
    .chip-alt {{
      background: color-mix(in srgb, var(--accent-2) 25%, transparent);
      border-color: color-mix(in srgb, var(--accent-2) 55%, transparent);
    }}
    .chip-icon {{
      background: color-mix(in srgb, var(--accent-2) 18%, transparent);
      border-color: color-mix(in srgb, var(--accent-2) 42%, transparent);
    }}
    .chip-soft {{
      background: color-mix(in srgb, var(--surface) 62%, transparent);
      border-color: color-mix(in srgb, var(--text) 18%, transparent);
      color: var(--text-soft);
      text-transform: none;
      font-weight: 600;
    }}
    h2 {{
      margin: 6px 0 8px;
      font-family: '{html.escape(heading_font)}', sans-serif;
      font-size: clamp(28px, 4.8vw, 44px);
      line-height: 0.96;
      letter-spacing: 0.3px;
      font-weight: 700;
    }}
    h3 {{
      margin: 0 0 12px;
      color: var(--accent-2);
      font-size: 15px;
      font-weight: 700;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 16px;
    }}
    .hook {{
      margin: 0 0 10px;
      padding: 10px 12px;
      border-radius: 10px;
      border-left: 4px solid var(--accent);
      background: color-mix(in srgb, var(--accent) 10%, transparent);
      color: var(--text);
      font-size: 14px;
      font-weight: 700;
      line-height: 1.35;
    }}
    .content p {{
      margin: 0 0 8px;
      color: var(--text-soft);
      font-size: 14px;
    }}
    .mini-note {{
      margin-top: 8px;
      padding: 8px 10px;
      border-radius: 9px;
      font-size: 12px;
      color: var(--text);
      background: color-mix(in srgb, var(--surface) 62%, transparent);
      border: 1px solid color-mix(in srgb, var(--text) 15%, transparent);
    }}
    .insights-grid {{
      margin-top: 10px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
    }}
    .insight-card {{
      border-radius: 11px;
      padding: 10px;
      background: color-mix(in srgb, var(--surface) 68%, transparent);
      border: 1px solid color-mix(in srgb, var(--text) 16%, transparent);
    }}
    .insight-card h4 {{
      margin: 0 0 6px;
      font-size: 12px;
      letter-spacing: 0.35px;
      text-transform: uppercase;
      color: var(--accent-2);
    }}
    .insight-warn h4 {{
      color: var(--accent);
    }}
    .quick-list, .avoid-list {{
      margin: 0;
      padding-left: 16px;
      display: grid;
      gap: 5px;
    }}
    .quick-list li, .avoid-list li {{
      font-size: 12px;
      color: var(--text);
      line-height: 1.35;
    }}
    .bullet-list, .action-list {{
      margin: 10px 0 0;
      padding-left: 18px;
      display: grid;
      gap: 6px;
    }}
    .bullet-list li, .action-list li {{
      font-size: 13px;
      color: var(--text);
    }}
    .action-box {{
      margin-top: 12px;
      background: color-mix(in srgb, var(--accent) 12%, transparent);
      border: 1px dashed color-mix(in srgb, var(--accent) 60%, transparent);
      border-radius: 12px;
      padding: 12px;
    }}
    .action-box h5 {{
      margin: 0 0 8px;
      color: var(--accent);
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .cta {{
      margin-top: 12px;
      display: inline-block;
      padding: 10px 12px;
      border-radius: 10px;
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      color: color-mix(in srgb, #000 75%, transparent);
      font-weight: 800;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.35px;
    }}
    .visual {{
      min-height: 250px;
      border-radius: 14px;
      overflow: hidden;
      background: var(--panel-alt);
      border: 1px solid color-mix(in srgb, var(--text) 12%, transparent);
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .visual img {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }}
    .placeholder {{
      width: 100%;
      height: 100%;
      min-height: 250px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 14px;
      color: var(--text);
      background: linear-gradient(140deg, var(--panel), var(--panel-alt));
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.3px;
    }}
    .ph-hero .shape {{
      position: absolute;
      border-radius: 999px;
    }}
    .ph-hero .shape-a {{
      width: 130px;
      height: 130px;
      right: 22px;
      top: 18px;
      background: color-mix(in srgb, var(--accent) 48%, transparent);
    }}
    .ph-hero .shape-b {{
      width: 88px;
      height: 88px;
      right: 86px;
      top: 76px;
      background: color-mix(in srgb, var(--accent-2) 43%, transparent);
    }}
    .ph-alert {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      align-content: center;
      justify-items: stretch;
    }}
    .ph-alert .hazard {{
      border: 1px solid color-mix(in srgb, var(--text) 20%, transparent);
      background: color-mix(in srgb, var(--accent) 24%, transparent);
      border-radius: 10px;
      padding: 12px;
      text-align: center;
      font-size: 11px;
    }}
    .ph-checklist {{
      display: grid;
      gap: 8px;
      width: 100%;
      align-content: center;
    }}
    .ph-checklist .check {{
      border: 1px solid color-mix(in srgb, var(--text) 20%, transparent);
      border-radius: 9px;
      padding: 10px;
      background: color-mix(in srgb, var(--surface) 60%, transparent);
      font-size: 12px;
      text-transform: none;
    }}
    .ph-route .node {{
      position: absolute;
      width: 34px;
      height: 34px;
      border-radius: 999px;
      display: grid;
      place-items: center;
      font-size: 11px;
      font-weight: 800;
      background: color-mix(in srgb, var(--accent-2) 35%, transparent);
      border: 1px solid color-mix(in srgb, var(--accent-2) 72%, transparent);
    }}
    .ph-route .n1 {{ top: 38px; left: 30px; }}
    .ph-route .n2 {{ top: 104px; left: 110px; }}
    .ph-route .n3 {{ top: 182px; left: 66px; }}
    .ph-route .line {{
      position: absolute;
      height: 3px;
      background: color-mix(in srgb, var(--accent) 62%, var(--accent-2) 38%);
      transform-origin: left center;
      border-radius: 999px;
    }}
    .ph-route .l1 {{ width: 94px; left: 56px; top: 60px; transform: rotate(33deg); }}
    .ph-route .l2 {{ width: 78px; left: 88px; top: 136px; transform: rotate(137deg); }}
    .ph-route p {{
      position: absolute;
      left: 16px;
      bottom: 12px;
      margin: 0;
      font-size: 11px;
      text-transform: none;
      color: var(--text-soft);
    }}
    .ph-stack {{
      display: grid;
      gap: 10px;
      width: 100%;
      align-content: center;
    }}
    .ph-stack .card {{
      border-radius: 10px;
      padding: 12px;
      text-align: center;
      border: 1px solid color-mix(in srgb, var(--text) 20%, transparent);
      background: color-mix(in srgb, var(--surface) 64%, transparent);
      font-size: 12px;
      text-transform: none;
    }}
    .ph-energy {{
      display: grid;
      gap: 10px;
      width: 100%;
      align-content: center;
    }}
    .ph-energy .meter {{
      height: 12px;
      border-radius: 999px;
      background: color-mix(in srgb, var(--text) 18%, transparent);
      overflow: hidden;
    }}
    .ph-energy .meter span {{
      display: block;
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--accent-2), var(--accent));
    }}
    .ph-energy p {{
      margin: 2px 0 0;
      font-size: 11px;
      text-transform: none;
      color: var(--text-soft);
    }}
    .ph-compare {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      width: 100%;
      height: 100%;
      align-items: stretch;
    }}
    .ph-compare .side {{
      display: grid;
      place-items: center;
      align-content: center;
      text-align: center;
      padding: 12px;
    }}
    .ph-compare .left {{
      background: color-mix(in srgb, var(--accent) 20%, transparent);
      border-right: 1px solid color-mix(in srgb, var(--text) 20%, transparent);
    }}
    .ph-compare .right {{
      background: color-mix(in srgb, var(--accent-2) 24%, transparent);
    }}
    .ph-compare h5 {{
      margin: 0 0 6px;
      font-size: 14px;
      letter-spacing: 0.3px;
      text-transform: none;
    }}
    .ph-compare p {{
      margin: 0;
      font-size: 11px;
      color: var(--text-soft);
      text-transform: uppercase;
    }}
    .ph-offer {{
      display: grid;
      gap: 8px;
      width: 100%;
      align-content: center;
    }}
    .ph-offer .pack {{
      border-radius: 9px;
      padding: 10px;
      border: 1px solid color-mix(in srgb, var(--text) 18%, transparent);
      background: color-mix(in srgb, var(--surface) 58%, transparent);
      font-size: 12px;
      text-transform: none;
    }}
    .ph-offer .buy {{
      margin-top: 6px;
      border-radius: 10px;
      padding: 11px;
      text-align: center;
      background: linear-gradient(90deg, var(--accent), var(--accent-2));
      color: color-mix(in srgb, #000 75%, transparent);
      font-size: 12px;
    }}
    @media (max-width: 920px) {{
      .grid {{ grid-template-columns: 1fr; }}
      .insights-grid {{ grid-template-columns: 1fr; }}
      .page:nth-of-type(even) .content,
      .page:nth-of-type(even) .visual {{ order: initial; }}
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1>{html.escape(heading)}</h1>
      <p>{html.escape(theme)}</p>
      <div class="hero-meta">
        <span class="meta">{page_count} paginas</span>
        <span class="meta">diseno modular</span>
        <span class="meta">listo para imagenes</span>
      </div>
    </header>
    {''.join(pages_html)}
  </div>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    data = load_json(Path(args.input))
    out_path = Path(args.output)
    images_dir = Path(args.images_dir) if args.images_dir else None

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        build_html(data, out_path, images_dir, args.title),
        encoding="utf-8",
    )
    print(f"[OK] HTML visual generado: {out_path}")


if __name__ == "__main__":
    main()
