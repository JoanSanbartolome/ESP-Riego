---
mpn: ESP32-S3-WROOM-1-N8
fabricante: Espressif Systems
funcion: módulo MCU Wi-Fi 2,4 GHz + BLE, antena PCB. Variante N8 fija (8 MB de flash, sin PSRAM, -40…85 °C); alternativa N16
lcsc: C2913198
tipo_jlcpcb: extended
stock_consultado: 2026-11-06
datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf
datasheet_local: datasheets/ESP32-S3-WROOM-1.pdf (v1.8, 1,3 MB)
simbolo: RF_Module:ESP32-S3-WROOM-1
huella: esp-riego:ESP32-S3-WROOM-1 (copia de RF_Module:ESP32-S3-WROOM-1 con las 12 vías del EPAD a 0,3/0,6 mm, FAB-02)
modelo_3d: ${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-S3-WROOM-1.step
origen_assets: kicad-oficial (huella modificada: vías del EPAD)
verificado_por:
---

# ESP32-S3-WROOM-1 · MCU (MCU-01)

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Variantes con la misma huella | N4, N8, N16 (sin PSRAM); N4R2, N8R2, N16R2 (PSRAM cuádruple 2 MB); N4R8, N8R8, N16R8 (PSRAM octal 8 MB) | Tabla 1-1, p. 3 |
| Alimentación VDD33 | 3,0 / 3,3 / 3,6 V; la fuente debe dar ≥ 0,5 A | Tabla 6-2, p. 27 |
| Temperatura ambiente | −40…85 °C (versión de 85 °C); las versiones R8 y algunas R2, −40…65 °C | Tabla 1-1, p. 3 |
| Antena | PCB integrada; zona de exclusión (*keepout*) en el borde del módulo | §3.1, p. 10 |
| Pines | 41 (40 + EPAD de masa) | §3.2, p. 11 |
| Arranque (*strapping*) | GPIO0 (pull-up débil), GPIO3 (flotante), GPIO45 (pull-down), GPIO46 (pull-down) | §4, p. 13 |
| USB nativo | GPIO19 = USB_D−, GPIO20 = USB_D+ (USB-Serial/JTAG) | Tabla 3-1, p. 11 |
| Con PSRAM octal (R8, R16) | IO35, IO36 e IO37 ocupados por la PSRAM | Tabla 3-1, nota b, p. 12 |
| EN | No dejar flotante; RC recomendado R = 10 kΩ, C = 1 µF | Tabla 3-1, p. 11; §9, p. 41 |

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| 1, 40, 41 | GND | Masa (41 = EPAD) |
| 2 | 3V3 | Alimentación |
| 3 | EN | Habilitación (alto = encendido) |
| 4–7 | IO4–IO7 | GPIO, ADC1_CH3–6, touch |
| 8–11 | IO15–IO18 | GPIO, ADC2 (IO15/IO16 = XTAL_32K) |
| 12 | IO8 | GPIO, ADC1_CH7 |
| 13 / 14 | IO19 / IO20 | GPIO; USB_D− / USB_D+ |
| 15 | IO3 | GPIO, ADC1_CH2, *strapping* (JTAG) |
| 16 | IO46 | GPIO, *strapping* |
| 17–22 | IO9–IO14 | GPIO (ADC1_CH8, ADC1_CH9, ADC2_CH0–3) |
| 23 | IO21 | GPIO |
| 24 / 25 | IO47 / IO48 | GPIO |
| 26 | IO45 | GPIO, *strapping* (VDD_SPI) |
| 27 | IO0 | GPIO, *strapping* (boot) |
| 28–30 | IO35–IO37 | GPIO (no disponibles en R8/R16) |
| 31–35 | IO38–IO42 | GPIO (IO39–IO42 = JTAG MTCK/MTDO/MTDI/MTMS) |
| 36 / 37 | RXD0 / TXD0 | UART0 (GPIO44 / GPIO43) |
| 38 / 39 | IO2 / IO1 | GPIO, ADC1_CH1 / ADC1_CH0 |

Tabla completa en el datasheet, Tabla 3-1 (pp. 11-12). Las restricciones de uso de ADC2 con el Wi-Fi no están en este datasheet: las debe confirmar el bloque MCU en el ESP32-S3 Series Datasheet.

## Recomendaciones de layout del fabricante

- Zona de exclusión de la antena (§3.1, p. 10): sin cobre, pistas ni componentes bajo ni junto a la antena; el módulo va en el borde de la placa con la antena fuera o sobre el borde. Dimensiones de la zona en la Figura 10-1 (p. 42) y en el *land pattern* de la Figura 11-1 (p. 45).
- El EPAD no hay que soldarlo, pero mejora la disipación; con poca pasta, porque el exceso levanta el módulo (§9, p. 41).
- RC en EN (10 kΩ / 1 µF) para un arranque estable (§9, p. 41).
- Desacoplo en 3V3 según el esquema de periféricos de la Figura 9-1 (p. 41).
- Perfil de *reflow*: §12.3, p. 47.

## Variante y restricciones del proyecto

- **Variante fija: N8** (C2913198): 8 MB de flash *quad*, sin PSRAM, −40…85 °C (tabla 1-1, p. 3). Alternativa: N16 (C2913199), misma huella y pines.
- **La placa no admite R8 ni R16V**: GPIO35–37 están en uso (EXP_INT, EXP_IO2, PULSE_IN) y esas variantes los ocupan con la PSRAM octal (tabla 3-1, nota b, p. 12); además solo llegan a 65 °C. N4 no cumple MCU-01.
- **Antena** (`mcu.md` §3; HDG §1.4.7, pp. 28-31, Fig. 24 y 26): módulo en una esquina con la antena sobresaliendo del borde lateral y el punto de alimentación hacia la esquina; si no sobresale, zona libre de 6 mm × ≥ 15 mm recortando la placa. La huella `esp-riego:ESP32-S3-WROOM-1` conserva el *keepout* de 21 × 48 mm en todas las capas de cobre (sin pistas, vías, pads, relleno ni huellas). ≥ 15 mm libres en la caja alrededor de la antena (HDG p. 30).
- **Huella propia (FAB-02):** igual que la oficial salvo el taladro de las 12 vías del EPAD (pad 41): 0,3 mm en vez de 0,2 (pad 0,6, máscara frontal abierta como en la oficial). Se conservan las 12 vías (≥ 9 que pide `mcu.md` §12). Poca pasta en el EPAD (§9, p. 41).

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| ESP32-S3-WROOM-1-N4 | C2913197 | 4 MB de flash (no cumple MCU-01); stock 4 154 (2026-11-06); 4,2629 $ (1–9) |
| ESP32-S3-WROOM-1-N16 | C2913199 | 16 MB de flash; Extended; stock 2 297 (2026-11-06); 4,9603 $ (1–9), 4,4447 $ (10–29) |
| ESP32-S3-WROOM-1U-N8 | no consultado | Conector de antena externa; huella distinta (`RF_Module:ESP32-S3-WROOM-1U`) |

## Aprovisionamiento (API de JLCPCB, consulta 2026-11-06)

| Código | Variante | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas | 10 placas |
|---|---|---|---|---|---|---|
| C2913198 | N8 | Extended | 2 776 | 1–9: 4,9259 · 10–29: 4,2482 · 30–99: 3,8455 | 24,63 $ | 42,48 $ |

(1 módulo por placa. El stock de LCSC era 3 277 el 2026-11-05.)

## Uso en el proyecto

U5 de `mcu.kicad_sch` (v2): MCU-01 y MCU-02. Variante N8 fija (`docs/diseno/mcu.md` §2); IO35–IO37 en uso.
