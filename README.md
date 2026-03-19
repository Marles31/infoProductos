# InfoProductos - WAT Starter

Proyecto inicial preparado con la arquitectura WAT (Workflows, Agents, Tools).

## Estructura base

- `.tmp/`: archivos temporales y regenerables
- `tools/`: scripts Python para ejecucion deterministica
- `workflows/`: SOPs en Markdown que describen que hacer
- `.env`: variables de entorno (no versionar)

## Puesta en marcha

1. Crear entorno virtual:
```powershell
python -m venv .venv
```
2. Activar entorno:
```powershell
.\.venv\Scripts\Activate.ps1
```
3. Instalar dependencias (cuando existan en `requirements.txt`):
```powershell
pip install -r requirements.txt
```
4. Copiar variables de entorno:
```powershell
Copy-Item .env.example .env
```
5. Completar `.env` con tus credenciales.

## MVP implementado

### Workflows

- `workflows/mvp_infoproduct_minimo.md`
- `workflows/investigacion_mercado_lite.md`
- `workflows/produccion_infoproducto.md`
- `workflows/generacion_imagenes_nano.md`
- `workflows/diseno_infoproducto_visual.md`
- `workflows/exportar_pdf.md`

### Tools

- `tools/research_score.py`
- `tools/build_infoproduct.py`
- `tools/nano_banana_generate.py`
- `tools/build_infoproduct_marketing.py`
- `tools/render_infoproduct_html.py`
- `tools/export_infoproduct_pdf.py`

### Skills

- `skills/investigacion-mercado-lite`
- `skills/redaccion-infoproducto-5-10`
- `skills/nano-banana-prompting`
- `skills/mvp-infoproduct-orquestador`
- `skills/diseno-infoproducto-conversion`
- `skills/copy-marketero-directo`

## Prueba rapida (MVP)

1. Rankear ideas:
```powershell
python tools/research_score.py `
  --input tools/examples/research_ideas.sample.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md
```

2. Construir infoproducto (5/10 paginas):
```powershell
python tools/build_infoproduct.py `
  --input tools/examples/infoproduct_brief.sample.json `
  --out-json .tmp/infoproduct/infoproduct.json `
  --out-md .tmp/infoproduct/infoproduct.md `
  --prompts-json .tmp/infoproduct/nano_prompts.json
```

3. Generar imagenes Nano Banana:
```powershell
$env:GEMINI_API_KEY="tu_api_key"
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --model gemini-2.5-flash-image
```

4. Test sin costo (sin llamar API):
```powershell
python tools/nano_banana_generate.py `
  --prompts .tmp/infoproduct/nano_prompts.json `
  --output-dir .tmp/infoproduct/images `
  --dry-run
```

## Notas

- `credentials.json` y `token.json` se mantienen fuera de git.
- Todo lo que este en `.tmp/` debe considerarse descartable.
