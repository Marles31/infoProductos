# Diseno infoproducto visual

## Objetivo

Renderizar una version visual con mejor jerarquia tipografica y bloques de lectura rapida.

## Skills obligatorias

1. `skills/diseno-infoproducto-conversion/SKILL.md`
2. `skills/copy-marketero-directo/SKILL.md`

## Tools

- `tools/render_infoproduct_html.py`
- `tools/render_infoproduct_pdf_visual.py`

## Comandos

```powershell
python tools/render_infoproduct_html.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_visual.html `
  --images-dir .tmp/projects/<slug>/images `
  --title "<Titulo Comercial>"

python tools/render_infoproduct_pdf_visual.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_visual.pdf `
  --title "<Titulo Comercial>"
```

## Validacion

- Hay bloques visuales: `hook`, `ganancias rapidas`, `evita esto`, `accion inmediata`.
- Tipografia visible en 3 niveles: titular, subtitulo, cuerpo/listas.
- No aparecen textos tecnicos internos tipo `PATRON: ...` en PDF final.
