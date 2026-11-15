---
mpn: TCA9554PWR
fabricante: Texas Instruments
funcion: expansor I²C de 8 E/S con salida de interrupción, TSSOP-16: lectura de los 6 pulsadores manuales (U18, DEC-0013)
lcsc: C477924
tipo_jlcpcb: extended
stock_consultado: 2026-11-15
datasheet: https://www.ti.com/lit/ds/symlink/tca9554.pdf
datasheet_local: datasheets/TCA9554PWR.pdf (SCPS233E, revisión de febrero de 2017, 30 pp.; descargada de ti.com el 2026-11-15)
simbolo: Interface_Expansion:TCA9554PW
huella: Package_SO:TSSOP-16_4.4x5mm_P0.65mm
modelo_3d: ${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/TSSOP-16_4.4x5mm_P0.65mm.step
origen_assets: kicad-oficial
verificado_por:
---

# TCA9554PWR · expansor de los pulsadores

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Alimentación | 1,65 a 5,5 V | pp. 1, 5 |
| Bus | 100 kHz (estándar) y 400 kHz (rápido) | p. 1 |
| Dirección | 0100 A2 A1 A0: 0x20 con A2-A0 a GND, hasta 0x27 | p. 19 (Tabla 2) |
| Entradas P0-P7 | Tolerantes a 5 V; arrancan como entradas | pp. 1, 4 |
| **Pull-up interno** | **Débil, de 100 kΩ típ. a VCC en cada E/S; «no hace falta pull-up externo»**; P6 y P7 sin usar llevan el interno | p. 16 (§8.3.1), p. 25 |
| INT | Salida activa baja de drenador abierto; pull-up externo a VCC | pp. 1, 4 |
| SDA y SCL | Pull-up externo a VCC (en la placa, R24 y R25) | p. 4 |

Por eso el proyecto no monta pull-ups externos en los pulsadores (DEC-0013 corregida); solo R79 en INT.

## Pinout (TSSOP-16, PW)

| Pin | Nombre | Función |
|---|---|---|
| 1, 2, 3 | A0, A1, A2 | Dirección; a VCC o a GND directos |
| 4, 5, 6, 7 | P0 a P3 | E/S (P0-P5: SW3-SW8) |
| 8 | GND | Masa |
| 9, 10, 11, 12 | P4 a P7 | E/S |
| 13 | INT | Interrupción, activa baja, drenador abierto |
| 14 | SCL | Reloj |
| 15 | SDA | Datos |
| 16 | VCC | Alimentación (100 nF a GND) |

## Recomendaciones de layout del fabricante

- Prácticas comunes de PCB; sin exigencias de impedancia a estas velocidades (§11.1, p. 29).
- 100 nF entre VCC y GND (C52) junto al pin 16.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| TI PCA9554PWR | C2873588 | Misma huella TSSOP-16 y pinout; VCC 2,3-5,5 V; Extended, 1 545 uds el 2026-11-15, 1,18 $ a 10 uds. Respaldo si el componente `pca9554` de ESPHome no admite el TCA (DEC-0013). Sin ficha propia |
| NXP PCA9554PW,118 | C17230 | Extended, 18 920 uds; datasheet de NXP sin contrastar |
| TI TCA9534PWR | C783615 | Extended, 7 510 uds; misma familia |

## Uso en el proyecto

SPEC-0031: U18 de `conectores.kicad_sch`, en el bus I²C de la placa (GPIO41/42), dirección 0x20, INT a GPIO39 (BTN_INT), SW3-SW8 en P0-P5 (DEC-0013).
