# MVP infoproducto minimo (WAT)

## Objetivo

Crear un infoproducto validado de 5 o 10 paginas con imagenes Nano Banana,
usando el menor costo y la menor complejidad posible.

## Entradas requeridas

- Tema
- Audiencia
- Numero de paginas (`5` o `10`)
- Señales de investigacion (dolores, deseo, objeciones, prueba)

## Tools usadas

1. `tools/research_score.py`
2. `tools/build_infoproduct.py`
3. `tools/nano_banana_generate.py`

## Flujo

1. Investigar de forma manual/web y guardar ideas en JSON.
2. Rankear ideas y elegir la mejor (`GO/NO_GO`).
3. Construir el infoproducto y prompts de imagen.
4. Generar imagenes por lote con Nano Banana.
5. Revisar `manifest.json` para verificar que no haya fallos.

## Comandos base

```powershell
python tools/research_score.py `
  --input .tmp/research_ideas.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md

python tools/build_infoproduct.py `
  --input .tmp/infoproduct_brief.json `
  --out-json .tmp/infoproduct/infoproduct.json `
  --out-md .tmp/infoproduct/infoproduct.md `
  --prompts-json .tmp/infoproduct/nano_prompts.json

python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images
```

## Salidas esperadas

- `.tmp/research_scored.json`
- `.tmp/research_scored.md`
- `.tmp/infoproduct/infoproduct.json`
- `.tmp/infoproduct/infoproduct.md`
- `.tmp/infoproduct/nano_prompts.json`
- `.tmp/infoproduct/images/*`
- `.tmp/infoproduct/images/manifest.json`
