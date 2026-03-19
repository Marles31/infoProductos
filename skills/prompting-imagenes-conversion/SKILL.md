---
name: prompting-imagenes-conversion
description: Construir prompts de imagen de alta calidad para infoproductos comerciales, con estructura cinematica, consistencia visual entre paginas y control de composicion, iluminacion, paleta y estilo. Usar cuando se necesiten imagenes que vendan y no resultados genericos.
---

# Prompting Imagenes Conversion

## Objetivo

Generar prompts que produzcan imagenes coherentes, atractivas y orientadas a conversion.

## Estructura obligatoria del prompt

1. Sujeto principal (quien/que)
2. Escena y contexto (donde/accion)
3. Composicion (encuadre, plano, foco)
4. Iluminacion (tipo de luz y contraste)
5. Paleta y textura (mood visual)
6. Estilo (fotografico/ilustracion/3D/etc.)
7. Restricciones (sin logos, sin texto largo, sin marcas de agua)

## Regla de consistencia

- Definir un `style anchor` global para toda la serie.
- Mantener lente/iluminacion/paleta coherentes entre paginas.
- Variar solo sujeto y accion por pagina.

## Regla anti-generico

Rechazar prompts del tipo:
- "Escena cinematografica de X..."

Usar prompts con detalles concretos de:
- angulo
- profundidad
- texturas
- atmosfera
- objetos clave

## Flujo recomendado

1. Crear copy final por pagina.
2. Construir prompts con `tools/build_nano_prompts_pro.py`.
3. Validar consistencia de serie.
4. Generar imagenes.
