---
id: SPEC-0007
titulo: Requisitos v0.3: D8 y observaciones de VAL-0004-02
fase: 0
estado: propuesta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0007-requisitos-v03
requisitos: [ALI-03, ALI-04, ALI-09, ALI-12, REL-03, REL-05, REL-08, AMB-02, FAB-03, FAB-07, FAB-08]
depende_de: [SPEC-0004, SPEC-0005]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0007 · Requisitos v0.3: D8 y observaciones de VAL-0004-02

> Propuesta: se abre cuando el usuario decida D8 (tecnología de las salidas) a partir del estudio de SPEC-0005. Reúne en una sola ronda la decisión y las observaciones de VAL-0004-02.

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la v0.3: refleja la decisión D8 (y D2 si se decide a la vez) en una DEC nueva y resuelve las observaciones de VAL-0004-02.

## Alcance

- Incluye:
  - DEC-0003 con D8 (y D2): tecnología de las salidas para las válvulas instaladas de 24 V DC (≈ 0,2 A).
  - Ajustar REL-03, REL-05, REL-08, FAB-07 y FAB-08 según la opción elegida (§7.3 del estudio).
  - Observaciones de VAL-0004-02:
    - **01:** posición de la TVS respecto a la protección de polaridad (ALI-03, ALI-04, §6).
    - **02:** cómo se impone el límite de 4 A de ALI-12 y la prueba de sobrecarga del conjunto.
    - **04:** ALI-03 en §9.
    - **05:** VRWM frente a la OVP de la fuente, y puntos de aviso de ALI-09 en §6.
    - **06:** la prueba térmica con al menos dos canales a la corriente de REL-05.
    - **07:** la corrección de T/HR válida en reposo y con carga.
    - **08:** clase de red del común de las salidas (FAB-03).
    - **09:** presupuesto de longitud de los bordes (FAB-07, FAB-08).
    - **10:** detalles de redacción y versiones de las checklists.
  - Las propuestas de VAL-0004-02 para las checklists de requisitos (v2), esquema y layout.
- Excluye: el módulo de expansión (SPEC-0006).

## Entradas

- `gestion/informes/VAL-0004-02.md`.
- `docs/diseno/estudio-salidas.md` (SPEC-0005) y su validación.
- Decisión del usuario sobre D8 y, si lo da, el modelo de la fuente de 24 V (para el hallazgo 05).

## Entregables

- `gestion/decisiones/DEC-0003-*.md`, `docs/02` v0.3 y las checklists actualizadas.

## Criterios de aceptación

- [ ] Las observaciones 01, 02 y 04–10 de VAL-0004-02 están resueltas o justificadas una a una.
- [ ] D8 está registrada en DEC-0003 y llega a requisitos vigentes.
- [ ] La checklist de requisitos vigente se cumple.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
