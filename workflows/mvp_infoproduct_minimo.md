# MVP infoproducto minimo (orquestado)

## Objetivo

Construir un infoproducto de 5 o 10 paginas con costo bajo y flujo reproducible.

## Entradas

- Brief en `.tmp/projects/<slug>/inputs/brief.json`
- API key de Gemini solo si se van a generar imagenes

## Pasos (skill -> tool)

1. Leer `skills/mvp-infoproduct-orquestador/SKILL.md`
2. Leer `skills/investigacion-mercado-lite/SKILL.md`
3. Ejecutar `tools/research_score.py`
4. Leer `skills/redaccion-infoproducto-5-10/SKILL.md`
5. Leer `skills/copy-marketero-directo/SKILL.md`
6. Ejecutar `tools/build_infoproduct_marketing.py`
7. Leer `skills/diseno-infoproducto-conversion/SKILL.md`
8. Ejecutar `tools/render_infoproduct_html.py`
9. Ejecutar `tools/render_infoproduct_pdf_visual.py`
10. Leer `skills/prompting-imagenes-conversion/SKILL.md`
11. Ejecutar `tools/build_nano_prompts_pro.py`
12. (Opcional) Ejecutar `tools/nano_banana_generate.py`

## Validacion minima

- Hay `infoproduct_marketing.json`
- Hay `infoproduct_visual.html`
- Hay `infoproduct_visual.pdf`
- Hay `nano_prompts_pro.json`
