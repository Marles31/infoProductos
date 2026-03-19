---
name: nano-banana-prompting
description: Diseñar prompts consistentes por pagina y generar imagenes con Nano Banana (Gemini image models) con costo minimo. Usar cuando ya existe el infoproducto y se necesita producir visuales coherentes y reutilizables.
---

# Nano Banana Prompting

## Objetivo

Pasar de direccion visual por pagina a imagenes finales listas para uso comercial.

## Requisito

Definir API key en `.env`:

```env
GEMINI_API_KEY=tu_api_key
```

## Flujo minimo

1. Usar `.tmp/infoproduct/nano_prompts.json` (salida de `build_infoproduct.py`).
2. Validar sin costo:

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --dry-run
```

3. Generar imagenes reales:

```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --model gemini-2.5-flash-image
```

4. Revisar `.tmp/infoproduct/images/manifest.json`.

## Regla de consistencia visual

- Mantener una misma direccion de estilo para todas las paginas.
- Evitar cambios bruscos de paleta, iluminacion o composicion.
- Usar texto dentro de imagen solo cuando aporte conversion.

## Salida obligatoria

- Imagenes en `.tmp/infoproduct/images/`
- `manifest.json` con estado por pagina
