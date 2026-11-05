# v2 — ESP-Riego (esqueleto de trabajo)

Proyecto KiCad 10 `esp-riego`. Nació como copia de la v1 (`hardware/v1-tfg/`, etiqueta `v1.1-tfg`, SPEC-0013) y en SPEC-0014 se vació: se retiraron todos los circuitos de la v1 que no encajan en los requisitos v0.4 (`docs/02-especificaciones-v2.md`, DEC-0002, DEC-0003 y DEC-0004). El inventario de lo retirado está en `gestion/logs/SPEC-0014/01-ing-esquematicos.md`.

Cajetín: hoja de dibujo `../libraries/ESP-Riego.kicad_wks`, título «ESP-Riego v2», revisión 2.0-dev. `comment 1` lleva la descripción de cada hoja («Placa de control de riego» en la raíz).

## Hojas

| Hoja (`Sheetname` · archivo) | Bloque pendiente | Requisitos | Contenido actual |
|---|---|---|---|
| `Alimentacion` · `alimentacion.kicad_sch` | Entrada, protecciones, limitador común, buck, 3,3 V | ALI-01 … ALI-13 | Texto del bloque pendiente |
| `MCU` · `mcu.kicad_sch` | ESP32-S3-WROOM-1, USB-C, BOOT/RESET, UART | MCU-01 … MCU-07, FW-02 | Texto del bloque pendiente |
| `Salidas` · `salidas.kicad_sch` | 6 *high-side* BTT6050 con diagnóstico y sus bornes | REL-01 … REL-10 | Texto del bloque pendiente |
| `Conectores` · `conectores.kicad_sch` | Entrada de pulsos, expansión, reparto de bornes | EXP-01 … EXP-04, FAB-07, FAB-08 | Texto del bloque pendiente y H1–H4 (taladros M3, FAB-08) |

La hoja `Sensores` (AMB-01 … AMB-03) se añade con el bloque de temperatura y humedad (KIC-02). Las hojas no tienen pines jerárquicos: cada bloque los crea cuando los necesite.

## Cómo se trabaja

Cada bloque llega con su propia spec. La PCB la sincroniza `ing-layout` con el esquema (SPEC-0014, segunda parte: contorno preliminar de 100 × 70 mm y reglas de FAB-02); el layout definitivo se hace cuando el esquema esté estable.

Las librerías están en `../libraries/` (tablas con `${KIPRJMOD}/../libraries/...`). Verificación: `python herramientas/verificar.py hardware/v2`. Tras limpiar el esquema: ERC 0. El DRC y la paridad siguen con incidencias hasta que la PCB se sincronice.
