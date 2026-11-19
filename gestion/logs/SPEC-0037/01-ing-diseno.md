---
spec: SPEC-0037
agente: ing-diseno
n: 01
fecha: 2026-11-19
estado: completado
---

# SPEC-0037 · 01 · ing-diseno

## Hecho

- `herramientas/kicad/colocacion.py`: `extraer` (huellas en texto por bloque; `--refs` añade los pads) y `evaluar` (tabla de `colocar.py` → informe de ≤ 30 líneas con `PUNTOS`; código 1 si queda algo obligatorio; `--detalle`). Fila en `herramientas/kicad/README.md`, con el formato de las reglas y los límites.
- `herramientas/kicad/colocar.py`: el bucle de colocación pasa a `aplicar(board, filas)`, sin cambio de comportamiento. `evaluar` lo usa, así que mide lo mismo que dejaría `colocar.py`.
- `docs/diseno/colocacion-reglas.csv`: 65 reglas (33 obligatorias y 32 objetivos) y 4 clases de red, cada una con su origen.
- Parche de la batería (clase `Colocacion` con 5 casos; `colocacion` en `HERRAMIENTAS` y en `test_no_modifican_lo_que_leen`): `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\ad4da10c-a29b-4ee4-bc81-7ee404e64af6\scratchpad\s37\test_kicad.patch`. El archivo entero, en CRLF, está en `…\s37\test_kicad.py`.

## Tamaños sobre la PCB actual (197 huellas)

| Salida | Líneas | Caracteres | Tokens (estimación) | caracteres / 4 |
|---|---|---|---|---|
| `extraer -o` | 211 | 11 461 | ≈ 6 100 | ≈ 2 900 |
| `evaluar` | 30 | 2 207 | ≈ 1 040 | ≈ 550 |

La estimación es una cota alta: cuenta 4 letras, 3 cifras o un signo por token. `evaluar` tarda menos de 1 s.

## Decisiones y desviaciones

- «Junto a» sin cifra: 5 mm de patio a patio, como `objetivo`. Las cifras que pone la tabla y no el documento (borne a ≤ 1 mm del borde, SHT40 a ≤ 6 mm, franja central del 50 %, «esquina» a 12 mm, 24 y 19 mm desde U13 por la isla sin dibujar) se explican en la columna `nota`.
- Los objetivos del autor de `mcu.md` §3 y `sensores.md` §6.3 van como `objetivo`. El *keepout* de 15 mm al SHT40 de `alimentacion.md` §8 va como obligatorio.
- El patio de U5 incluye la zona de la antena. U5 puede salir del contorno por esa zona (regla G02, `sale`). Los solapes se miden sin la zona; la zona dentro de la placa cuenta aparte, como «zona prohibida».
- Orientación (`hacia`), comprobada con `vista.py placa`: entrada de cable del WJ500V en −Y, ranura de J10 en −X, boca del USB-C en +Y y antena de U5 en −Y.

## Verificación

- Batería entera con el parche en un repositorio falso: 59/59 (236 s). Tras los últimos retoques, `Generales`, `Colocacion` y `Pcb.test_colocar`: 10/10.
- Se detectan los cinco fallos sembrados: solape R17/R18, C24 fuera, R16 en la zona de U5, J4 en el borde inferior (B01, B05) y U13 en el centro (S01). La colocación de control no da ninguno.
- Ida y vuelta con `colocar.py`: deja las 197 posiciones de la tabla y el mismo informe. `hardware/v2` sin cambios; no se usó el MCP.
- Para validación: muestrear las reglas B01–B13, A01–A05 y S01–S05. El consumo real de tokens lo darán la auditoría y el paso 2.
