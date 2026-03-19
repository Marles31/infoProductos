#!/usr/bin/env python3
"""Rankea ideas de infoproducto usando una matriz de senales de mercado.

Uso rapido:
    python tools/research_score.py \
      --input tools/examples/research_ideas.sample.json \
      --output .tmp/research_scored.json \
      --markdown-out .tmp/research_scored.md
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WEIGHTS = {
    "demand": 0.30,
    "purchase_intent": 0.30,
    "competition_gap": 0.20,
    "differentiation": 0.10,
    "execution_ease": 0.10,
}


@dataclass
class IdeaScore:
    idea_id: str
    title: str
    audience: str
    score_0_100: float
    decision: str
    strengths: list[str]
    risks: list[str]
    evidence_count: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Puntua ideas de infoproducto y devuelve ranking GO/NO_GO."
    )
    parser.add_argument("--input", required=True, help="Ruta al JSON de ideas.")
    parser.add_argument(
        "--output",
        default=".tmp/research_scored.json",
        help="Ruta del JSON de salida.",
    )
    parser.add_argument(
        "--markdown-out",
        default="",
        help="Ruta opcional para reporte markdown.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=75.0,
        help="Umbral GO en escala 0-100.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_number_0_10(value: Any, field_name: str, idea_title: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"'{field_name}' en '{idea_title}' debe ser numerico (0-10).")
    if value < 0 or value > 10:
        raise ValueError(f"'{field_name}' en '{idea_title}' debe estar entre 0 y 10.")
    return float(value)


def extract_signals(idea: dict[str, Any]) -> dict[str, float]:
    title = str(idea.get("title", "idea_sin_titulo"))
    raw_signals = idea.get("signals", {})
    if not isinstance(raw_signals, dict):
        raise ValueError(f"'signals' en '{title}' debe ser un objeto JSON.")

    signals: dict[str, float] = {}
    for field in WEIGHTS:
        if field not in raw_signals:
            raise ValueError(f"Falta senal '{field}' en idea '{title}'.")
        signals[field] = ensure_number_0_10(raw_signals[field], field, title)
    return signals


def score_idea(idea: dict[str, Any], threshold: float, idx: int) -> IdeaScore:
    title = str(idea.get("title", f"Idea {idx + 1}")).strip()
    audience = str(idea.get("audience", "")).strip()
    signals = extract_signals(idea)

    weighted_0_10 = sum(signals[field] * weight for field, weight in WEIGHTS.items())
    score_0_100 = round(weighted_0_10 * 10, 2)
    decision = "GO" if score_0_100 >= threshold else "NO_GO"

    strengths: list[str] = []
    risks: list[str] = []
    for field, value in signals.items():
        if value >= 8:
            strengths.append(field)
        elif value <= 4:
            risks.append(field)

    evidence = idea.get("evidence", [])
    evidence_count = len(evidence) if isinstance(evidence, list) else 0

    return IdeaScore(
        idea_id=str(idea.get("id", f"idea_{idx + 1}")),
        title=title,
        audience=audience,
        score_0_100=score_0_100,
        decision=decision,
        strengths=strengths,
        risks=risks,
        evidence_count=evidence_count,
    )


def build_markdown_report(
    topic: str, threshold: float, ranked: list[IdeaScore], out_path: Path
) -> None:
    lines: list[str] = []
    lines.append(f"# Ranking de ideas: {topic}")
    lines.append("")
    lines.append(f"- Umbral GO: **{threshold:.1f}**")
    lines.append(f"- Total ideas: **{len(ranked)}**")
    lines.append("")
    lines.append("| Rank | Idea | Score | Decision | Evidencias |")
    lines.append("|---|---|---:|---|---:|")
    for i, item in enumerate(ranked, start=1):
        lines.append(
            f"| {i} | {item.title} | {item.score_0_100:.2f} | {item.decision} | {item.evidence_count} |"
        )
    lines.append("")
    lines.append("## Detalle")
    lines.append("")
    for i, item in enumerate(ranked, start=1):
        lines.append(f"### {i}. {item.title}")
        lines.append(f"- Audiencia: {item.audience or 'N/D'}")
        lines.append(f"- Decision: {item.decision}")
        lines.append(f"- Score: {item.score_0_100:.2f}")
        lines.append(f"- Fortalezas: {', '.join(item.strengths) if item.strengths else 'N/D'}")
        lines.append(f"- Riesgos: {', '.join(item.risks) if item.risks else 'N/D'}")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    markdown_path = Path(args.markdown_out) if args.markdown_out else None

    data = read_json(input_path)
    ideas = data.get("ideas")
    if not isinstance(ideas, list) or not ideas:
        raise ValueError("El JSON de entrada debe tener 'ideas' como lista no vacia.")

    topic = str(data.get("topic", "sin_tema"))
    ranked = sorted(
        [score_idea(idea, args.threshold, idx) for idx, idea in enumerate(ideas)],
        key=lambda x: x.score_0_100,
        reverse=True,
    )

    best_idea = ranked[0] if ranked else None
    result = {
        "topic": topic,
        "scored_at_utc": datetime.now(timezone.utc).isoformat(),
        "threshold": args.threshold,
        "best_idea_id": best_idea.idea_id if best_idea else None,
        "best_idea_title": best_idea.title if best_idea else None,
        "ranking": [
            {
                "rank": i + 1,
                "id": item.idea_id,
                "title": item.title,
                "audience": item.audience,
                "score_0_100": item.score_0_100,
                "decision": item.decision,
                "strengths": item.strengths,
                "risks": item.risks,
                "evidence_count": item.evidence_count,
            }
            for i, item in enumerate(ranked)
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, ensure_ascii=True, indent=2),
        encoding="utf-8",
    )

    if markdown_path:
        build_markdown_report(topic, args.threshold, ranked, markdown_path)

    print(f"[OK] Ranking generado: {output_path}")
    if markdown_path:
        print(f"[OK] Reporte markdown: {markdown_path}")


if __name__ == "__main__":
    main()
