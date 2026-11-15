---
spec: SPEC-0031
agente: jr-conformidad
n: 02
fecha: 2026-11-15
estado: completado
---

# SPEC-0031 · 02 · jr-conformidad

## Hecho

- `hardware/componentes/campos-conectores.csv`: 18 filas (J10, U14–U18, R69–R79, C48–C52, SW3–SW8) con las referencias definitivas; Value y Datasheet iguales a los de las mismas piezas de otras hojas.
- `hardware/componentes/stock-conectores.csv`: 21 códigos del 2026-11-15, con tipo, stock y precio a 10 uds. Incluye las alternativas de §10.6 (C4355000, C13612, C22913), C2873588, C17230 y C783615. Los 21 tienen stock.
- Fichas nuevas: `BH254V-10P.md`, `TPS2553.md`, `TCA9554PWR.md` y la ficha de bloque `bloque-conectores.md` (pasivos, C19666, C2873588, y remite a las fichas de USBLC6-2SC6 y TS-1187A-B-A-B).
- Datasheets en `hardware/componentes/datasheets/`: `BH254V-10P.pdf` (copia de JLCPCB, una hoja), `TPS2553.pdf` y `TCA9554PWR.pdf` (ti.com).
- C19666 (hoy FALLA en `librerias.fichas`) queda cubierto por `bloque-conectores.md`; comprobado con `fuentes_fichas` de `comprobar.py` que los 15 códigos de la tabla tienen ficha con tipo, fecha y datasheet.

## Decisiones y desviaciones

- Todos los códigos coinciden con su MPN y fabricante según la API de JLCPCB. Sin cambios de compra (DEC-0007): no hay principal sin stock ni equivalente Basic con distinto tipo.
- J10: la hoja de datos (p. 1) no numera los pines (solo marca el pin 1 con un triángulo). Cotas contrastadas con `IDC-Header_2x05_P2.54mm_Vertical`: A = 10,16, taladro Ø 1,02 ± 0,05 (huella 1,0), cuerpo 20,35 ± 0,40 frente a patio de 21,36.
- Esquema no tocado, según el encargo; `campos.py revisar` solo dice que la tabla no está aún en la hoja.

## Verificación

No aplica `verificar.py` (no se ha tocado ningún proyecto KiCad).

## Para validación

- TPS2553 (SLVS841G, oct. 2026): pinout p. 4 (IN 1, GND 2, EN 3, FAULT 4, ILIM 5, OUT 6), ecuaciones de I_OS en la **p. 16** (la SPEC dice p. 17). R_ILIM 68 kΩ da 347/388/435 mA y 220 kΩ da 105/123/144 mA (mín/nom/máx), antes de la tolerancia de la resistencia.
- TCA9554 (SCPS233E): pinout p. 4, dirección p. 19, pull-up interno p. 16.

## Pendiente

- Corrección del coordinador: DEC-0013 corregida; quitadas R79–R84 de `campos-conectores.csv` y `bloque-conectores.md`; R85 pasa a R79 (pull-up de INT). `stock-conectores.csv` no cita referencias (sin cambios).
- (Resuelto) **Contradicción con DEC-0013 y `conectores.md` §1.3:** el TCA9554PWR sí tiene pull-up interno de 100 kΩ por E/S (TI p. 16 y p. 24: «no hace falta pull-up externo»). R79–R84 no son necesarias; con ellas el pull-up efectivo es ≈ 9,1 kΩ y es inocuo. Decidir si se quitan (−6 resistencias, ≈ 0,01 $) o se dejan; la tabla las lleva, como ordena DEC-0013.
- **TPS2553: no hay símbolo oficial** en KiCad 10.0.6 (ni TPS2553 ni TPS2552): `ing-diseno` lo crea en `hardware/libraries` (huella `SOT-23-6` y 3D oficiales sí existen). Sí hay `Interface_Expansion:TCA9554PW` y `Connector_Generic:Conn_02x05_Odd_Even`.
- Los `.step` oficiales de J10, TCA9554 y SOT-23-6 existen en `3dmodels` de KiCad 10.0.6 (comprobado). Stock del respaldo C2873588: 1 545 uds, Extended, como C477924 (5 455).
