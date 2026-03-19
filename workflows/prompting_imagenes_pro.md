# Prompting imagenes pro (orquestado)

## Objetivo

Generar prompts consistentes por pagina, respetando politicas de contenido del brief.

## Skills obligatorias

1. `skills/prompting-imagenes-conversion/SKILL.md`
2. `skills/nano-banana-prompting/SKILL.md`

## Tool

`tools/build_nano_prompts_pro.py`

## Comando

```powershell
python tools/build_nano_prompts_pro.py `
  --input .tmp/projects/<slug>/outputs/infoproduct_marketing.json `
  --output .tmp/projects/<slug>/outputs/nano_prompts_pro.json `
  --aspect-ratio 3:2 `
  --image-size 1K
```

## Validacion

- `meta.required_theme_entities` incluye terminos obligatorios del tema.
- Las restricciones salen de `prompting.*` (no hardcoded).
- Cada prompt tiene estructura por bloques (subject, action, camera, lighting, etc.).
