---
name: prompting-imagenes-conversion
description: Construir prompts de imagen de alta calidad para infoproductos comerciales, con estructura cinematica, consistencia visual entre paginas y control de composicion, iluminacion, paleta y estilo. Usar cuando se necesiten imagenes que vendan y no resultados genericos.
---

# Prompting Imagenes Conversion

## Objetivo

Generar prompts que produzcan imagenes coherentes, atractivas y orientadas a conversion.

## Estructura obligatoria del prompt (orden fijo)

1. `Series style anchor` (identidad visual global)
2. `Page mission` (mensaje de esa pagina)
3. `Subject` (quien/que es protagonista)
4. `Environment` (donde ocurre)
5. `Action` (que esta pasando)
6. `Composition` (encuadre, capas, espacio negativo)
7. `Camera` (lente y angulo)
8. `Lighting`
9. `Color and texture`
10. `Props`
11. `Mood`
12. `Negative constraints`

## Regla de consistencia

- Definir un `style anchor` global para toda la serie.
- Mantener lente, iluminacion y paleta coherentes entre paginas.
- Variar solo sujeto y accion por pagina.

## Regla anti-generico

- Rechazar prompts tipo:
  - "Escena cinematografica de X..."
  - "Imagen epica de X..."
  - "Hazlo profesional..."

Usar prompts con detalles concretos de:
- angulo
- profundidad
- texturas
- atmosfera
- objetos clave

## Plantilla reusable

```text
[SERIES STYLE ANCHOR]
...

[PAGE MISSION]
...

[SUBJECT]
...

[ENVIRONMENT]
...

[ACTION]
...

[COMPOSITION]
...

[CAMERA]
...

[LIGHTING]
...

[COLOR AND TEXTURE]
...

[PROPS]
...

[MOOD]
...

[NEGATIVE CONSTRAINTS]
No logos, no watermark, no embedded text, no UI elements, no cartoon style, no deformed anatomy.
```

## Checklist de calidad (rapido)

- Hay 1 sujeto principal claro.
- Hay accion verificable (verbo concreto).
- Hay 3-5 props que refuerzan la historia.
- Hay instrucciones de encuadre y lente.
- Incluye negativos explicitos.
- El prompt evita texto publicitario dentro de la imagen.

## Flujo recomendado

1. Crear copy final por pagina.
2. Construir prompts con `tools/build_nano_prompts_pro.py`.
3. Validar consistencia de serie.
4. Generar imagenes.
