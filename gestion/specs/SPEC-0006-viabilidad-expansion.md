---
id: SPEC-0006
titulo: Viabilidad del módulo de expansión de canales
fase: 2
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0006-viabilidad-expansion
requisitos: [EXP-02, EXP-04]
depende_de: [SPEC-0004, SPEC-0005, SPEC-0030]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0006 · Viabilidad del módulo de expansión de canales

> Propuesta. Va después de SPEC-0030 y antes de SPEC-0031: entrega el informe y, con él, la definición del conector EXP-02; el usuario decide D9 con el informe (DEC-0011).

## Objetivo

Un informe de viabilidad, con investigación a fondo, sobre cómo ampliar el número de canales con un módulo de expansión. Para cada arquitectura: componentes, costes y lo que la placa principal debe reservar en su conector de expansión. Con el informe se fija el conector EXP-02 y el usuario decide D9 (DEC-0011).

## Alcance

- Incluye, como mínimo, estas arquitecturas:
  1. Expansor de GPIO por I²C (p. ej. PCA9555/TCA9555, MCP23017, PCF8574), con extensor de bus para cables largos (p. ej. P82B715, PCA9615).
  2. Bus RS-485 / Modbus RTU con esclavos propios (MCU pequeño y transceptor) o módulos comerciales.
  3. Registros de desplazamiento encadenados (p. ej. 74HC595, TPIC6B595).
  4. Segundo nodo ESP32 independiente por Wi-Fi o ESP-NOW con ESPHome.
  5. CAN, como referencia.
- Para cada una:
  - distancia y cableado (conductores, apantallado);
  - número máximo de módulos y canales, y direccionamiento;
  - alimentación de los módulos (24 V DC compartida, 5 V o local);
  - estado seguro si se corta el bus;
  - alimentación de las salidas del módulo: el bus limitado de la placa (ALI-13) apenas tiene margen sobre su carga instalada (ALI-12), así que el módulo lleva su propio limitador o su propia alimentación; su consumo por el 5 V de la placa cuenta en los ≤ 0,2 A de la lógica (VAL-0007-01-07, VAL-0011-01-06);
  - soporte en ESPHome (`pca9554`, `mcp23017`, `modbus_controller`…);
  - BOM y coste de un módulo de 6 u 8 canales en cantidades de 5 y 10, incluido el montaje en JLCPCB;
  - comparación con módulos comerciales equivalentes;
  - complejidad de firmware y de puesta en marcha.
- Incluye la definición del conector EXP-02 (DEC-0011), que admite la arquitectura recomendada y la alternativa:
  - **pines**, a partir de lo que ya reserva la hoja MCU (`mcu.md` §9.2): I²C de expansión propio, separado del bus del SHT4x (GPIO47 SDA y GPIO48 SCL, *pull-ups* de 2,2 kΩ provisionales), `EXP_INT` (GPIO35, entrada de interrupción) y `EXP_IO2` (GPIO36, E/S), más GND. Si pide otro pin, sale de los libres (GPIO10, 18, 37 y 39, con las restricciones de `mcu.md` §9.1) y deja los que necesitan los 6 pulsadores de EXP-03 (SPEC-0031), o lo justifica;
  - **tensiones**: 3,3 V ≤ 50 mA y 5 V ≤ 0,30 A (`alimentacion.md` §4), que ya cuentan en los ≤ 0,2 A de la lógica (ALI-12). Si propone llevar 24 V por el conector, dice de qué nodo sale (no del bus limitado, ALI-13), con qué protección y su efecto en ALI-12;
  - **tipo**: familia, paso, número de polos, THT o SMD, polarización y bloqueo, con referencia LCSC y stock; va en el borde inferior junto a la entrada y los bornes de salida (FAB-07);
  - **ESD**: protección de cada línea que sale de la placa (pieza, tensión de trabajo, capacidad frente al tiempo de subida del I²C con el cable propuesto y nivel IEC 61000-4-2), *pull-ups* definitivos y, si hace falta, extensor de bus y en qué lado va.
- Excluye: diseñar el módulo en KiCad; la hoja de conectores y las piezas en el esquema (SPEC-0031).

## Entradas

- `docs/02-especificaciones-v2.md` v0.6 (EXP-02 … EXP-04, REL, ALI-12, ALI-13, FAB-07) y `gestion/decisiones/DEC-0011-sin-pulsos-pulsadores-conector-y-valvulas.md`.
- `docs/diseno/mcu.md` §9 (GPIO reservados y libres) y `docs/diseno/alimentacion.md` §4 (3,3 V y 5 V de la expansión).
- `docs/diseno/estudio-salidas.md` (SPEC-0005) y `gestion/decisiones/DEC-0003-salidas-high-side-y-limitador.md` (D8: BTT6050-1ERA con limitador común), porque el módulo debería repetir la etapa de salida elegida.

## Entregables

- `docs/diseno/viabilidad-expansion.md`:
  - resumen para decidir;
  - una sección por arquitectura;
  - tabla de costes con fuentes y fecha de consulta;
  - recomendación;
  - definición del conector EXP-02: tabla de pines (señal, GPIO, tensión, corriente, ESD), tipo con referencia LCSC y stock, lista para que SPEC-0031 la pase a `conectores.md` y a la hoja.
- Parte `gestion/logs/SPEC-0006/01-ing-diseno.md`.

## Criterios de aceptación

- [ ] Las 5 arquitecturas se analizan con los mismos criterios.
- [ ] Cada coste tiene fuente, fecha y cantidad.
- [ ] La definición del conector EXP-02 admite al menos la arquitectura recomendada y la alternativa.
- [ ] Los pines del conector coinciden con `mcu.md` §9.2 o cada cambio está justificado, y dejan pines para los pulsadores de EXP-03 o justifican el expansor.
- [ ] Las corrientes de 3,3 V y 5 V no superan las de `alimentacion.md` §4, o el informe propone el cambio de ALI-12 como pendiente para el usuario.
- [ ] Cada pieza de ESD y el conector tienen datasheet citado (página) y referencia LCSC con stock y fecha.

## Plan de validación

Nivel **completo**: el conector y su ESD van al esquema y al cobre (DEC-0005).

- Reproducir de forma independiente: la tabla de pines frente a `mcu.md` §9.1-9.2 (restricciones de arranque, ADC1, pines libres); el presupuesto de 3,3 V y 5 V frente a `alimentacion.md` §4 y ALI-12; los parámetros de la pieza de ESD y del conector en su datasheet (tensión de trabajo, capacidad frente al tiempo de subida del I²C con el cable y los *pull-ups* propuestos).
- Comprobar que la arquitectura recomendada y la alternativa funcionan con el conector tal como queda (señales, alimentación, estado seguro si se corta el bus).
- Por muestreo: costes (fuente, fecha, cantidad y tramo de precio), stock en LCSC y componentes de ESPHome citados.
- Checklist: `gestion/checklists/requisitos.md`, sección «Estudios de diseño».

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | Añade VAL-0007-01-07 (bus limitado y ALI-12) | VAL-0007-01 |
| 2026-11-05 | coordinador | Actualiza el punto de alimentación de las salidas con VAL-0011-01-06 | VAL-0011-01 |
| 2026-11-11 | coordinador | Responsable: ing-diseno; se completa con el ciclo nuevo al abrirla | DEC-0009 |  |  |  |
| 2026-11-13 | coordinador | Añade la definición del conector EXP-02 y el plan de validación | SPEC-0030 · DEC-0011 |  |  |  |
