---
id: SPEC-0031
titulo: Bloque de conectores, expansión y pulsadores
fase: 3
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0031-bloque-conectores
requisitos: [EXP-02, EXP-03, AMB-03, FAB-07, KIC-02]
depende_de: [SPEC-0006, SPEC-0030]
creada: 2026-11-13
cerrada:
validacion:
---

# SPEC-0031 · Bloque de conectores, expansión y pulsadores

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

El bloque de conectores de la v2 queda completo: conector de expansión, pulsadores manuales y taladros en `hardware/v2/conectores.kicad_sch`, unida a la raíz, con ERC 0 y paridad 0.

## Alcance

- Incluye:
  - `docs/diseno/conectores.md`: conector de expansión EXP-02 tal como lo define `docs/diseno/viabilidad-expansion.md` §10 para la arquitectura 1, I²C con TCA9535 + ADS1115 (D9, DEC-0012): pines, TPS2553 de 5 V y 3,3 V con sus EN y FAULT (§10.6), ESD, *pull-ups* en el lado del conector y restricciones de layout (§10.7);
  - `docs/diseno/mcu.md` y hoja MCU, con la lista de §10.6: GPIO36 de EXP_IO2 a EXP_EN (salida con *pull-down* de 100 kΩ), EXP_EN en §10.1, §10.2 y Anexo B (REL-04 en el módulo), y §14.2 cerrada;
  - 6 pulsadores (EXP-03): comparación, con coste, de una escalera de resistencias en un canal de ADC1 frente a un expansor I²C en el bus de la placa; quedan libres GPIO10, 18, 37 y 39 (DEC-0011);
  - longitud de cada borde con los taladros M3 (FAB-07) y restricciones de layout, con la fila de pulsadores en el centro;
  - `docs/diseno/mcu.md` §9 y hoja MCU: `PULSE_IN` (GPIO37) libre y pines de los pulsadores;
  - restos de EXP-01 y de la entrada de pulsos fuera de `docs/02`, retirados en la v0.6 (lista de SPEC-0030, 2026-11-13):
    - `docs/diseno/mcu.md`: cabecera (requisitos), resumen (GPIO, «3 libres» pasa a 4), §2 (GPIO35–37 «se usan»), §9.2 «deja 3 libres para EXP-02», trazabilidad de MCU-05 («GPIO35–37 en uso»), pendientes («más 3 pines libres»), tabla §9.2 (fila de GPIO37 y lista de libres), restricciones de layout (fila de `PULSE_IN`), trazabilidad (fila de EXP-01), ESPHome (`pulse_counter` en GPIO37) y tabla de etiquetas jerárquicas y sus formas;
    - `docs/diseno/estudio-salidas.md`: resumen S6, §4 (borde inferior con EXP-01) y su nota *Vigente*: aviso que remite a la longitud de bordes de `conectores.md`;
    - `hardware/componentes/ESP32-S3-WROOM-1.md`: «GPIO35–37 en uso» pasa a GPIO35–36 (la conclusión sobre R8 y R16V no cambia);
    - `hardware/v2/mcu.kicad_sch` (etiqueta jerárquica `PULSE_IN`), `esp-riego.kicad_sch` (pin de hoja `PULSE_IN` y texto del esqueleto, «EXP-01 … EXP-04»), `esp-riego.kicad_pcb` (red `/MCU/PULSE_IN`, al sincronizar) y `conectores.kicad_sch` (comentario 1 del cajetín y los dos textos del bloque pendiente);
    - `hardware/v2/README.md`: fila `Conectores` («Entrada de pulsos», EXP-01 … EXP-04).
  - piezas, hoja, raíz, campos, stock y fichas; PCB sincronizada con las huellas sin colocar.
- Excluye: el diseño del módulo de expansión; colocación y rutado (fase 4).

## Entradas

- `docs/diseno/viabilidad-expansion.md` §10 entera (tipo, pines, alimentación, *pull-ups*, ESD, lista de piezas con las conexiones de EN y FAULT y los cambios para `mcu.md`, restricciones de layout) y §12 (riesgos 3, 5 y 6).
- `gestion/decisiones/DEC-0011-*.md` (decisiones 1 y 2, consecuencia «GPIO») y `DEC-0012-*.md` (consecuencias); DEC-0013, cuando exista (lectura de los pulsadores).
- `docs/02-especificaciones-v2.md` (v0.6): EXP-02, EXP-03, EXP-04, AMB-03, FAB-07, FAB-08 y KIC-02; REL-04, REL-08 y FW-04 por el estado seguro y el manual; la fila «Pulsadores manuales» de la tabla de pruebas.
- `docs/diseno/mcu.md`: §2, §9.1 (criterios: GPIO18 con H↑, GPIO39 con WPU, ADC1 solo en GPIO1–10), §9.2 (tabla y lista de libres), §10.1, §10.2, §11 (SW1/SW2 como referencia del pulsador), §12, §13, §14.2, Anexo B y Anexo C.
- `hardware/componentes/TS-1187A-B-A-B.md` (pulsador de SW1/SW2, Basic, huella propia con 3D) y `USBLC6-2SC6.md`; datasheets locales de `hardware/componentes/datasheets/` (los del TPS2553, el BH254V-10P y las piezas nuevas los deja ahí el paso 3).
- `herramientas/kicad/README.md` (herramientas, formatos y límites; `hoja.py` no toca los pines de hoja de la raíz ni admite símbolos de varias unidades).
- Checklists `gestion/checklists/esquema.md` y `gestion/checklists/librerias.md`.
- Modelo de bloque cerrado: `docs/diseno/sensores.md` (estructura y anexo de etiquetas) y `hardware/componentes/campos-sensores.csv`.
- `hardware/v2/README.md`: pines de la raíz con no conexión provisional (`I2C_EXP_SDA`, `I2C_EXP_SCL`, `EXP_INT`, `EXP_IO2` y `PULSE_IN`, que esta spec quita).
- Referencias libres: J10, U14, R69, C48 y SW3 en adelante (las mayores en uso son J9, U13, R68, C47 y SW2).
- Punto de partida (`main` en `0b1ff5c`): `verificar.py hardware/v2` da ERC 0, DRC 0 con 358 sin conectar, paridad 0, y FALLA solo en `librerias.fichas` y `librerias.gitattributes` (SPEC-0028).

## Entregables

- Paso 1, `ing-diseno` (solo documento): `docs/diseno/conectores.md` con la comparación de la lectura de los 6 pulsadores con GPIO10, 18, 37 y 39 (al menos escalera de resistencias en un canal de ADC1 y expansor I²C en el bus de la placa; por opción: piezas con LCSC, coste por placa con 5 y 10 uds, tipo Basic o Extended, dirección I²C sin choque si aplica, comportamiento con dos pulsaciones a la vez y soporte en ESPHome) y su recomendación; parte `gestion/logs/SPEC-0031/01-ing-diseno.md`.
- Paso 2, coordinador: `gestion/decisiones/DEC-0013-*.md` con la elección del usuario.
- Paso 3, `jr-conformidad`: `hardware/componentes/campos-conectores.csv` (filas de §10.6 de `viabilidad-expansion.md` con las referencias definitivas, más los 6 pulsadores y las piezas de la opción de DEC-0013), `hardware/componentes/stock-conectores.csv`, una ficha por cada código LCSC sin ficha (plantilla `componente.md`), con su datasheet en `hardware/componentes/datasheets/` si es un circuito integrado o un conector, y parte `02-jr-conformidad.md`.
- Paso 4, `ing-diseno` (la instancia del paso 1): `conectores.md` completo (EXP-02 de §10 con las referencias definitivas, pulsadores según DEC-0013, longitud de cada borde con los taladros M3, restricciones de layout en formato de fila de `restricciones.csv`, trazabilidad y anexo de etiquetas); `mcu.md` con los cambios de §10.6 y los restos de EXP-01 del alcance; los otros restos de EXP-01 (`estudio-salidas.md`, `ESP32-S3-WROOM-1.md`, `hardware/v2/README.md`); `hardware/v2/conectores.kicad_sch`, `mcu.kicad_sch` y `esp-riego.kicad_sch`; `esp-riego.kicad_pcb` sincronizada; piezas nuevas en `hardware/libraries/` si no valen las oficiales; parte `03-ing-diseno.md`, que cuenta los scripts escritos en la carpeta temporal y los usos de `herramientas/kicad/`.
- Paso 5, `ing-validacion`: `gestion/informes/VAL-0031-01.md`.

## Criterios de aceptación

- [ ] Cada pieza, valor, huella y pin de la hoja coinciden con `conectores.md` y con su datasheet: J10 (BH254V-10P, numeración 1–10 de §10.2 con la huella `Connector_IDC` contrastada con la p. 1), TPS2553 (IN, OUT, GND, EN, FAULT, ILIM), USBLC6-2SC6 (I/O1, I/O2, VBUS) y las piezas de los pulsadores.
- [ ] EN de los dos TPS2553 unido a su IN; los dos FAULT y el *pull-up* de 10 kΩ en EXP_INT, en el lado del MCU de la de 470 Ω; *pull-ups* de 2,2 kΩ a +3V3_EXP en el lado del conector de las de 100 Ω; R_ILIM 68 kΩ y 220 kΩ.
- [ ] `EXP_EN` (GPIO36) con su *pull-down* de 100 kΩ a GND en el lado del MCU de la de 470 Ω; `mcu.md` §9.2, §10.1, §10.2, Anexo B y §14.2 cerrada según §10.6, y la hoja MCU con la etiqueta `EXP_EN` en lugar de `EXP_IO2`.
- [ ] Los 6 pulsadores llegan a los GPIO que fija `mcu.md` §9.2 según DEC-0013, sin usar pines fuera de GPIO10, 18, 37 y 39, y cumpliendo los criterios de §9.1 (GPIO18 solo entrada, GPIO39 con WPU, ADC solo en ADC1).
- [ ] `PULSE_IN` no queda en ninguna hoja ni en la PCB, y ninguno de los restos de EXP-01 del alcance sigue en los archivos citados.
- [ ] `verificar.py hardware/v2`: ERC 0, DRC 0 errores, paridad 0, y ningún punto `[auto]` nuevo en FALLA. Los «sin conectar» suben solo por las huellas nuevas, y el parte da la cifra.
- [ ] `campos.py revisar hardware/v2`: 0 diferencias con `campos-conectores.csv`; cada código LCSC nuevo tiene ficha y fila de stock.
- [ ] En la raíz, los pines de expansión de la hoja MCU llegan a la hoja de conectores y no les queda ninguna no conexión provisional; ningún pin de hoja sin unir.
- [ ] `conectores.md` justifica la longitud de cada borde con los taladros M3 (FAB-07) y da las restricciones de §10.7 y de la fila de pulsadores en el centro, sin colocar ni rutar nada.

## Plan de validación

Nivel **completo**. Se reproduce de forma independiente: el mapeo de pines de J10, de los TPS2553 y de los USBLC6 frente a sus datasheets, y su conexión en la netlist exportada (EN–IN, FAULT y *pull-up* en EXP_INT, lado de cada *pull-up* y *pull-down* respecto a su resistencia en serie); la unión de la raíz con GPIO35, 36, 47 y 48 y con los GPIO de los pulsadores; la lectura de los pulsadores de DEC-0013 (valores de la escalera y umbrales del ADC con tolerancias, o dirección I²C del expansor sin choque con el SHT4x); las R_ILIM frente a las ecuaciones de la p. 17 del TPS2553; y la ausencia de `PULSE_IN` y de los restos de EXP-01. Por muestreo: filas de `campos-conectores.csv` y de `stock-conectores.csv` frente a LCSC, dos fichas nuevas y la longitud de un borde.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-13 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-13 | coordinador | Añade la lista de restos de EXP-01 y `PULSE_IN` | SPEC-0030 · DEC-0011 |  |  |  |
| 2026-11-15 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-15 | ing-diseno | conectores.md §1, comparación de la lectura de los 6 pulsadores | 01-ing-diseno | 156011 | 22 | 12 |
