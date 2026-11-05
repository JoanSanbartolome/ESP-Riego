---
id: SPEC-0006
titulo: Viabilidad del módulo de expansión de canales
fase: 2
estado: propuesta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0006-viabilidad-expansion
requisitos: [EXP-02, EXP-04]
depende_de: [SPEC-0004, SPEC-0005]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0006 · Viabilidad del módulo de expansión de canales

> Propuesta: el usuario la pedirá más adelante. Debe estar cerrada antes de fijar el conector de expansión (EXP-02) en el esquema de la fase 3.

## Objetivo

Un informe de viabilidad, con investigación a fondo, sobre cómo ampliar el número de canales con un módulo de expansión. Para cada arquitectura: componentes, costes y lo que la placa principal debe reservar en su conector de expansión (decisión D9).

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
  - soporte en ESPHome (`pca9554`, `mcp23017`, `modbus_controller`…);
  - BOM y coste de un módulo de 6 u 8 canales en cantidades de 5 y 10, incluido el montaje en JLCPCB;
  - comparación con módulos comerciales equivalentes;
  - complejidad de firmware y de puesta en marcha.
- Excluye: diseñar el módulo en KiCad.

## Entradas

- `docs/02-especificaciones-v2.md` (EXP-01 … EXP-04, REL, ALI).
- `docs/diseno/estudio-salidas.md` (SPEC-0005) y `gestion/decisiones/DEC-0003-salidas-high-side-y-limitador.md` (D8: BTT6050-1ERA con limitador común), porque el módulo debería repetir la etapa de salida elegida.

## Entregables

- `docs/diseno/viabilidad-expansion.md`:
  - resumen para decidir;
  - una sección por arquitectura;
  - tabla de costes con fuentes y fecha de consulta;
  - recomendación;
  - especificación propuesta del conector EXP-02 (pines, tensiones, ESD).
- Log `gestion/logs/SPEC-0006/01-ing-esquematicos.md`.

## Criterios de aceptación

- [ ] Las 5 arquitecturas se analizan con los mismos criterios.
- [ ] Cada coste tiene fuente, fecha y cantidad.
- [ ] La propuesta del conector EXP-02 admite al menos la arquitectura recomendada y la alternativa.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
