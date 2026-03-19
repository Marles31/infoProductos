# Generacion imagenes Nano Banana

## Objetivo

Crear imagenes por pagina a partir de prompts pro con control de costo.

## Skill obligatoria

Leer primero: `skills/nano-banana-prompting/SKILL.md`

## Requisito

Definir API key:

```powershell
$env:GEMINI_API_KEY="tu_api_key"
```

## Tool

`tools/nano_banana_generate.py`

## Comandos

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/projects/<slug>/outputs/nano_prompts_pro.json `
  --output-dir .tmp/projects/<slug>/images `
  --manifest .tmp/projects/<slug>/images/manifest.json `
  --model gemini-2.5-flash-image
```

Validacion sin costo:

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/projects/<slug>/outputs/nano_prompts_pro.json `
  --output-dir .tmp/projects/<slug>/images `
  --manifest .tmp/projects/<slug>/images/manifest.json `
  --dry-run
```

## Validacion

- Existe `manifest.json`.
- Cada pagina tiene estado `ok` o error claro para reintento.
