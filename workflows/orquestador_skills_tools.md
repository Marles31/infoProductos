# Workflow Orquestado Skills + Tools

## Objetivo

Ejecutar el pipeline completo de infoproducto con orden claro:
skill -> tool -> skill -> tool.

## Entradas minimas

- `topic`
- `offer_name`
- `page_count` (`5` o `10`)
- `cta`
- `research.*` (dolor, resultado, objecion, prueba)
- Opcional: `brand.*`, `prompting.*`, `page_blueprint`

## Flujo oficial

1. Leer skill: `skills/mvp-infoproduct-orquestador/SKILL.md`
2. Leer skill: `skills/investigacion-mercado-lite/SKILL.md`
3. Ejecutar tool: `tools/research_score.py` para ranking GO/NO_GO
4. Leer skill: `skills/redaccion-infoproducto-5-10/SKILL.md`
5. Leer skill: `skills/copy-marketero-directo/SKILL.md`
6. Ejecutar tool: `tools/build_infoproduct_marketing.py`
7. Leer skill: `skills/diseno-infoproducto-conversion/SKILL.md`
8. Ejecutar tool: `tools/render_infoproduct_html.py`
9. Ejecutar tool: `tools/render_infoproduct_pdf_visual.py`
10. Leer skill: `skills/prompting-imagenes-conversion/SKILL.md`
11. Leer skill: `skills/nano-banana-prompting/SKILL.md`
12. Ejecutar tool: `tools/build_nano_prompts_pro.py`
13. Ejecutar tool: `tools/nano_banana_generate.py` (si hay API key)

## Comandos de referencia

```powershell
python tools/research_score.py `
  --input .tmp/research_ideas.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md `
  --threshold 75

python tools/build_infoproduct_marketing.py `
  --input .tmp/projects/<slug>/inputs/brief.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_marketing.json

python tools/render_infoproduct_html.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_visual.html `
  --images-dir .tmp/projects/<slug>/images `
  --title "<Titulo Comercial>"

python tools/render_infoproduct_pdf_visual.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_visual.pdf `
  --title "<Titulo Comercial>"

python tools/build_nano_prompts_pro.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/nano_prompts_pro.json `
  --aspect-ratio 3:2 `
  --image-size 1K
```

## Validaciones

- Existe `infoproduct_marketing.json` con `pages` y `brand.palette`.
- Existe `infoproduct_visual.html` y `infoproduct_visual.pdf`.
- Existe `nano_prompts_pro.json` con `meta.required_theme_entities`.
- Si hay imagenes: existe `images/manifest.json` sin errores criticos.
