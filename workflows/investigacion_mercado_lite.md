# Investigacion mercado lite (orquestado)

## Objetivo

Transformar un tema en ideas evaluables con señal numerica y decision GO/NO_GO.

## Skill obligatoria

Leer primero: `skills/investigacion-mercado-lite/SKILL.md`

## Tool

`tools/research_score.py`

## Comando

```powershell
python tools/research_score.py `
  --input .tmp/research_ideas.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md `
  --threshold 75
```

## Validacion

- `research_scored.json` contiene `status` por idea.
- Hay al menos una idea `GO` o una recomendacion clara de ajuste.
