# Bloque MCU: pasivos sin ficha propia (SPEC-0028)

Consulta de JLCPCB: **2026-11-16**, con `herramientas/kicad/jlc.py`. Campos de los símbolos de la hoja en `campos-mcu.csv`. Datasheet de cada pieza: la URL de la columna `Datasheet` de esa tabla (PDF del fabricante en LCSC). El módulo ESP32-S3, el USB-C, el pulsador y las demás piezas del bloque tienen ficha propia (`ESP32-S3-WROOM-1.md`, `TYPE-C-31-M-12.md`, `TS-1187A-B-A-B.md`, `USBLC6-2SC6.md`, `B-2100S04P-A110.md`, `KT-0603R.md`). Fuente de la lista: `docs/diseno/mcu.md` §10.

| Refs. | MPN | Fabricante | LCSC | Tipo · stock (2026-11-16) | Función |
|---|---|---|---|---|---|
| R24, R25 | 0603WAF4701T5E | UNI-ROYAL | C23162 | Basic · 14 679 061 | *Pull-ups* del I²C de la placa, 4,7 kΩ 1 % 0603 |
| R18, R19 | 0603WAF5101T5E | UNI-ROYAL | C23186 | Basic · 19 106 444 | CC1/CC2 del USB-C, 5,1 kΩ 1 % 0603 |
| R20, R21 | 0603WAF220JT5E | UNI-ROYAL | C23345 | Basic · 5 161 314 | Serie en D+/D−, 22 Ω 1 % 0603 |
| C24 | CL21A226MAQNNNE | Samsung Electro-Mechanics | C45783 | Basic · 3 965 666 | Desacoplo de 3V3 del módulo, 22 µF 25 V X5R 0805 |
