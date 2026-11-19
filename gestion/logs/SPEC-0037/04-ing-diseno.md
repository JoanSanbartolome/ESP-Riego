---
spec: SPEC-0037
agente: ing-diseno
n: 04
fecha: 2026-11-19
estado: completado
---

# SPEC-0037 · 04 · ing-diseno (paso 3: criterios de DEC-0016)

## Hecho

- `herramientas/kicad/colocacion.py`: tipos de regla nuevos `separacion`, `borde_min`, `cobre_borde`, `serigrafia` (13 comprobaciones), `calor`, `reparto` y `precio`; `!REF` excluye. `evaluar --placa ANCHOxALTO` (o fila `PLACA` en la tabla) cambia el contorno y lleva los M3 con su esquina; líneas nuevas de placa y precio (con `AVISO` por encima de 100 × 100), serigrafía y térmico, y sigue en ≤ 30 líneas. `--detalle` da la clase de red de las reglas, el cobre libre de cada fuente y el precio con su fuente. Orden nueva `referencias`: coloca las referencias (alto 1,0 y trazo 0,18 de las reglas) y escribe `rx,ry,rgiro,ralto,rtrazo`.
- `herramientas/kicad/colocar.py`: columnas opcionales de la referencia, fila `PLACA`, `--placa`, `--con-referencias`; compatible con las tablas de 5 columnas. README de `herramientas/kicad` al día.
- `docs/diseno/colocacion-reglas.csv`: 36 reglas nuevas (101 en total): F01–F04 (JLCPCB y FAB-02), T01–T13 (serigrafía), Q01–Q12 (calor: P y cobre de alimentacion.md §5 y §8 y salidas.md §6), Z01 (precio), D01–D06 (desacoplos de U3, U4 y L1) y L01 (LED). Cada regla de JLCPCB lleva URL, apartado y fechas.
- Parche de la batería (clase `ColocacionCriterios`, 5 casos; `referencias` en `test_no_modifican…`): `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\ad4da10c-a29b-4ee4-bc81-7ee404e64af6\scratchpad\p3\prueba\test_kicad.patch` (archivo entero en CRLF: `…\p3\prueba\test_kicad.py`; se aplica con `patch --binary`).

## Decisiones y desviaciones

- Separación entre piezas: JLCPCB solo pide IPC-7351B densidad media (Términos §2.2), que los patios de KiCad ya cumplen sin solape. F01 (obligatoria, 0,1 mm) y F02 (objetivo, 0,5 mm alrededor de CI y J2) salen de FAB-02 (pista y vía entre pads).
- Borde: Economic pide 0,3 mm (FAQ P14), F03; manda FAB-02 en el cobre (0,5 mm, F04). Los Términos §2.3 piden 2,5 mm sin distinguir Economic: no se aplica (choca con FAB-07).
- Cobre térmico: franja de √A/2 alrededor del patio, sin patios ni zonas, lo compartido a medias. El área de U1 y U2 (300 mm²) es cifra de la tabla: los documentos dan R_θJA 50 °C/W sin área.
- Precio: JLCPCB no publica tarifa por encima de 102 × 102 mm (precio especial; si no, «engineering fee + board fee»). Z01 da 2 $ / 5 uds hasta 100 × 100 (DEC-0016) y, por encima, una incidencia y `AVISO`; el sobrecoste sale de otra fila `precio` con un presupuesto.

## Verificación

- Seis fallos sembrados detectados (F01 R17/R18 0,06 mm, T05 C24/R16, T06 y T07 C25 sobre su pad, T11 R20 a 2,7 mm, Q10 U7/U8 a 1 mm, Z01 con 110 × 70) y ninguno en el control. Batería completa con el parche, en un repositorio falso: 64/64 (428 s).
- `colocacion-b.csv` con las reglas nuevas: 0 solapes, 1075 obligatorias (197 por el trazo de 0,15 de la librería). Con `referencias`: 211 obligatorias (T12 ambiguas 70, T05 38, F01 34, T09 22, cobre de Q01–Q05 10, Q10 4) y 89 objetivos. `referencias`, 30 s; `evaluar`, 5 s.
- Imagen de control (serigrafía tras `referencias`): `…\p3\b_refs.png` y `…\p3\b_refs_zona.png`: los fallos que ve evaluar (filas de pasivos sin hueco, textos pisados) son los de la imagen.
- `hardware/v2` sin cambios; sin MCP. `verificar.py`: no aplica (no se toca ningún proyecto).

## Para validación

- No se ve en texto: legibilidad real (sentido de lectura de las referencias), la serigrafía de FAB-09 (aún no existe), el reparto real del cobre (pistas, otras redes, cara inferior) y si la flecha de F.Fab de los WJ500V cuenta como cuerpo (T09). Muestrear F01, F03, T01–T03, T06 y Z01 frente a sus páginas.

## Pendiente

- Usuario (vía coordinador): la antena de U5 sobresale del borde (MCU-02) y JLCPCB Economic paneliza y fresa a 0,3 mm del borde (FAQ P14); hay que confirmarlo con JLCPCB. Lo mismo con los 2,5 mm de los Términos §2.3.
- Usuario: presupuesto de JLCPCB para los tamaños candidatos por encima de 100 × 100 mm, si el paso 4 los necesita (fila `precio`).
- Coordinador: aplicar el parche; JP1 tiene textos de 0,8 mm en la huella (T04, objetivo): se corrigen en la librería, en otra spec; `checklists/layout.md` l. 46 pide serigrafía ≥ 0,8 mm y JLCPCB, 1,0 mm (T01); l. 44 (fiduciales) no aplica en Economic.
