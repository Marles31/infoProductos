---
name: investigacion-mercado-lite
description: Investigar y validar oportunidades de infoproducto con evidencia de mercado y scoring GO/NO_GO. Usar cuando el usuario da un tema y necesita identificar que idea tiene mayor potencial de compra antes de redactar o generar imagenes.
---

# Investigacion Mercado Lite

## Objetivo

Convertir un tema en 2 a 5 ideas evaluables y seleccionar la mejor idea con criterios medibles.

## Flujo minimo

1. Definir `tema` y `audiencia`.
2. Recolectar evidencia de mercado en fuentes abiertas (problemas repetidos, lenguaje de compra, objeciones).
3. Construir `.tmp/research_ideas.json` con la estructura de `tools/examples/research_ideas.sample.json`.
4. Ejecutar:

```powershell
python tools/research_score.py `
  --input .tmp/research_ideas.json `
  --output .tmp/research_scored.json `
  --markdown-out .tmp/research_scored.md `
  --threshold 75
```

5. Escoger la idea top con `decision = GO`.

## Criterios de senales (0-10)

- `demand`
- `purchase_intent`
- `competition_gap`
- `differentiation`
- `execution_ease`

## Salida obligatoria

- Idea ganadora (titulo + score)
- Top 3 dolores
- Top 3 resultados deseados
- Top 3 objeciones
- 2 a 3 pruebas de credibilidad

## Regla de costo

Priorizar investigacion web/manual gratuita y sintetizar en JSON compacto.
