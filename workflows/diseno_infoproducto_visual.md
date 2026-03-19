# Diseno infoproducto visual (marketing + conversion)

## Objetivo

Pasar de brief tecnico a infoproducto visual vendible.

## Tools

- `tools/build_infoproduct_marketing.py`
- `tools/render_infoproduct_html.py`

## Flujo

```powershell
python tools/build_infoproduct_marketing.py `
  --input .tmp/projects/zombie/inputs/brief.json `
  --output .tmp/projects/zombie/outputs/infoproduct_marketing.json

python tools/render_infoproduct_html.py `
  --input .tmp/projects/zombie/outputs/infoproduct_marketing.json `
  --output .tmp/projects/zombie/outputs/infoproduct_visual.html `
  --images-dir .tmp/projects/zombie/images `
  --title "Manual de Supervivencia Zombie 72H"
```

## Salida

- `.tmp/projects/zombie/outputs/infoproduct_marketing.json`
- `.tmp/projects/zombie/outputs/infoproduct_visual.html`
