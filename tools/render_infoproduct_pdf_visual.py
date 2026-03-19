#!/usr/bin/env python3
"""Renderiza un infoproducto visual en PDF (sin depender de navegador)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from fpdf import FPDF


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


class VisualPDF(FPDF):
    pass


def draw_page_background(pdf: VisualPDF, bg: tuple[int, int, int]) -> None:
    pdf.set_fill_color(*bg)
    pdf.rect(0, 0, 210, 297, style="F")


def write_wrapped(pdf: VisualPDF, text: str, x: float, y: float, w: float, h: float = 6.0) -> float:
    pdf.set_xy(x, y)
    pdf.multi_cell(w, h, text)
    return pdf.get_y()


def render_visual_pdf(data: dict[str, Any], out_path: Path, title: str) -> None:
    palette = data.get("brand", {}).get("palette", {})
    bg = as_rgb(str(palette.get("bg", "#101319")))
    surface = as_rgb(str(palette.get("surface", "#1C222B")))
    accent = as_rgb(str(palette.get("accent", "#E94E1B")))
    accent2 = as_rgb(str(palette.get("accent_2", "#F6C945")))
    text = as_rgb(str(palette.get("text", "#F4F6F8")))
    muted = as_rgb(str(palette.get("muted", "#B8C0CC")))

    pdf = VisualPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=False)

    doc_title = title or str(data.get("offer_name", "Infoproducto Visual"))
    theme = str(data.get("theme", ""))

    for page in data.get("pages", []):
        pdf.add_page()
        draw_page_background(pdf, bg)

        # Hero/top block
        pdf.set_fill_color(*surface)
        pdf.rect(10, 10, 190, 40, style="F")
        pdf.set_fill_color(*accent)
        pdf.rect(10, 10, 190, 4, style="F")

        # Chips
        pdf.set_fill_color(*accent)
        pdf.rect(14, 17, 28, 8, style="F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_xy(14, 19)
        pdf.cell(28, 4, f"PAG {int(page['page_number']):02d}", 0, 0, "C")

        pdf.set_fill_color(*accent2)
        pdf.set_text_color(20, 20, 20)
        pdf.rect(44, 17, 74, 8, style="F")
        pdf.set_xy(44, 19)
        pdf.cell(74, 4, str(page.get("section_title", ""))[:38].upper(), 0, 0, "C")

        # Title/subtitle
        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "B", 17)
        write_wrapped(pdf, str(page.get("headline", "")), 14, 28, 182, h=7)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*muted)
        write_wrapped(pdf, str(page.get("subheadline", "")), 14, 43, 182, h=5)

        # Left column content
        left_x = 12
        left_y = 56
        left_w = 118
        right_x = 134
        right_w = 64

        pdf.set_fill_color(*surface)
        pdf.rect(left_x, left_y, left_w, 205, style="F")
        pdf.set_fill_color(26, 33, 43)
        pdf.rect(right_x, left_y, right_w, 205, style="F")

        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "", 10)
        y = left_y + 8
        for paragraph in safe_list(page.get("body")):
            y = write_wrapped(pdf, paragraph, left_x + 6, y, left_w - 12, h=5)
            y += 2

        # Bullets box
        pdf.set_fill_color(27, 34, 45)
        pdf.rect(left_x + 5, y + 2, left_w - 10, 62, style="F")
        pdf.set_text_color(*accent2)
        pdf.set_font("Helvetica", "B", 10)
        write_wrapped(pdf, "PUNTOS CLAVE", left_x + 8, y + 6, left_w - 16, h=5)
        pdf.set_text_color(*text)
        pdf.set_font("Helvetica", "", 9)
        by = y + 12
        for bullet in safe_list(page.get("bullets"))[:4]:
            by = write_wrapped(pdf, f"- {bullet}", left_x + 8, by, left_w - 16, h=4.7)
            by += 1

        # Action box
        ay = min(by + 4, left_y + 150)
        pdf.set_fill_color(41, 19, 12)
        pdf.rect(left_x + 5, ay, left_w - 10, 46, style="F")
        pdf.set_text_color(*accent)
        pdf.set_font("Helvetica", "B", 10)
        write_wrapped(pdf, str(page.get("action_title", "ACCION INMEDIATA")).upper(), left_x + 8, ay + 5, left_w - 16, h=5)
        pdf.set_text_color(255, 229, 220)
        pdf.set_font("Helvetica", "", 9)
        sy = ay + 11
        for step in safe_list(page.get("action_steps"))[:3]:
            sy = write_wrapped(pdf, f"- {step}", left_x + 8, sy, left_w - 16, h=4.6)
            sy += 0.5

        # CTA block
        cta_y = left_y + 186
        pdf.set_fill_color(*accent)
        pdf.rect(left_x + 5, cta_y, left_w - 10, 18, style="F")
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 9)
        write_wrapped(pdf, str(page.get("micro_cta", "")), left_x + 8, cta_y + 5, left_w - 16, h=4.2)

        # Right column visual placeholder
        pdf.set_fill_color(48, 58, 73)
        pdf.rect(right_x + 6, left_y + 8, right_w - 12, 86, style="F")
        pdf.set_fill_color(*accent)
        pdf.ellipse(right_x + 35, left_y + 16, 20, 20, style="F")
        pdf.set_fill_color(*accent2)
        pdf.ellipse(right_x + 20, left_y + 34, 14, 14, style="F")

        pdf.set_text_color(235, 240, 245)
        pdf.set_font("Helvetica", "B", 9)
        write_wrapped(pdf, "VISUAL KEY FRAME", right_x + 10, left_y + 98, right_w - 20, h=5)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(196, 205, 218)
        write_wrapped(
            pdf,
            str(page.get("image_prompt", ""))[:360],
            right_x + 10,
            left_y + 104,
            right_w - 20,
            h=4.3,
        )

        # Footer
        pdf.set_text_color(145, 156, 170)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_xy(12, 270)
        pdf.cell(130, 5, doc_title[:70], 0, 0, "L")
        pdf.cell(60, 5, theme[:40], 0, 0, "R")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))


def main() -> None:
    args = parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    render_visual_pdf(data, Path(args.output), args.title)
    print(f"[OK] PDF visual generado: {args.output}")


if __name__ == "__main__":
    main()
