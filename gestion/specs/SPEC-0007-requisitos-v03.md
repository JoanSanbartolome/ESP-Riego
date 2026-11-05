---
id: SPEC-0007
titulo: Requisitos v0.3: D8 y observaciones de VAL-0004-02 y VAL-0005-01
fase: 0
estado: cerrada
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0007-requisitos-v03
requisitos: [ALI-04, ALI-09, ALI-12, ALI-13, REL-01, REL-02, REL-03, REL-04, REL-05, REL-08, REL-10, AMB-02, FAB-03, FAB-06, FAB-07, FAB-08]
depende_de: [SPEC-0004, SPEC-0005]
creada: 2026-11-04
cerrada: 2026-11-05
validacion: VAL-0007-01
---

# SPEC-0007 · Requisitos v0.3: D8 y observaciones de VAL-0004-02 y VAL-0005-01

> D8 ya está decidida (BTT6050-1ERA con protección completa; registro de SPEC-0005). Reúne en una sola ronda la decisión y las observaciones de VAL-0004-02 y VAL-0005-01.

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la v0.3: refleja D8, el limitador común y D2 en DEC-0003 y resuelve las observaciones de VAL-0004-02 y VAL-0005-01.

## Alcance

- Incluye:
  - DEC-0003 con D8 (y D2): *high-side* inteligente BTT6050-1ERA por canal, segunda fuente BTT6030-2ERA, reserva BSP752R, para las válvulas instaladas de 24 V DC (≈ 0,2 A).
  - Ajustar REL-03, REL-05, REL-08, ALI-04, FAB-07 y FAB-08 según la opción elegida (§11.5 del estudio), con las correcciones de VAL-0005-01.
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
  - Observaciones de VAL-0005-01:
    - **01 (M):** cortocircuito con la fuente de 5 A. No adoptar «sin fusible por canal» tal cual: limitador común del bus +24V_SAL por debajo de la fuente (resuelve también la 02 de VAL-0004-02), o *hold-up* recalculado desde 18 V hasta el UVLO con un presupuesto de reacción por hardware o interrupción. Distinguir el *hold-up* de la «reserva de energía» de ALI-09.
    - **03:** datos del BTT6030-2ERA como segunda fuente (4 A con los dos canales, k_ILIS 2240).
    - **04:** el límite de 4 A no puede depender solo de la suma de IS (± 25 %).
    - **05:** dejar como requisito del bloque de salidas R_SENSE con *clamp* entre IS y el ADC, y el *pull-up* R_OL de carga abierta con fuga ≤ 1 mA.
    - **06:** REL-03 con la energía de desmagnetización (ec. 5.1) frente a la curva E_AS(I_L), con el máximo de válvulas por canal.
    - **07:** ALI-04 con «máximo absoluto o, si el fabricante lo especifica, *load dump*»; pines DEN y DSEL del corte general.
  - Las propuestas de VAL-0004-02 y VAL-0005-01 para las checklists de requisitos (v2), esquema y layout.
- Excluye: el módulo de expansión (SPEC-0006) y las correcciones de texto del estudio (SPEC-0008).

## Entradas

- `gestion/informes/VAL-0004-02.md`.
- `docs/diseno/estudio-salidas.md` (SPEC-0005) y `gestion/informes/VAL-0005-01.md`.
- Decisión del usuario sobre D8 y, si lo da, el modelo de la fuente de 24 V (para el hallazgo 05).

## Entregables

- `gestion/decisiones/DEC-0003-*.md`, `docs/02` v0.3 y las checklists actualizadas.

## Criterios de aceptación

- [ ] Las observaciones 01, 02 y 04–10 de VAL-0004-02 y 01 y 03–07 de VAL-0005-01 están resueltas o justificadas una a una.
- [ ] D8 está registrada en DEC-0003 y llega a requisitos vigentes.
- [ ] La checklist de requisitos vigente se cumple.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) | |
| 2026-11-04 | coordinador | D8 decidida; añade las observaciones 01 y 03–07 de VAL-0005-01 | VAL-0005-01 |
| 2026-11-04 | usuario | Cortocircuito en una salida (VAL-0005-01-01): limitador común en el bus de las salidas | DEC-0003 |
| 2026-11-04 | coordinador | Abre la spec | |
| 2026-11-04 | usuario | D2: confirma quitar el contacto libre (solo salidas alimentadas) | DEC-0003 |
| 2026-11-05 | ing-validacion | VAL-0007-01: APROBADO_CON_OBSERVACIONES (M 3 · B 7) | `c48e2b5` |
| 2026-11-05 | coordinador | Erratas 04, 08 y DEC-0003 del 09 | `2e9640a` |
| 2026-11-05 | coordinador | Cierra la spec. 01, 02, 05, 06 y 09 a requisitos v0.4 (propuesta); 03 a SPEC-0008; 07 a SPEC-0006; 10 a ing-esquematicos | VAL-0007-01 |
