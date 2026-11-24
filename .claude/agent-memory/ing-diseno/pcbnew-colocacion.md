---
name: pcbnew-colocacion
description: API de pcbnew de KiCad 10 que costó encontrar y método para iterar la colocación en texto con colocacion.py
metadata:
  type: reference
---

- pcbnew de KiCad 10: `GetBoardPolygonOutlines(poly, False)` (el 2.º argumento es obligatorio), `SHAPE_POLY_SET.BooleanIntersection/Subtract(otro)` sin modo, `Area()` en nm², `pad.GetFPRelativePosition()` sin girar y `fp.BuildCourtyardCaches()` tras mover; las ventanas de pasta de un EP son pads sin número. Por qué: se encontraron probando una a una. Fuente: SPEC-0037; `herramientas/kicad/colocacion.py`.
- `fp.GetSheetname()` devuelve la ruta de nombres (`/Salidas/Canal1/`), no el nombre de la hoja. Por qué: no sirve como nombre de hoja. Fuente: SPEC-0037.
- Tinta de un texto: `TransformTextToPolySet(poly, 0, FromMM(0.01), ERROR_INSIDE)` y `poly.BBox()`, porque `GetBoundingBox()` lleva ≈ 0,25 mm de relleno; `Inflate(int, CORNER_STRATEGY_ROUND_ALL_CORNERS, maxError)` y `GetSolderMaskExpansion(F_Mask)` piden esos argumentos. Por qué: con la caja del texto salían solapes de serigrafía falsos. Fuente: SPEC-0037 paso 3.
- Girar una huella gira también su referencia (ángulo absoluto): `SetTextAngleDegrees` va después del giro. Por qué: el ángulo del texto es absoluto. Fuente: SPEC-0037 paso 3.
- En informes que se prueban con ida y vuelta (`colocar.py --exportar` redondea a 4 decimales), se redondea antes de comparar y se recorre en orden fijo. Por qué: los empates cambiaban entre ejecuciones. Fuente: SPEC-0037 paso 3.
- En `docs/diseno/colocacion-reglas.csv`, una nota con `; ` parte la fila: se usan comas. Por qué: el separador es `;`. Fuente: SPEC-0037.
- Huellas sin girar: la entrada del cable del WJ500V mira a −Y y la boca del USB-C HRO a +Y. Por qué: decide el giro en el borde. Fuente: SPEC-0037.
- Al iterar la colocación en texto: primero solapes y cobre con `evaluar --omitir serigrafia` y sin `referencias` (5 s), y `referencias --todas` solo al final (≈ 55 s). Por qué: cada iteración baja a segundos. Fuente: SPEC-0037 pasos 4 y 5.
- Referencias sin ambigüedad: ≥ 1,55 mm libres a un lado de la pieza (0,15 + 1,0 + 0,4); filas de 0603 con paso ≥ 3,25 mm (3,6 con giro 0 y el texto debajo) o columnas con hueco ≥ 1,8 mm. Por qué: es lo que pide la regla `ambigua` con texto de 1,0 mm. Fuente: SPEC-0037 pasos 4 y 5.
- Si `referencias` no encuentra hueco, se fijan `rx,ry` de las conflictivas en la tabla y se coloca el resto alrededor. Por qué: la pasada automática no siempre lo resuelve. Fuente: SPEC-0037 paso 4.
