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


def page_block(page: dict[str, Any], image_rel: str) -> str:
    bullets = page.get("bullets", [])
    action_steps = page.get("action_steps", [])
    body = page.get("body", [])

    body_html = "".join([f"<p>{html.escape(p)}</p>" for p in body])
    bullet_html = list_to_html([str(x) for x in bullets], "bullet-list")
    action_html = list_to_html([str(x) for x in action_steps], "action-list")

    visual_html = ""
    if image_rel:
        visual_html = f'<img src="{html.escape(image_rel)}" alt="Visual pagina {page["page_number"]}" />'
    else:
        visual_html = (
            '<div class="placeholder">'
            '<div class="shape shape-a"></div>'
            '<div class="shape shape-b"></div>'
            '<p>Visual en preparacion</p>'
            "</div>"
        )

    section = str(page.get("section_title", "")).lower()
    icon_label = "shield"
    if "error" in section:
        icon_label = "alert"
    elif "paso" in section:
        icon_label = "route"
    elif "objec" in section:
        icon_label = "chat"
    elif "cierre" in section:
        icon_label = "target"
    elif "impacto" in section:
        icon_label = "pulse"

    return f"""
    <section class="page">
      <div class="page-top">
        <span class="chip">Pagina {page["page_number"]}</span>
        <span class="chip chip-alt">{html.escape(str(page.get("section_title", "")))}</span>
        <span class="chip chip-icon">icon:{icon_label}</span>
      </div>
      <h2>{html.escape(str(page.get("headline", "")))}</h2>
      <h3>{html.escape(str(page.get("subheadline", "")))}</h3>
      <div class="grid">
        <div class="content">
          {body_html}
          {bullet_html}
          <div class="action-box">
            <h4>{html.escape(str(page.get("action_title", "Accion")))}</h4>
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
    bg = palette.get("bg", "#101319")
    surface = palette.get("surface", "#1C222B")
    accent = palette.get("accent", "#E94E1B")
    accent2 = palette.get("accent_2", "#F6C945")
    text = palette.get("text", "#F4F6F8")
    muted = palette.get("muted", "#B8C0CC")

    pages_html: list[str] = []
    for page in data.get("pages", []):
        image_rel = ""
        if images_dir:
            image_rel = find_image_rel(images_dir, int(page["page_number"]), output_path)
        pages_html.append(page_block(page, image_rel))

    heading = doc_title or str(data.get("offer_name", "Infoproducto Visual"))
    theme = str(data.get("theme", ""))

    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(heading)}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: {bg};
      --surface: {surface};
      --accent: {accent};
      --accent-2: {accent2};
      --text: {text};
      --muted: {muted};
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: 'Sora', sans-serif;
      background: radial-gradient(circle at 20% 0%, #1b222e 0%, var(--bg) 52%);
      color: var(--text);
      line-height: 1.45;
    }}
    .wrap {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }}
    .hero {{
      background:
        linear-gradient(110deg, rgba(233,78,27,0.25), transparent 52%),
        linear-gradient(180deg, #202938, var(--surface));
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 22px;
      padding: 28px;
      margin-bottom: 28px;
      position: relative;
      overflow: hidden;
    }}
    .hero::after {{
      content: "";
      position: absolute;
      width: 240px;
      height: 240px;
      right: -80px;
      top: -80px;
      border-radius: 999px;
      background: rgba(246,201,69,0.15);
    }}
    .hero h1 {{
      margin: 0 0 10px;
      font-family: 'Bebas Neue', sans-serif;
      font-size: clamp(40px, 8vw, 76px);
      line-height: 0.95;
      letter-spacing: 1px;
    }}
    .hero p {{
      margin: 0;
      max-width: 760px;
      color: var(--muted);
      font-size: 15px;
    }}
    .page {{
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 18px;
      padding: 22px;
      margin-bottom: 18px;
    }}
    .page-top {{
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 8px;
    }}
    .chip {{
      display: inline-flex;
      align-items: center;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(233,78,27,0.2);
      border: 1px solid rgba(233,78,27,0.45);
      font-size: 12px;
      font-weight: 600;
    }}
    .chip-alt {{
      background: rgba(246,201,69,0.2);
      border-color: rgba(246,201,69,0.45);
    }}
    .chip-icon {{
      background: rgba(148, 196, 255, 0.18);
      border-color: rgba(148, 196, 255, 0.45);
    }}
    h2 {{
      margin: 6px 0 8px;
      font-family: 'Bebas Neue', sans-serif;
      font-size: clamp(30px, 5vw, 48px);
      line-height: 0.95;
      letter-spacing: 0.6px;
    }}
    h3 {{
      margin: 0 0 14px;
      color: var(--accent-2);
      font-size: 16px;
      font-weight: 600;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1.2fr 1fr;
      gap: 16px;
    }}
    .page:nth-of-type(even) .content {{ order: 2; }}
    .page:nth-of-type(even) .visual {{ order: 1; }}
    .content p {{
      margin: 0 0 9px;
      color: #d8dfe8;
      font-size: 14px;
    }}
    .bullet-list, .action-list {{
      margin: 10px 0 0;
      padding-left: 20px;
      display: grid;
      gap: 6px;
    }}
    .bullet-list li, .action-list li {{
      font-size: 13px;
      color: #e7ebf0;
    }}
    .action-box {{
      margin-top: 12px;
      background: rgba(233,78,27,0.08);
      border: 1px dashed rgba(233,78,27,0.6);
      border-radius: 12px;
      padding: 12px;
    }}
    .action-box h4 {{
      margin: 0 0 8px;
      color: var(--accent);
      font-size: 13px;
      letter-spacing: 0.3px;
      text-transform: uppercase;
    }}
    .cta {{
      margin-top: 12px;
      display: inline-block;
      padding: 10px 12px;
      border-radius: 10px;
      background: linear-gradient(90deg, var(--accent), #ff7a2f);
      color: #fff;
      font-weight: 700;
      font-size: 13px;
    }}
    .visual {{
      min-height: 240px;
      border-radius: 14px;
      overflow: hidden;
      background: #0f131a;
      border: 1px solid rgba(255,255,255,0.12);
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
      min-height: 240px;
      position: relative;
      display: flex;
      align-items: flex-end;
      justify-content: flex-start;
      padding: 14px;
      color: #f1f4f8;
      background: linear-gradient(140deg, #242d3b, #151b24);
    }}
    .shape {{
      position: absolute;
      border-radius: 999px;
      filter: blur(1px);
    }}
    .shape-a {{
      width: 120px;
      height: 120px;
      right: 20px;
      top: 20px;
      background: rgba(233,78,27,0.45);
    }}
    .shape-b {{
      width: 90px;
      height: 90px;
      right: 80px;
      top: 80px;
      background: rgba(246,201,69,0.4);
    }}
    @media (max-width: 900px) {{
      .grid {{ grid-template-columns: 1fr; }}
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
