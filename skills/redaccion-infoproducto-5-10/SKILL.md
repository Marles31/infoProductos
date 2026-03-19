---
name: redaccion-infoproducto-5-10
description: Redactar infoproductos de 5 o 10 paginas desde un brief validado, generando estructura, copy comercial y direccion visual por pagina. Usar cuando ya existe una idea GO y se necesita convertirla en entregable listo para publicar.
---

# Redaccion Infoproducto 5-10

## Objetivo

Transformar un brief de mercado en un infoproducto completo con copy y plan visual por pagina.

## Input minimo

- `topic`
- `audience`
- `page_count` (5 o 10)
- `offer_name`
- `goal`
- `cta`
- `research.pain_points`
- `research.desired_outcomes`
- `research.objections`
- `research.proof_points`

## Flujo minimo

1. Construir `.tmp/infoproduct_brief.json` usando como base `tools/examples/infoproduct_brief.sample.json`.
2. Ejecutar:

```powershell
python tools/build_infoproduct.py `
  --input .tmp/infoproduct_brief.json `
  --out-json .tmp/infoproduct/infoproduct.json `
  --out-md .tmp/infoproduct/infoproduct.md `
  --prompts-json .tmp/infoproduct/nano_prompts.json
```

3. Revisar que cada pagina tenga:
- `hook`
- `body_copy`
- `bullets`
- `image_brief`

## Reglas de copy

- Escribir para conversion, no para relleno.
- Mantener fraseo directo y accionable.
- Resolver objeciones dentro del contenido.
- Cerrar con CTA explicito en la ultima pagina.

## Salida obligatoria

- `.tmp/infoproduct/infoproduct.md` para revision
- `.tmp/infoproduct/infoproduct.json` para automatizacion
- `.tmp/infoproduct/nano_prompts.json` para imagenes
