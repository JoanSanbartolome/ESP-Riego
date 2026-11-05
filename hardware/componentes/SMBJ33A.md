---
mpn: SMBJ33A
fabricante: Littelfuse (serie SMBJ; varios fabricantes en LCSC)
funcion: TVS unidireccional de 600 W en la entrada de potencia (ALI-04, DEC-0004)
lcsc: C224019
tipo_jlcpcb: extended
stock_consultado: 2026-11-05
datasheet: https://www.littelfuse.com/assets/littelfuse/products/pdf/smbj.pdf
datasheet_espejo: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Littelfuse-SMBJ33A_C224019.pdf
datasheet_local: datasheets/SMBJ33A.pdf (serie SMBJ, revisión de 07/04/25, 0,9 MB, copia de LCSC). Revisión vigente: confirmado por el usuario (2026-11-05) que se usa esta copia (07/04/25); littelfuse.com devuelve 403 desde el equipo de conformidad, así que no se ha contrastado con la web de Littelfuse
simbolo: esp-riego:SMBJ33A (propio, unidireccional; copia de la forma de Diode:SM6T33A con pines K=1 y A=2; Device:D_TVS es bidireccional y no vale)
huella: Diode_SMD:D_SMB
modelo_3d: ${KICAD10_3DMODEL_DIR}/Diode_SMD.3dshapes/D_SMB.step
origen_assets: símbolo propio (basado en Diode:SM6T33A); huella y 3D kicad-oficial
verificado_por:
---

# SMBJ33A · TVS de entrada

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Potencia de pico (10/1000 µs) | 600 W | p. 1 |
| Tensión de trabajo V_WM (*stand-off*) | 33 V | Tabla de la p. 2 |
| Tensión de ruptura V_BR | 36,7 V mín. / 40,6 V máx. a 1 mA | Tabla de la p. 2 |
| Tensión de *clamping* V_C | 53,3 V a I_PP = 11,3 A | Tabla de la p. 2 |
| Fuga I_R a V_WM | 1 µA máx. | Tabla de la p. 2 |
| Polaridad | unidireccional (sufijo A) | p. 1 |

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
| SMBJ33A (Brightking) | C78419 | 0,0736 $ a 1 ud; stock 3 887 |
| SMBJ33A (Ruilon) | C10219 | 0,0944 $; stock 12 041 |
| SMBJ33A-TR (ST) | C133662 | 0,2169 $; stock 8 295 |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-05)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas | 10 placas |
|---|---|---|---|---|---|
| C224019 (Littelfuse) | Extended | 9 752 | 1–49: 0,1229 · 50–149: 0,0998 | 0,61 $ | 1,23 $ |

## Uso en el proyecto

ALI-04 y DEC-0004: protección de sobretensión de la entrada (`alimentacion.kicad_sch`).
