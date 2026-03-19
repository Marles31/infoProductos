# Tools

Este directorio contiene scripts Python que ejecutan tareas de forma deterministica.

Convenciones sugeridas:

- Un script por tarea o dominio
- Parametros claros por linea de comandos
- Salidas reproducibles y faciles de testear

## Scripts MVP

- `research_score.py`: rankea ideas con matriz de mercado GO/NO_GO.
- `build_infoproduct.py`: crea infoproducto 5/10 paginas + prompts de imagen.
- `nano_banana_generate.py`: genera imagenes por lote con Gemini/Nano Banana.
- `build_infoproduct_marketing.py`: genera copy marketero final por pagina.
- `render_infoproduct_html.py`: maquetacion visual HTML con color, bloques y CTA.
- `export_infoproduct_pdf.py`: exporta markdown a PDF simple.
- `build_nano_prompts_pro.py`: crea prompts avanzados para imagen con consistencia de serie.
- `render_infoproduct_pdf_visual.py`: crea PDF visual con diseño por pagina sin depender de navegador.

## Ejemplos

- `examples/research_ideas.sample.json`
- `examples/infoproduct_brief.sample.json`
