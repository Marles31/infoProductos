---
name: mvp-infoproduct-orquestador
description: Orquestar el flujo completo del MVP de infoproductos (investigar, seleccionar idea, redactar 5/10 paginas y generar imagenes Nano Banana) usando las tools locales del proyecto con la menor complejidad tecnica posible.
---

# MVP Infoproduct Orquestador

## Objetivo

Ejecutar todo el pipeline en pasos cortos y repetibles.

## Secuencia recomendada

1. Investigacion y scoring:

```powershell
python tools/research_score.py `
  --input .tmp/research_ideas.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md `
  --threshold 75
```

2. Construccion del infoproducto:

```powershell
python tools/build_infoproduct.py `
  --input .tmp/infoproduct_brief.json `
  --out-json .tmp/infoproduct/infoproduct.json `
  --out-md .tmp/infoproduct/infoproduct.md `
  --prompts-json .tmp/infoproduct/nano_prompts.json
```

3. Validacion de prompts sin costo:

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --dry-run
```

4. Generacion de imagenes:

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --model gemini-2.5-flash-image
```

## Criterios de salida final

- Existe una idea con `GO`.
- Existe infoproducto en markdown y json.
- Hay prompts por pagina.
- El manifest de imagenes no reporta errores criticos.

## Regla de simplicidad

Si una decision no mejora conversion ni reduce costo, no agregarla.
