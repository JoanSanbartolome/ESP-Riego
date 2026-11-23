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

Paso 5 (2026-11-20): 0 obligatorias en 23 iteraciones con antena y J2 al ras (`colocacion-b3.csv`). Lo que ahorró trabajo:
- Generador `scratchpad\p5\gen5.py` + `plan.py` (put/mover/CANAL por bloque, añadiendo iteraciones al final) y `ev.sh N [r]` con `OMIT=serigrafia` (`evaluar --omitir`) hasta tener 0 obligatorias; `referencias --todas` solo al final.
- Cobre térmico: cada BTT necesita ≈ 26 mm de paso con su vecino; con 6 BTT + U1 + U2 + U4 + Q1, +20 % no cabe en 100 × 100 (+10 % sí). U4 solo cabe en el centro (anillo de 10 mm). C1 a ≤ 8 mm de U1 cae en su anillo.
- Referencias: filas de 0603 con paso ≥ 3,25 mm (texto encima/debajo) o columnas con hueco ≥ 1,8 mm; bloques de 4 × 4 con paso 3,6 × 3,27.

Paso 6 (2026-11-20): b4 en 10 iteraciones (J10 horizontal). Lo que ahorró trabajo:
- Para cambiar una huella en la copia: editar `Footprint`/`Value`/`LCSC Part#` en la hoja de la copia (Python en binario) y `sincronizar.py` (la recarga con la red intacta). Después, `extraer` otra vez para `mapa.py`.
- `scratchpad\p6\caja.py h.txt tabla.csv x0 y0 x1 y1`: cajas de patio en placa de una zona (giro como KiCad: 90 → (y, −x)). Más rápido que el mapa para huecos de décimas.
- Anillo de U1: solo admite ≈ 68 mm² ocupados (D3, C6, JP1 ya llenan 58): R2/C4 dentro, el resto fuera. D2 entre U1 y Q1 cabe si queda fuera de y > patio de U1 + 8,66.
- Cambiar una regla que usan las pruebas (B04/B07) rompe `Colocacion` y `ColocacionPaso5`: dejar parche con reglas filtradas.
