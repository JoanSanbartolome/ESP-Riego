---
id: SPEC-0004
titulo: Requisitos v0.2: nuevo objetivo, 6 salidas, 24 V DC y T/HR en placa
fase: 0
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0004-requisitos-v02
requisitos: [ALI-01, ALI-02, ALI-04, ALI-05, ALI-06, ALI-08, ALI-09, ALI-11, ALI-12, MCU-02, REL-01, REL-02, REL-03, REL-04, REL-05, REL-06, REL-08, REL-09, AMB-01, AMB-02, AMB-03, EXP-01, EXP-02, EXP-04, FAB-03, FAB-06, FAB-07, FAB-08, FAB-09, FAB-10, KIC-02, KIC-04, FW-03]
depende_de: []
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0004 · Requisitos v0.2: nuevo objetivo, 6 salidas, 24 V DC y T/HR en placa

> El usuario redefine el objetivo de la placa respecto al TFG (2026-11-04). Se registra en DEC-0002. Las siguientes rondas de *features* irán en specs de requisitos nuevas, no en esta.

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la versión v0.2 y refleja el nuevo objetivo:

- instalación en interior, en una caja ventilada a la pared;
- alimentación única desde una fuente de 24 V DC de hasta 5 A (en el primer borrador, transformador de 24 V AC; el usuario lo cambió tras VAL-0004-01);
- 6 salidas con 3 en el borde superior y 3 en el inferior;
- sensor de temperatura y humedad en la placa;
- sin sensor de nivel.

El resto del repositorio queda coherente con esa versión.

## Alcance

- Incluye:
  - `gestion/decisiones/DEC-0002`.
  - `docs/02` v0.2:
    - objetivo, resumen, arquitectura, requisitos ALI/REL/AMB/EXP/FAB/FW, condiciones ambientales, criterios de aceptación y decisiones abiertas;
    - sección de requisitos retirados e historial de versiones.
  - `docs/03`: fases 2 y 4, para quitar el lazo 4–20 mA y adaptar el *floorplan*.
  - Checklists de esquema y de layout, y checklist nueva de requisitos (propuesta de VAL-0004-01).
  - `.claude/agents/ing-layout.md`: las líneas del *floorplan* y de la caja (hallazgo VAL-0004-01-07).
- Excluye:
  - Elegir la tecnología de las salidas (SPEC-0005).
  - Diseñar el módulo de expansión (SPEC-0006).
  - `docs/01`, que describe la v1 tal como es.

## Entradas

- Respuestas del usuario del 2026-11-04 (recogidas en DEC-0002).
- `docs/02-especificaciones-v2.md` v0.1, `docs/03-plan-de-diseno.md`, `gestion/checklists/esquema.md` y `gestion/checklists/layout.md`.

## Entregables

- `gestion/decisiones/DEC-0002-objetivo-v2-revisado.md`.
- `docs/02-especificaciones-v2.md` v0.2.
- `docs/03-plan-de-diseno.md`, `gestion/checklists/esquema.md` y `gestion/checklists/layout.md` actualizados.

## Criterios de aceptación

- [ ] Ningún requisito vigente, criterio de aceptación ni checklist menciona el lazo 4–20 mA, la caja IP65 o 4 canales.
- [ ] Los requisitos retirados aparecen en la tabla de retirados con su motivo y DEC-0002, y no vuelven a usarse sus IDs.
- [ ] Cada cambio del usuario se puede seguir hasta un requisito: 6 salidas, 3+3 bornes, 24 V DC, T/HR en placa, interior ventilado, sin nivel y módulo de expansión.
- [ ] Las decisiones D1–D9 son coherentes con los requisitos (cerradas, pendientes o con la spec que las resuelve).
- [ ] `python herramientas/gestion.py trazabilidad` no da avisos y cuenta los requisitos vigentes.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (abierta) | |
| 2026-11-04 | coordinador | DEC-0002, docs/02 v0.2, docs/03 y checklists de esquema y layout v2 | |
| 2026-11-04 | ing-validacion | VAL-0004-01: RECHAZADO (A 1 · M 6 · B 9) | gestion/informes/VAL-0004-01.md |
| 2026-11-04 | usuario | Fuente de hasta 5 A, 6 salidas a la vez, T/HR de la caseta, corte visto como «no disponible»; quita la entrada de AC: solo fuente de 24 V DC | DEC-0002 |
| 2026-11-04 | coordinador | Rehace la alimentación para 24 V DC y corrige los hallazgos 01–16 de VAL-0004-01 | |
| 2026-11-04 | usuario | Las electroválvulas instaladas son de 24 V DC, ≈ 0,2 A (no de 24 V AC) | DEC-0002 |
