---
spec: SPEC-0037
agente: ing-diseno
n: 06
fecha: 2026-11-20
estado: completado
---

# SPEC-0037 · 06 · ing-diseno (paso 5: reglas nuevas y recolocación)

## Hecho

- `colocacion.py`: tipos `ras`, `rieles` (panel y precio con Z01), `lazo`, `largo`, `pasillo`, `corte` (capacidad de los pasillos: rodea las piezas, sale gratis por el patio propio) y `margen`; `--detalle` con lo que ocupa cada anillo; `cifra` (299.6/300); `referencias` con vuelta atrás (`--sin-vuelta`); `evaluar --omitir`; zona de U5 dentro de la placa en el informe. README al día.
- `colocacion-reglas.csv` (119): A01/B12 `ras` (U5/antena y J2 a 0–0,5 mm, HDG §1.4.7 p. 30 y Fig. 26 p. 31; tolerancia del fresado ±0,2 de JLCPCB), A06 `sale`, A03 reescrita (esquina: ≤ 23,5 mm), F03 sin J2, W01–W08 (lazos de U1, Q1 y del buck), U01/U02 (USB ≤ 40 mm, mcu.md §12), N01 (≥ 1 mm entre bloques), N02 (pasillos, tramos de 15 mm), Q13/Q14 (margen), R01 (rieles, con URL y fecha).
- `docs/diseno/colocacion-b3.csv` (100 × 100) y `colocacion-b3.png`. 23 iteraciones en texto, una imagen al final. Ida y vuelta con `colocar.py` sobre copia: mismo resultado.
- Parche de la batería (clase `ColocacionPaso5` y control de `Colocacion` con J2 y la antena al ras): `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\ad4da10c-a29b-4ee4-bc81-7ee404e64af6\scratchpad\p5\prueba\test_kicad.patch` (`patch --binary`; archivo entero en `…\p5\prueba\test_kicad.py`). Batería entera con el parche, en un repositorio falso: 68/68 (≈ 19 min). `hardware/v2` sin cambios, sin MCP.

## PUNTOS

Partida `colocacion-b2.csv` con las reglas nuevas: 46 101 (41 obligatorias). It. 3: 84 605 · it. 8: 27 273 · it. 13: 6154 (0 obligatorias sin serigrafía) · it. 23: **6557, 0 obligatorias**, 61 objetivos, longitud 4570.

## Decisiones y desviaciones

- Margen del cobre: +20 % no cabe en 100 × 100 (los BTT de abajo se quedan en 300–320 de 360). Queda Q13 = +10 % (U1, U4, Q1, BTT) y Q14 = +5 % (U2, cuyo anillo tiene que contener L1, C7, C8, C22, C11 y C12). Mínimos: U11 332/330, U2 319/315.
- W01 a 10 mm (no 8): con 8 mm, C1 caía dentro del anillo de U1.
- Plano: U5 arriba a la izquierda (zona dentro de la placa 298 mm², antes 1008), J2 bajo la zona, SHT40 en el mismo borde bajo J2 (S02/S04, objetivos), LDO en el centro, buck a su derecha, U1/Q1/F1 en el lateral derecho.
- N02 ajustada en la iteración: tramos de 10 → 15 mm, rodeo de piezas y huecos < 1 mm cerrados (b2 sigue dando 2 focos).

## Objetivos que quedan (61)

O11 12, C02 6, E05 6, F02 6, P02 5, O10 3, E01 3 y otros 20 de una incidencia (lista en `evaluar --detalle`). Visibles en la imagen: D2 (TVS) a 27 mm de Q1 (E02) y C46 junto al grupo de arriba (O13): cerca de Q1 o de U10–U12 les quitan el cobre.
No se comprueba en texto: rutado real (N02 es una estimación en línea recta, sin la cara inferior), altura e isla del SHT40, caja (D5), legibilidad real y los valores de F.Fab solapados.

## Pendiente

- Coordinador/usuario: aceptar el margen de +10 % / +5 % en lugar de +20 % (o placa mayor).
- Usuario: J2 y U5 al ras piden rieles; el panel de 110 × 100 no tiene tarifa publicada (R01): presupuesto en JLCPCB y si bastan rieles en los bordes superior e inferior.
- Otra spec: la zona de la huella de U5 deja 15 mm a los dos lados; la Fig. 26 pide ≤ 2 mm del lado del punto de alimentación y recortar la placa alrededor de la antena (D5).
- Coordinador: aplicar el parche de la batería.
