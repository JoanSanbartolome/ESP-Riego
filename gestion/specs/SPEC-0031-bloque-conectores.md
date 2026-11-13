---
id: SPEC-0031
titulo: Bloque de conectores, expansión y pulsadores
fase: 3
estado: propuesta
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

> Propuesta: entradas, entregables, criterios y plan de validación se completan al abrirla, con el informe de SPEC-0006 y la decisión D9.

El bloque de conectores de la v2 queda completo: conector de expansión, pulsadores manuales y taladros en `hardware/v2/conectores.kicad_sch`, unida a la raíz, con ERC 0 y paridad 0.

## Alcance

- Incluye:
  - `docs/diseno/conectores.md`: conector de expansión según SPEC-0006 y D9 (pines, tensiones, ESD y *pull-ups* del I²C de expansión);
  - 6 pulsadores (EXP-03): comparación, con coste, de una escalera de resistencias en un canal de ADC1 frente a un expansor I²C en el bus de la placa; quedan libres GPIO10, 18, 37 y 39 (DEC-0011);
  - longitud de cada borde con los taladros M3 (FAB-07) y restricciones de layout, con la fila de pulsadores en el centro;
  - `docs/diseno/mcu.md` §9 y hoja MCU: `PULSE_IN` (GPIO37) libre y pines de los pulsadores;
  - restos de EXP-01 y de la entrada de pulsos fuera de `docs/02`, retirados en la v0.6 (lista de SPEC-0030, 2026-11-13):
    - `docs/diseno/mcu.md`: cabecera (requisitos), tabla §9.2 (fila de GPIO37 y lista de libres), restricciones de layout (fila de `PULSE_IN`), trazabilidad (fila de EXP-01), ESPHome (`pulse_counter` en GPIO37) y tabla de etiquetas jerárquicas y sus formas;
    - `docs/diseno/estudio-salidas.md`: resumen S6, §4 (borde inferior con EXP-01) y su nota *Vigente*: aviso que remite a la longitud de bordes de `conectores.md`;
    - `hardware/componentes/ESP32-S3-WROOM-1.md`: «GPIO35–37 en uso» pasa a GPIO35–36 (la conclusión sobre R8 y R16V no cambia);
    - `hardware/v2/mcu.kicad_sch` (etiqueta jerárquica `PULSE_IN`), `esp-riego.kicad_sch` (pin de hoja `PULSE_IN` y texto del esqueleto, «EXP-01 … EXP-04»), `esp-riego.kicad_pcb` (red `/MCU/PULSE_IN`, al sincronizar) y `conectores.kicad_sch` (comentario 1 del cajetín y los dos textos del bloque pendiente);
    - `hardware/v2/README.md`: fila `Conectores` («Entrada de pulsos», EXP-01 … EXP-04).
  - piezas, hoja, raíz, campos, stock y fichas; PCB sincronizada con las huellas sin colocar.
- Excluye: el diseño del módulo de expansión; colocación y rutado (fase 4).

## Entradas

<Archivos y secciones concretas que el responsable debe leer. La spec es la orden completa: un agente sin más contexto tiene que poder ejecutarla.>

-

## Entregables

-

## Criterios de aceptación

- [ ]

## Plan de validación

<Nivel (ligero o completo). Qué reproduce validación de forma independiente (lo que tiene riesgo: cotas, mapeo de pines, cálculos con poco margen) y qué comprueba por muestreo (lo mecánico: stock, campos, enlaces).>

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-13 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-13 | coordinador | Añade la lista de restos de EXP-01 y `PULSE_IN` | SPEC-0030 · DEC-0011 |  |  |  |
