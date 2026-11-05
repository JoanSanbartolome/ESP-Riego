---
mpn: TLV1117LV33DCYR
fabricante: Texas Instruments
funcion: LDO de 3,3 V y 1 A, entrada de 2 a 5,5 V; raíl +3V3 (U4)
lcsc: C15578 (alternativa JSMSEMI TLV1117LV33DCYR, C48937499)
tipo_jlcpcb: extended
stock_consultado: 2026-11-05 (TI 1 606 · JSMSEMI 76 870)
datasheet: https://www.ti.com/lit/ds/symlink/tlv1117lv.pdf
datasheet_local: datasheets/TLV1117LV.pdf (SBVS160C, enero de 2023)
simbolo: Regulator_Linear:TLV1117-33 (hereda LT1117-2.85: 1 GND, 2 VO, 3 VI)
huella: Package_TO_SOT_SMD:SOT-223-3_TabPin2
modelo_3d: ${KICAD10_3DMODEL_DIR}/Package_TO_SOT_SMD.3dshapes/SOT-223.step
origen_assets: kicad-oficial
verificado_por:
---

# TLV1117LV · LDO 3,3 V / 1 A

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Entrada | 2…5,5 V (máximo absoluto 6 V) | p. 1 |
| Corriente | 1 A; límite mínimo 1,1 A | p. 1 |
| Precisión | ± 1,5 % típ. (más línea ≤ 5 mV y carga ≤ 35 mV) | pp. 1 y 5 |
| Caída | 230 mV típ. a 500 mA; 700 mV máx. a 1 A | p. 5 |
| R_θJA | 62,9 °C/W (JEDEC) | p. 4 |
| C de salida | 1 µF cerámico; capacitancia **efectiva** (tensión, temperatura, envejecimiento) > 0,5 µF | §8.2.2.1 (p. 13) |
| C de entrada | no necesario; 0,1…1 µF recomendado | §8.2.2.1 (p. 13) |

## Pinout (DCY, SOT-223; Tabla 5-1, p. 3)

| Pin | Nombre | Función |
|---|---|---|
| 1 | GND | Masa |
| 2 y pestaña | OUT | Salida |
| 3 | IN | Entrada |

El símbolo `TLV1117-33` (pines 1 GND, 2 VO, 3 VI) y la huella `SOT-223-3_TabPin2` (pads 1, 2, 3 y pestaña unida al 2) coinciden. El símbolo oficial apunta al datasheet del TLV1117 (no LV) y no trae huella: ambos campos se rellenan en el esquema.

## Recomendaciones de layout del fabricante

- Condensadores lo más cerca posible de los pines; masa del condensador de salida directa al pin GND; sin electrolíticos (§10, p. 14).
- Pestaña a cobre para disipar (el diseño pide ≥ 4 cm² y vías: `docs/diseno/alimentacion.md` §8).

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| TLV1117LV33DCYR (JSMSEMI) | C48937499 | Otro fabricante, sin datasheet en la API de JLCPCB; verificar antes de usarla |

## Uso en el proyecto

U4: +5V → +3V3 (ALI-07).
