---
mpn: TYPE-C-31-M-12
fabricante: Korean Hroparts Elec (HRO)
funcion: conector USB-C 2.0 de 16 pines, montaje SMT con pestañas de carcasa (MCU-03)
lcsc: C165948
tipo_jlcpcb: extended
stock_consultado: 2026-11-07
datasheet: https://www.lcsc.com/datasheet/lcsc_datasheet_2205251630_Korean-Hroparts-Elec-TYPE-C-31-M-12_C165948.pdf
datasheet_local: datasheets/TYPE-C-31-M-12.pdf (1 hoja, 0,1 MB). Sin PDF propio localizado: hroparts.com no responde desde este equipo (2026-11-05); LCSC es la única fuente
simbolo: Connector:USB_C_Receptacle_USB2.0_16P
huella: esp-riego:USB_C_Receptacle_HRO_TYPE-C-31-M-12 (copia de Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12; solo cambia la ruta del 3D)
modelo_3d: ${KIPRJMOD}/../libraries/3d/USB_C_Receptacle_HRO_TYPE-C-31-M-12.step (el oficial falta en 10.0.6; la huella esp-riego lo enlaza)
origen_assets: kicad-oficial
verificado_por:
---

# TYPE-C-31-M-12 · USB-C 2.0 16P

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Corriente / tensión | 5 A / 20 V | Dibujo, nota 4-1 (hoja única) |
| Durabilidad | 10 000 ciclos | Dibujo, nota 3-3 |
| Fuerza de inserción / extracción | 0,5–2,0 kgf / 0,8–2,0 kgf | Dibujo, notas 3-1 y 3-2 |
| Temperatura de funcionamiento | −30…+80 °C | Dibujo, nota 5 |
| *Reflow* | 260 °C durante 10 s como máximo | Dibujo, nota 6 |
| Dimensiones | 8,94 × 7,35 mm (alto 3,26 mm); *layout* de PCB recomendado con 16 contactos a 0,5/0,8 mm y 4 agujeros de carcasa | Dibujo, vistas superior y *layout* |

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| A1, A12, B1, B12 | GND | Masa |
| A4, A9, B4, B9 | VBUS | 5 V del bus |
| A5 / B5 | CC1 / CC2 | Configuración (5,1 kΩ a masa en el dispositivo, MCU-03) |
| A6, B6 | D+ (DP1/DP2) | Datos; las dos orientaciones se unen en la placa |
| A7, B7 | D− (DN1/DN2) | Datos; las dos orientaciones se unen en la placa |
| A8 / B8 | SBU1 / SBU2 | Banda lateral (sin uso en USB 2.0) |
| SH | SHIELD | Carcasa (pad `SH` de la huella) |

## Recomendaciones de layout del fabricante

- Usar el *layout* de PCB recomendado del dibujo (tolerancia ± 0,05 mm): la huella oficial está dibujada sobre él.
- Pares D+/D− cortos y simétricos, con la protección USBLC6-2SC6 junto al conector.
- Carcasa a masa por sus cuatro pestañas.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| TYPE-C-31-M-12A | C5337088 | Variante A de HRO; stock 2 533; confirmar la huella antes de usarla |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-07)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas | 10 placas |
|---|---|---|---|---|---|
| C165948 | Extended | 321 343 | 1–49: 0,1870 · 50–149: 0,1476 (precios de 2026-11-06 y 2026-11-05) | 0,93 $ | 1,87 $ |

## Nota sobre el modelo 3D

La instalación local de KiCad 10.0.6 no incluye el `.step` que la huella oficial referencia, y tampoco el repositorio oficial `kicad-packages3D` (rama `master` y rama `10.0`, comprobado el 2026-11-05 con el listado de la API de GitLab: la carpeta `Connector_USB.3dshapes` no contiene ningún HRO). El archivo de respaldo es el mismo modelo que KiCad distribuye en sus demos (`demos/royalblue54L_feather`), copiado a `hardware/libraries/3d/`. La huella `esp-riego:USB_C_Receptacle_HRO_TYPE-C-31-M-12` (SPEC-0021) ya lo enlaza con `${KIPRJMOD}`; render de comprobación en `hardware/libraries/3d/fuentes-solidcraft/render_SPEC-0021_top.png`.

## Uso en el proyecto

MCU-03 (`mcu.kicad_sch` o `conectores.kicad_sch` de la v2).
