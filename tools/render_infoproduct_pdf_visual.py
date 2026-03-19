#!/usr/bin/env python3
"""Renderiza un infoproducto visual en PDF (sin depender de navegador)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from fpdf import FPDF
from fpdf.enums import XPos, YPos


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Genera PDF visual desde JSON marketero.")
    parser.add_argument("--input", required=True, help="JSON marketero de entrada")
    parser.add_argument("--output", required=True, help="PDF de salida")
    parser.add_argument("--title", default="", help="Titulo opcional")
    return parser.parse_args()


def as_rgb(hex_color: str) -> tuple[int, int, int]:
    c = hex_color.strip().lstrip("#")
    if len(c) != 6:
        return (16, 19, 25)
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def safe_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    return []


def mix(c1: tuple[int, int, int], c2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    tt = max(0.0, min(1.0, t))
    return (
        int(c1[0] * (1 - tt) + c2[0] * tt),
        int(c1[1] * (1 - tt) + c2[1] * tt),
        int(c1[2] * (1 - tt) + c2[2] * tt),
    )


def contrast_text(c: tuple[int, int, int]) -> tuple[int, int, int]:
    luminance = (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) / 255
    return (12, 14, 18) if luminance > 0.62 else (245, 247, 250)


class VisualPDF(FPDF):
    pass


def draw_page_background(pdf: VisualPDF, bg: tuple[int, int, int]) -> None:
    pdf.set_fill_color(*bg)
    pdf.rect(0, 0, 210, 297, style="F")


def write_wrapped(pdf: VisualPDF, text: str, x: float, y: float, w: float, h: float = 6.0) -> float:
    pdf.set_xy(x, y)
    pdf.multi_cell(w, h, text)
    return pdf.get_y()


def draw_visual_module(
    pdf: VisualPDF,
    *,
    x: float,
    y: float,
    w: float,
    h: float,
    pattern: str,
    accent: tuple[int, int, int],
    accent2: tuple[int, int, int],
    panel: tuple[int, int, int],
    panel_alt: tuple[int, int, int],
) -> None:
    pdf.set_fill_color(*panel)
    pdf.rect(x, y, w, h, style="F")

    soft = mix(panel_alt, (255, 255, 255), 0.08)
    warm = mix(accent, panel, 0.35)
    cool = mix(accent2, panel, 0.35)

    if pattern == "alert_grid":
        box_w = (w - 8) / 2
        box_h = (h - 8) / 2
        for row in range(2):
            for col in range(2):
                xx = x + 3 + col * (box_w + 2)
                yy = y + 3 + row * (box_h + 2)
                pdf.set_fill_color(*(warm if (row + col) % 2 == 0 else cool))
                pdf.rect(xx, yy, box_w, box_h, style="F")
    elif pattern == "checklist_cards":
        card_h = (h - 16) / 4
        for i in range(4):
            yy = y + 4 + i * (card_h + 2)
            pdf.set_fill_color(*soft)
            pdf.rect(x + 4, yy, w - 8, card_h, style="F")
            pdf.set_fill_color(*accent2)
            pdf.rect(x + 7, yy + card_h / 2 - 2, 4, 4, style="F")
    elif pattern == "route_map":
        pdf.set_draw_color(*accent2)
        pdf.set_line_width(1.2)
        pdf.line(x + 12, y + 20, x + 34, y + 44)
        pdf.line(x + 34, y + 44, x + 18, y + 68)
        for (nx, ny) in [(x + 10, y + 18), (x + 32, y + 42), (x + 16, y + 66)]:
            pdf.set_fill_color(*accent2)
            pdf.ellipse(nx, ny, 8, 8, style="F")
    elif pattern == "framework_stack":
        colors = [mix(accent2, panel, 0.45), mix(accent, panel, 0.55), soft]
        for i, c in enumerate(colors):
            yy = y + 10 + i * 20
            pdf.set_fill_color(*c)
            pdf.rect(x + 6, yy, w - 12, 16, style="F")
    elif pattern == "energy_meter":
        for i, pct in enumerate([0.88, 0.64, 0.42]):
            yy = y + 14 + i * 18
            pdf.set_fill_color(*soft)
            pdf.rect(x + 8, yy, w - 16, 8, style="F")
            pdf.set_fill_color(*(accent2 if i == 0 else accent))
            pdf.rect(x + 8, yy, (w - 16) * pct, 8, style="F")
    elif pattern == "comparison_split":
        half = w / 2
        pdf.set_fill_color(*mix(accent, panel, 0.25))
        pdf.rect(x, y, half, h, style="F")
        pdf.set_fill_color(*mix(accent2, panel, 0.25))
        pdf.rect(x + half, y, half, h, style="F")
    elif pattern == "offer_stack":
        for i in range(3):
            yy = y + 10 + i * 16
            pdf.set_fill_color(*soft)
            pdf.rect(x + 6, yy, w - 12, 12, style="F")
        pdf.set_fill_color(*accent)
        pdf.rect(x + 6, y + h - 22, w - 12, 14, style="F")
    else:
        pdf.set_fill_color(*accent)
        pdf.ellipse(x + w - 34, y + 8, 22, 22, style="F")
        pdf.set_fill_color(*accent2)
        pdf.ellipse(x + w - 52, y + 24, 16, 16, style="F")


def render_visual_pdf(data: dict[str, Any], out_path: Path, title: str) -> None:
    palette = data.get("brand", {}).get("palette", {})
    bg = as_rgb(str(palette.get("bg", "#101319")))
    surface = as_rgb(str(palette.get("surface", "#1C222B")))
    accent = as_rgb(str(palette.get("accent", "#E94E1B")))
    accent2 = as_rgb(str(palette.get("accent_2", "#F6C945")))
    text = as_rgb(str(palette.get("text", "#F4F6F8")))
    muted = as_rgb(str(palette.get("muted", "#B8C0CC")))

    panel = mix(surface, bg, 0.25)
    panel_alt = mix(surface, bg, 0.5)
    text_soft = mix(text, muted, 0.45)
    action_bg = mix(accent, panel, 0.7)
    action_text = contrast_text(action_bg)
    cta_text = contrast_text(accent)
    chip2_text = contrast_text(accent2)

    pdf = VisualPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=False)

    doc_title = title or str(data.get("offer_name", "Infoproducto Visual"))
    theme = str(data.get("theme", ""))
    pages = data.get("pages", [])
    total = max(1, len(pages))

    for idx, page in enumerate(pages, start=1):
        pdf.add_page()
        draw_page_background(pdf, bg)

        pdf.set_fill_color(*surface)
        pdf.rect(10, 10, 190, 35, style="F")
        pdf.set_fill_color(*accent)
        pdf.rect(10, 10, 190, 4, style="F")
        progress_w = 190 * (idx / total)
        pdf.set_fill_color(*accent2)
        pdf.rect(10, 44, progress_w, 2, style="F")

        pdf.set_text_color(*contrast_text(accent))
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_fill_color(*accent)
        pdf.rect(14, 17, 24, 8, style="F")
        pdf.set_xy(14, 19)
        pdf.cell(24, 4, f"P{idx:02d}/{total:02d}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")

        pdf.set_fill_color(*accent2)
        pdf.set_text_color(*chip2_text)
        pdf.rect(40, 17, 70, 8, style="F")
        pdf.set_xy(40, 19)
        pdf.cell(
            70,
            4,
            str(page.get("section_title", ""))[:35].upper(),
            new_x=XPos.RIGHT,
            new_y=YPos.TOP,
            align="C",
        )

        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "B", 16)
        write_wrapped(pdf, str(page.get("headline", "")), 14, 27, 182, h=6.8)

        text_left = idx % 2 == 1
        left_x = 12 if text_left else 108
        right_x = 108 if text_left else 12
        col_w = 90
        top_y = 52
        col_h = 210

        pdf.set_fill_color(*surface)
        pdf.rect(left_x, top_y, col_w, col_h, style="F")
        pdf.set_fill_color(*panel_alt)
        pdf.rect(right_x, top_y, col_w, col_h, style="F")

        hook = str(page.get("hook", ""))
        one_liner = str(page.get("one_liner", ""))
        quick_wins = safe_list(page.get("quick_wins"))
        avoid_list = safe_list(page.get("avoid_list"))

        hook_bg = mix(accent, surface, 0.72)
        pdf.set_fill_color(*hook_bg)
        pdf.rect(left_x + 4, top_y + 6, col_w - 8, 18, style="F")
        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "B", 8.8)
        write_wrapped(pdf, hook[:150], left_x + 7, top_y + 10, col_w - 14, h=4.1)

        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "", 9)
        y = top_y + 28
        for paragraph in safe_list(page.get("body"))[:3]:
            y = write_wrapped(pdf, paragraph, left_x + 5, y, col_w - 10, h=4.5)
            y += 0.8

        note_bg = mix(panel_alt, surface, 0.55)
        pdf.set_fill_color(*note_bg)
        pdf.rect(left_x + 4, y + 1, col_w - 8, 14, style="F")
        pdf.set_text_color(*text_soft)
        pdf.set_font("Helvetica", "I", 7.8)
        write_wrapped(pdf, one_liner[:120], left_x + 7, y + 5, col_w - 14, h=3.7)

        box1_y = y + 17
        win_bg = mix(panel, surface, 0.55)
        pdf.set_fill_color(*win_bg)
        pdf.rect(left_x + 4, box1_y, col_w - 8, 30, style="F")
        pdf.set_text_color(*accent2)
        pdf.set_font("Helvetica", "B", 8.5)
        write_wrapped(pdf, "GANANCIAS RAPIDAS", left_x + 7, box1_y + 4, col_w - 14, h=3.9)
        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "", 7.9)
        wy = box1_y + 9
        for item in quick_wins[:3]:
            wy = write_wrapped(pdf, f"- {item}", left_x + 7, wy, col_w - 14, h=3.5)

        box2_y = box1_y + 33
        warn_bg = mix(action_bg, panel, 0.35)
        pdf.set_fill_color(*warn_bg)
        pdf.rect(left_x + 4, box2_y, col_w - 8, 26, style="F")
        pdf.set_text_color(*accent)
        pdf.set_font("Helvetica", "B", 8.4)
        write_wrapped(pdf, "EVITA ESTO", left_x + 7, box2_y + 4, col_w - 14, h=3.8)
        pdf.set_text_color(*action_text)
        pdf.set_font("Helvetica", "", 7.7)
        ay2 = box2_y + 9
        for item in avoid_list[:2]:
            ay2 = write_wrapped(pdf, f"- {item}", left_x + 7, ay2, col_w - 14, h=3.4)

        ay = box2_y + 29
        pdf.set_fill_color(*action_bg)
        pdf.rect(left_x + 4, ay, col_w - 8, 26, style="F")
        pdf.set_text_color(*accent)
        pdf.set_font("Helvetica", "B", 8.6)
        write_wrapped(pdf, str(page.get("action_title", "ACCION INMEDIATA")).upper(), left_x + 7, ay + 4, col_w - 14, h=3.8)

        pdf.set_text_color(*action_text)
        pdf.set_font("Helvetica", "", 7.8)
        sy = ay + 9
        for step in safe_list(page.get("action_steps"))[:2]:
            sy = write_wrapped(pdf, f"- {step}", left_x + 7, sy, col_w - 14, h=3.4)

        cta_y = ay + 28
        pdf.set_fill_color(*accent)
        pdf.rect(left_x + 4, cta_y, col_w - 8, 14, style="F")
        pdf.set_text_color(*cta_text)
        pdf.set_font("Helvetica", "B", 7.8)
        write_wrapped(pdf, str(page.get("micro_cta", ""))[:120], left_x + 7, cta_y + 4, col_w - 14, h=3.4)

        pattern = str(page.get("design_pattern", "hero_split"))
        draw_visual_module(
            pdf,
            x=right_x + 4,
            y=top_y + 8,
            w=col_w - 8,
            h=94,
            pattern=pattern,
            accent=accent,
            accent2=accent2,
            panel=panel,
            panel_alt=panel_alt,
        )
        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "B", 8.8)
        write_wrapped(pdf, "RESUMEN VISUAL", right_x + 8, top_y + 108, col_w - 16, h=4.4)
        pdf.set_text_color(*text_soft)
        pdf.set_font("Helvetica", "", 8.2)
        write_wrapped(pdf, one_liner[:135], right_x + 8, top_y + 114, col_w - 16, h=4)

        tag_y = top_y + 136
        for item in quick_wins[:3]:
            tag_color = mix(accent2, panel_alt, 0.42)
            pdf.set_fill_color(*tag_color)
            pdf.rect(right_x + 8, tag_y, col_w - 16, 8, style="F")
            pdf.set_text_color(*text)
            pdf.set_font("Helvetica", "B", 7.2)
            write_wrapped(pdf, item[:46], right_x + 10, tag_y + 2.4, col_w - 20, h=3.2)
            tag_y += 10

        pdf.set_text_color(*muted)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_xy(12, 270)
        pdf.cell(130, 5, doc_title[:70], new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        pdf.cell(60, 5, theme[:40], new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))


def main() -> None:
    args = parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    render_visual_pdf(data, Path(args.output), args.title)
    print(f"[OK] PDF visual generado: {args.output}")


if __name__ == "__main__":
    main()
