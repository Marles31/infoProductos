#!/usr/bin/env python3
"""Exporta un markdown de infoproducto a PDF simple y legible.

Uso:
    python tools/export_infoproduct_pdf.py \
      --input .tmp/projects/zombie/outputs/infoproduct.md \
      --output .tmp/projects/zombie/outputs/infoproduct.pdf
"""

from __future__ import annotations

import argparse
from pathlib import Path

from fpdf import FPDF


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convierte markdown a PDF simple.")
    parser.add_argument("--input", required=True, help="Ruta markdown de entrada.")
    parser.add_argument("--output", required=True, help="Ruta PDF de salida.")
    return parser.parse_args()


def write_markdown_to_pdf(md_text: str, output_path: Path) -> None:
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_title("Infoproducto")
    pdf.set_author("InfoProductos WAT")

    epw = pdf.w - pdf.l_margin - pdf.r_margin

    def write_line(text: str, h: float = 6.0, style: str = "", size: int = 11) -> None:
        clean = text.replace("\t", " ").replace("\u00a0", " ").strip()
        if not clean:
            pdf.ln(2)
            return
        pdf.set_font("Helvetica", style, size)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(epw, h, clean)

    lines = md_text.splitlines()
    for raw_line in lines:
        line = raw_line.rstrip()

        if line.startswith("# "):
            pdf.ln(2)
            write_line(line[2:].strip(), h=10, style="B", size=18)
            pdf.ln(1)
            continue

        if line.startswith("## "):
            pdf.ln(1)
            write_line(line[3:].strip(), h=8, style="B", size=14)
            pdf.ln(0.5)
            continue

        if line.startswith("### "):
            write_line(line[4:].strip(), h=7, style="B", size=12)
            continue

        if line.startswith("- "):
            write_line(f"- {line[2:].strip()}", h=6, style="", size=11)
            continue

        if not line.strip():
            pdf.ln(2)
            continue

        text = line.replace("**", "")
        write_line(text, h=6, style="", size=11)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(output_path))


def main() -> None:
    args = parse_args()
    input_path = Path(args.input)
    output_path = Path(args.output)

    md_text = input_path.read_text(encoding="utf-8")
    write_markdown_to_pdf(md_text, output_path)
    print(f"[OK] PDF generado: {output_path}")


if __name__ == "__main__":
    main()
