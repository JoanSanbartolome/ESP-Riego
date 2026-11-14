---
id: SPEC-0030
titulo: Requisitos v0.6
fase: 3
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0030-requisitos-v06
requisitos: [EXP-01, EXP-02, EXP-03, EXP-04, FAB-07, REL-03]
depende_de: []
creada: 2026-11-13
cerrada:
validacion:
---

# SPEC-0030 · Requisitos v0.6

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la v0.6 con las decisiones de DEC-0011, sin referencias rotas en el resto de documentos.

## Alcance

- Incluye:
  - EXP-01 pasa a «Requisitos retirados»: fuera del diagrama de §3, de FAB-07 y de la prueba o la trazabilidad que lo citen; D3 cerrada;
  - EXP-03 redefinido: 6 pulsadores en la placa, uno por salida, en fila en el centro, leídos por el firmware con antirrebote; prioridad de C a S (propuesta del coordinador, aceptada por el usuario el 2026-11-13); D4 cerrada;
  - EXP-02 y EXP-04: el conector se fija con el informe de SPEC-0006; completar el alcance de SPEC-0006 con la definición del conector;
  - §1 y REL-03: las válvulas instaladas son bobinas de 24 V AC alimentadas en continua, con la medida pendiente (DEC-0011);
  - historial v0.6 y lista, con Grep, de lo que queda por cambiar en `docs/diseno/` y en el esquema (`PULSE_IN`, «pulsos», «lluvia»), que hace SPEC-0031.
- Excluye: `docs/diseno/` y el esquema; cambiar las cifras de REL-05 o de ALI-12 antes de medir la válvula.

## Entradas

- `gestion/decisiones/DEC-0011-sin-pulsos-pulsadores-conector-y-valvulas.md` entera.
- `docs/02-especificaciones-v2.md` (v0.5) entero.
- `docs/diseno/mcu.md` §9.2 (GPIO reservados a la expansión y `PULSE_IN`) y `docs/diseno/alimentacion.md` §4 (3,3 V y 5 V de la expansión).
- `gestion/specs/SPEC-0006-viabilidad-expansion.md` y `gestion/specs/SPEC-0031-bloque-conectores.md`.
- `gestion/checklists/requisitos.md` (v5).

## Entregables

- `docs/02-especificaciones-v2.md` v0.6.
- `gestion/specs/SPEC-0006-viabilidad-expansion.md`: definición del conector EXP-02 en el alcance y «Plan de validación».
- `gestion/specs/SPEC-0031-bloque-conectores.md`: lista de lo que queda por cambiar fuera de `docs/02` (`PULSE_IN`, EXP-01, «pulsos», «lluvia»).

## Criterios de aceptación

- [ ] EXP-01 figura en §9 con versión, DEC-0011, motivo y texto anterior, y no aparece como vigente en §3, §4, FAB-07, §6 ni §8.
- [ ] EXP-03 dice 6 pulsadores en la placa, uno por salida, en fila en el centro, leídos por el firmware con antirrebote y sin actuar directamente sobre la salida; el cambio de prioridad C → S figura como aceptado por el usuario (DEC-0011).
- [ ] EXP-02 y EXP-04 fijan el conector con el informe de SPEC-0006, y D9 lo decide el usuario con ese informe.
- [ ] D3 y D4 cerradas en §7 con DEC-0011; D9 coherente con EXP-02 y EXP-04.
- [ ] §1, §2, §6 y REL-03 dicen que las válvulas instaladas son de 24 V AC (Bermad S-390-3-D) alimentadas en continua, con la corriente en continua pendiente de medir; las cifras de REL-05, ALI-12 y ALI-13 no cambian.
- [ ] La cabecera cita DEC-0011, como las versiones anteriores citan su DEC; §9 (redefiniciones de la v0.6) y §10 citan SPEC-0030 y DEC-0011.
- [ ] SPEC-0006 define en su alcance los pines, tensiones, tipo y ESD del conector a partir de `mcu.md` §9.2 y `alimentacion.md` §4, y tiene «Plan de validación».
- [ ] SPEC-0031 lista, con ruta, cada aparición pendiente fuera de `docs/02`; `docs/diseno/` y `hardware/` sin cambios.
- [ ] `gestion.py trazabilidad` sin avisos.

## Plan de validación

Nivel **ligero** (texto de requisitos; DEC-0005), con `gestion/checklists/requisitos.md` v5.

- Reproducir de forma independiente: la búsqueda de EXP-01, «pulsos», «lluvia», `PULSE_IN` y «24 V DC» referido a las válvulas en `docs/`, `gestion/` (specs propuestas, checklists), `CLAUDE.md`, `.claude/agents/` y `.claude/agent-memory/`, y comprobar que cada aparición fuera de `docs/02` está en la lista de SPEC-0031 o es histórica (specs cerradas, informes, decisiones).
- Comparar las tablas de §4 de la v0.5 y la v0.6: cada ID cuyo texto o prioridad cambia está en `requisitos` y en el historial.
- Cada punto de DEC-0011 («Decisión» y «Consecuencias» que tocan requisitos) llega a docs/02, a SPEC-0006 o a SPEC-0031.
- Por muestreo: las cifras de REL-05, ALI-12 y ALI-13 iguales a las de la v0.5; pines y tensiones del conector en SPEC-0006 iguales a los de `mcu.md` §9.2 y `alimentacion.md` §4.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-13 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-13 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-14 | ing-validacion | VAL-0030-01 RECHAZADO (3 M, 2 B) | VAL-0030-01 | 119792 | 24 | 1395 |
| 2026-11-14 | ing-validacion | VAL-0030-02 APROBADO_CON_OBSERVACIONES (1 B) | VAL-0030-02 |  | 28 | 1398 |
