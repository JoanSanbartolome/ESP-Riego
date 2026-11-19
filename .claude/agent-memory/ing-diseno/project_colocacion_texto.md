---
name: project-colocacion-texto
description: Colocación iterada en texto con colocacion.py (SPEC-0037 brazo B): método que converge en 6 iteraciones, cotas clave de U5 y plano que cumple todas las reglas
metadata:
  type: project
---

Brazo B de SPEC-0037 (2026-11-19): 0 incumplimientos y PUNTOS 373 en 6 iteraciones, unos 17 min. Resultado en `docs/diseno/colocacion-b.csv`.

**Why:** la partida exportada de hardware/v2 tiene 193 huellas fuera del contorno, así que hay que colocarlo todo desde cero. Editar a mano un CSV de 193 filas no es viable.

**How to apply:**
- Escribir un generador en la carpeta temporal con `put/row/col` por bloques (canal = columna bajo su borne) y lanzar `colocacion.py evaluar ... --detalle` en cada iteración. Los solapes se leen en `--detalle`.
- El patio de U5 tiene forma de T: cuerpo ±9,75 × −6,75…13,45 y zona de ±24 × −27,8…−6,75. Con giro 90 en (106,75, 78,5), la línea −6,75 cae en x = 100: la antena queda entera fuera, a 4,0 mm de H3, y cumple A01–A03.
- Giros: bornes de arriba a 0 y de abajo a 180; BTT de arriba a 90 y de abajo a 270 (OUT hacia el borne); J10 a 90; J2 a 270 en el borde izquierdo; Q1 a 270.
- Lo que más sube la puntuación de longitud: las distancias de U5 a U1 y de U5 a J10. En esta placa no compensa rehacer el plano.
- Ver [[reference-trucos-esquema]] para las demás herramientas.

Brazo B' (paso 4, 2026-11-19): 0 obligatorias en 100 × 100 en 25 iteraciones (≈ 50 min), con la antena entera dentro y 2,5 mm a borde. Lo que ahorró trabajo:
- Mapa ASCII de patios (`scratchpad\b2\mapa.py`, 1 × 2 mm) para ver los huecos sin imagen; overrides al final del generador en vez de reescribirlo.
- Primero solapes y cobre (Q01–Q05) sin `referencias` (5 s); `referencias` solo cuando quedan menos de 10 (30 s).
- "Ambiguas": hace falta ≥ 1,55 mm libres en un lado de cada pieza (0,15 + 1,0 + 0,4). Filas de 0603 a giro 0 con un paso de 3,6 y el texto debajo; columnas con un paso de ≥ 3,25.
- Cuando `referencias` (voraz) no encuentra hueco, se fija `rx,ry` de las piezas conflictivas en la tabla y el resto se coloca alrededor.
- Anillo de cobre: un BTT necesita una separación de ≈ 20 mm con su vecino; los BTT junto al borde ganan cobre (la franja de 2,5 mm cuenta).
