# Produccion infoproducto (5 o 10 paginas)

## Objetivo

Convertir un brief validado en copy estructurado y prompts visuales listos.

## Entrada

JSON con:

- `topic`
- `audience`
- `page_count` (`5` o `10`)
- `offer_name`
- `goal`
- `cta`
- `research.pain_points`
- `research.desired_outcomes`
- `research.objections`
- `research.proof_points`

## Tool

`tools/build_infoproduct.py`

## Command

```powershell
python tools/build_infoproduct.py `
  --input .tmp/infoproduct_brief.json `
  --out-json .tmp/infoproduct/infoproduct.json `
  --out-md .tmp/infoproduct/infoproduct.md `
  --prompts-json .tmp/infoproduct/nano_prompts.json
```

## Salidas

- JSON estructurado para automatizar
- Markdown para revision humana
- JSON de prompts para Nano Banana
