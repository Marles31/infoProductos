# Investigacion mercado lite

## Objetivo

Tomar un tema y convertirlo en 2 a 5 ideas evaluables con señales numericas.

## Entrada

- Tema principal
- Audiencia objetivo
- Hallazgos de fuentes abiertas (busqueda web, comunidades, catalogos)

## Output

Archivo JSON con estructura:

```json
{
  "topic": "Tema",
  "ideas": [
    {
      "id": "idea_1",
      "title": "Nombre de idea",
      "audience": "Segmento",
      "signals": {
        "demand": 0,
        "purchase_intent": 0,
        "competition_gap": 0,
        "differentiation": 0,
        "execution_ease": 0
      },
      "evidence": []
    }
  ]
}
```

## Regla de evaluacion

- Escala por señal: `0` a `10`.
- Criterio de avance: usar `tools/research_score.py` con umbral sugerido `75`.

## Command

```powershell
python tools/research_score.py `
  --input .tmp/research_ideas.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md `
  --threshold 75
```
