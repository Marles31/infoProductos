# Produccion infoproducto (copy)

## Objetivo

Crear copy marketero por pagina con lenguaje claro, bullets y estructura de conversion.

## Skills obligatorias

1. `skills/redaccion-infoproducto-5-10/SKILL.md`
2. `skills/copy-marketero-directo/SKILL.md`

## Tool

`tools/build_infoproduct_marketing.py`

## Comando

```powershell
python tools/build_infoproduct_marketing.py `
  --input .tmp/projects/<slug>/inputs/brief.json `
  --output .tmp/projects/<slug>/outputs/infoproduct_marketing.json
```

## Validacion

- Cada pagina incluye: `hook`, `body`, `bullets`, `quick_wins`, `avoid_list`, `action_steps`.
- El JSON incluye `brand.palette` y `prompting`.
