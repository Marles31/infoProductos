# Exportar PDF final

## Objetivo

Generar PDF final de lectura/comercial (sin texto tecnico interno).

## Skills obligatorias

1. `skills/diseno-infoproducto-conversion/SKILL.md`
2. `skills/copy-marketero-directo/SKILL.md`

## Tool recomendado

`tools/render_infoproduct_pdf_visual.py`

## Comando

```powershell
python tools/render_infoproduct_pdf_visual.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_visual.pdf `
  --title "<Titulo Comercial>"
```

## Validacion

- El PDF contiene hook, listas y CTA por pagina.
- No contiene bloques tecnicos de depuracion.
