# Generacion imagenes Nano Banana

## Objetivo

Generar una imagen por pagina a partir de prompts, con costo minimo.

## Requisito

Definir API key de Gemini:

```powershell
$env:GEMINI_API_KEY="tu_api_key"
```

## Input

`.tmp/infoproduct/nano_prompts.json`

## Tool

`tools/nano_banana_generate.py`

## Command

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --model gemini-2.5-flash-image
```

## Modo validacion (sin costo)

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --dry-run
```

## Salida

- Imagenes en `.tmp/infoproduct/images/`
- Reporte `.tmp/infoproduct/images/manifest.json`
