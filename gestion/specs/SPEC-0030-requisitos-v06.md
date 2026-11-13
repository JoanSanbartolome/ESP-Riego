---
id: SPEC-0030
titulo: Requisitos v0.6
fase: 3
estado: propuesta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0030-requisitos-v06
requisitos: [EXP-01, EXP-02, EXP-03, EXP-04, FAB-07]
depende_de: []
creada: 2026-11-13
cerrada:
validacion:
---

# SPEC-0030 · Requisitos v0.6

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

> Propuesta: entradas, entregables, criterios y plan de validación (ligero) se completan al abrirla.

`docs/02-especificaciones-v2.md` pasa a la v0.6 con las decisiones de DEC-0011, sin referencias rotas en el resto de documentos.

## Alcance

- Incluye:
  - EXP-01 pasa a «Requisitos retirados»: fuera del diagrama de §3, de FAB-07 y de la prueba o la trazabilidad que lo citen; D3 cerrada;
  - EXP-03 redefinido: 6 pulsadores en la placa, uno por salida, en fila en el centro, leídos por el firmware con antirrebote; prioridad de C a S (propuesta del coordinador); D4 cerrada;
  - EXP-02 y EXP-04: el conector se fija con el informe de SPEC-0006; completar el alcance de SPEC-0006 con la definición del conector;
  - §1 y REL-03: las válvulas instaladas son bobinas de 24 V AC alimentadas en continua, con la medida pendiente (DEC-0011);
  - historial v0.6 y lista, con Grep, de lo que queda por cambiar en `docs/diseno/` y en el esquema (`PULSE_IN`, «pulsos», «lluvia»), que hace SPEC-0031.
- Excluye: `docs/diseno/` y el esquema; cambiar las cifras de REL-05 o de ALI-12 antes de medir la válvula.

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
