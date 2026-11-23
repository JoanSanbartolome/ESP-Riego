---
mpn: SMBJ33A
fabricante: Zhuhai Hongjiacheng (marca «R+O» en LCSC; serie SMBJ). Antes Littelfuse C224019 (DEC-0018 P1, SPEC-0038)
funcion: TVS unidireccional de 600 W en la entrada de potencia (ALI-04, DEC-0004)
lcsc: C19077586 (alternativa Littelfuse SMBJ33A, C224019)
tipo_jlcpcb: extended
stock_consultado: 2026-11-23 (JLCPCB 49 715; Extended preferida; 0,0504 $ a 1 ud.; jlc.py)
datasheet: https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2312280935_hongjiacheng-SMBJ33A_C19077586.pdf (Hongjiacheng SMBJ series, Rev. 2.1; sin URL del fabricante)
datasheet_local: datasheets/SMBJ33A-HJC.pdf (C19077586, 5 pp., descargado de JLCPCB el 2026-11-23)
datasheet_alternativa: https://www.littelfuse.com/assets/littelfuse/products/pdf/smbj.pdf (Littelfuse, C224019)
datasheet_local_alternativa: datasheets/SMBJ33A.pdf (serie SMBJ, revisión de 07/04/25, 0,9 MB, copia de LCSC). Revisión vigente: confirmado por el usuario (2026-11-05) que se usa esta copia (07/04/25); littelfuse.com devuelve 403 desde el equipo de conformidad, así que no se ha contrastado con la web de Littelfuse
simbolo: esp-riego:SMBJ33A (propio, unidireccional; copia de la forma de Diode:SM6T33A con pines K=1 y A=2; Device:D_TVS es bidireccional y no vale)
huella: Diode_SMD:D_SMB
modelo_3d: ${KICAD10_3DMODEL_DIR}/Diode_SMD.3dshapes/D_SMB.step
origen_assets: símbolo propio (basado en Diode:SM6T33A); huella y 3D kicad-oficial
verificado_por:
---

# SMBJ33A · TVS de entrada

## Datos clave

Pieza montada: Hongjiacheng C19077586 (`SMBJ33A-HJC.pdf`). Última columna: la pieza anterior, Littelfuse C224019 (`SMBJ33A.pdf`), para comparar (VAL-0037-01-09).

| Parámetro | Hongjiacheng C19077586 | Fuente (página) | Littelfuse C224019 (p.) |
|---|---|---|---|
| Potencia de pico (10/1000 µs) | 600 W | p. 1 | 600 W (p. 1) |
| Tensión de trabajo V_WM (*stand-off*) | 33 V | Tabla de la p. 3 | 33 V (p. 2) |
| Tensión de ruptura V_BR | 36,7 V mín. / 40,6 V máx. | Tabla de la p. 3 | 36,7 / 40,6 V a 1 mA (p. 2) |
| Tensión de *clamping* V_C | 53,3 V a I_PP = 11,26 A | Tabla de la p. 3 | 53,3 V a 11,3 A (p. 2) |
| Fuga I_R a V_WM | **5 µA máx.** | Tabla de la p. 3 | 1 µA (p. 2) |
| T_J | −55…150 °C | p. 1 | — |
| Polaridad | unidireccional (sufijo A); banda en el cátodo | p. 1 | igual |

Diferencia: solo la fuga, 5 µA frente a 1 µA a 33 V (≤ 0,2 mW). V_C es la misma, así que ALI-05 (≥ 60 V en el nodo) no cambia.

La V_C = 53,3 V fija la tensión mínima de todo el nodo de entrada (ALI-05: ≥ 60 V). Con V_BR mínima de 36,7 V el TVS no conduce hasta bien por encima de la tensión de entrada máxima prevista (ver ALI-04 y DEC-0004).

## Pinout (DO-214AA / SMB)

| Pin | Nombre | Función |
|---|---|---|
| 1 | K | Cátodo (a la entrada positiva; banda en el encapsulado) |
| 2 | A | Ánodo (a masa) |

## Recomendaciones de layout del fabricante

- Datos de soldadura y *land pattern* en la p. 5 (la huella `D_SMB` es genérica de KiCad).
- TVS lo más cerca posible del conector de entrada, con pistas cortas y anchas hacia masa: la corriente de pulso de 11,3 A hace que la inductancia de la pista sume a V_C.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| SMBJ33A (Littelfuse; antes la principal) | C224019 | Extended, 21 329 uds, 0,1419 $ a 1 ud. (2026-11-23); I_R 1 µA |
| SMBJ33A (Brightking) | C78419 | 0,0736 $ a 1 ud; stock 3 887 |
| SMBJ33A (Ruilon) | C10219 | 0,0944 $; stock 12 041 |
| SMBJ33A-TR (ST) | C133662 | 0,2169 $; stock 8 295 |

## Aprovisionamiento (JLCPCB, consulta 2026-11-23, `jlc.py`)

| Código | Tipo | Stock | Precio unitario por tramo (USD) |
|---|---|---|---|
| C19077586 (Hongjiacheng) | Extended (preferida: sin cargo de pieza extendida) | 49 715 | 1–99: 0,0504 · 100–299: 0,0405 |
| C224019 (Littelfuse, alternativa) | Extended | 21 329 | 1: 0,1419 |

## Uso en el proyecto

ALI-04 y DEC-0004: protección de sobretensión de la entrada (`alimentacion.kicad_sch`).
