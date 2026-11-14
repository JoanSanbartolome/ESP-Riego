---
id: SPEC-0032
titulo: Integración y revisión global del esquema
fase: 3
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0032-integracion-esquema
requisitos: [KIC-02, KIC-03, ALI-12, MCU-05, REL-04, FAB-05]
depende_de: [SPEC-0028, SPEC-0029, SPEC-0031]
creada: 2026-11-13
cerrada:
validacion:
---

# SPEC-0032 · Integración y revisión global del esquema

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

> Propuesta: entradas, entregables, criterios y plan de validación (completo) se completan al abrirla.

El esquema v2 queda cerrado para el layout: raíz completa, ERC 0, campos completos y revisión global hecha. Es la base de la etiqueta `v2.0-sch`.

## Alcance

- Incluye:
  - raíz: todas las hojas unidas, sin no conexiones provisionales;
  - `docs/04-arquitectura.md`: diagrama de bloques, presupuesto de potencia por raíl con todos los bloques (ALI-12) y tabla de GPIO contrastada con la netlist (base de FW-02);
  - revisión global de la fase 3 del plan: pines de arranque, estado de las salidas en el reset, polaridades, ESD en todos los conectores de campo y test points;
  - `docs/diseno/salidas.md` con el dato medido de la válvula instalada (DEC-0011); sin ese dato no se propone la etiqueta; con él, también el aviso de vigencia de la cabecera de `estudio-salidas.md` y la memoria `.claude/agent-memory/ing-diseno/project_salidas_d8.md`, que aún dicen «válvulas de 24 V DC» (VAL-0030-01-04);
  - BOM preliminar con coste y stock (`jr-conformidad`) y PDF del esquema;
  - casillas de las fases 2 y 3 de `docs/03-plan-de-diseno.md` (coordinador).
- Excluye: el layout; la etiqueta `v2.0-sch`, que el coordinador propone al usuario al cerrar.

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
