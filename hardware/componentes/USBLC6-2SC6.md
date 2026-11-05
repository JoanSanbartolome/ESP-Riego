---
mpn: USBLC6-2SC6
fabricante: STMicroelectronics
funcion: protección ESD de 2 líneas de datos USB y de VBUS (MCU-03)
lcsc: C7519
tipo_jlcpcb: extended
stock_consultado: 2026-11-05
datasheet: https://www.st.com/resource/en/datasheet/usblc6-2.pdf
datasheet_local: datasheets/USBLC6-2SC6.pdf (Rev 5, 0,2 MB, copia de LCSC del PDF de ST). Revisión vigente: confirmado por el usuario (2026-11-05) que se usa esta copia (Rev 5); st.com no responde desde el equipo de conformidad, así que no se ha contrastado con la web de ST
simbolo: Power_Protection:USBLC6-2SC6
huella: Package_TO_SOT_SMD:SOT-23-6
modelo_3d: ${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-23-6.step
origen_assets: kicad-oficial
verificado_por:
---

# USBLC6-2SC6 · ESD del USB

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Capacidad I/O–GND | 2,5 típ. / 3,5 pF máx. | Tabla 2, p. 2 |
| Capacidad entre líneas | 1,2 típ. / 1,7 pF máx. | Tabla 2, p. 2 |
| Tensión de ruptura V_BR (VBUS–GND) | ≥ 6 V a 1 mA | Tabla 2, p. 2 |
| Tensión de *clamping* | 17 V a 1 A (8/20 µs) | Tabla 2, p. 2 |
| Fuga | 150 nA máx. | p. 1 |
| Uso | USB 2.0 hasta 480 Mb/s, protege VBUS | p. 1 |

## Pinout (SOT-23-6)

| Pin | Nombre | Función |
|---|---|---|
| 1, 6 | I/O1 | Línea de datos 1 (entrada y salida, en paralelo) |
| 3, 4 | I/O2 | Línea de datos 2 |
| 2 | GND | Masa |
| 5 | VBUS | Alimentación a proteger |

## Recomendaciones de layout del fabricante

- Las pistas entre conector, protección y masa deben ser cortas y anchas; los parásitos de inductancia suben la tensión de *clamping* (Figuras 6 y 7, p. 5).
- La línea de datos pasa por el pin I/O del dispositivo (topología *rail-to-rail*): el TVS va entre el conector y el MCU, sin derivación larga.
- Masa al plano de masa con vías directas.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| USBLC6-2SC6 (UMW) | C2687116 | Clon; 0,0478 $ a 1 ud, stock 101 666; no es ST |
| USBLC6-2SC6 (Tech Public) | C2827654 | Clon; 0,0449 $, stock 93 772 |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-05)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas | 10 placas |
|---|---|---|---|---|---|
| C7519 (ST) | Extended | 46 715 | 1–49: 0,1795 · 50–149: 0,1382 · 150–499: 0,1180 | 0,90 $ | 1,80 $ |

## Uso en el proyecto

MCU-03: entre el USB-C y GPIO19/GPIO20 del MCU.
