# Prompting imagenes pro

## Objetivo

Generar prompts de imagen con mayor control y consistencia de serie.

## Tool

`tools/build_nano_prompts_pro.py`

## Command

```powershell
python tools/build_nano_prompts_pro.py `
  --input .tmp/projects/zombie/outputs/infoproduct_marketing.json `
  --output .tmp/projects/zombie/outputs/nano_prompts_pro.json `
  --aspect-ratio 3:2 `
  --image-size 1K
```

## Salida

- `.tmp/projects/zombie/outputs/nano_prompts_pro.json`
