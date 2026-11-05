---
id: SPEC-0011
titulo: Requisitos v0.4: ventana del limitador y sobrecarga por canal
fase: 0
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0011-requisitos-v04
requisitos: [ALI-01, ALI-04, ALI-06, ALI-09, ALI-12, ALI-13, REL-03, REL-05, REL-08, REL-10, FAB-01, FAB-03, FAB-09]
depende_de: [SPEC-0007]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0011 · Requisitos v0.4: ventana del limitador y sobrecarga por canal

> Observaciones 01, 02, 05, 06 y 09 de VAL-0007-01. **Decisiones del usuario (2026-11-05, DEC-0004):**
>
> - Fuente: una fuente de 24 V DC y 5 A para tiras LED, sin más datos; el coordinador asume los parámetros típicos de ese tipo de fuente, sin complicar el circuito.
> - Sobrecarga de un canal: sin protección por canal. Se define una carga máxima por canal como parámetro y se dimensiona correctamente.

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la v0.4: la ventana del limitador común queda cerrada contra la fuente real, la sobrecarga de un solo canal tiene un mecanismo de protección, y se resuelven las observaciones B de VAL-0007-01 que afectan a los requisitos.

## Alcance

- Incluye los hallazgos de `gestion/informes/VAL-0007-01.md`:
  - **01 (M):** la fuente como dato de entrada o requisito (corriente nominal, protección de sobrecarga y OVP). Con ella:
    - ALI-12 y ALI-13 definen el umbral del limitador como una banda con tolerancia, entre el total de las salidas y la protección de la fuente menos la lógica;
    - la prueba de §6 se hace por encima de la banda;
    - ALI-04 elige entre la SMBJ33A y la SMBJ36A, y fija la tensión del limitador (≥ 60 V o ≥ 64 V).
  - **02 (M):** la sobrecarga de un canal entre 1 A y el umbral del limitador, según la decisión del usuario:
    - sin protección por canal: carga máxima por canal como parámetro y dimensionamiento correcto (DEC-0004).
  - **05 (B):** aviso de subtensión y punto de prueba separados, y arranque en frío.
  - **06 (B):**
    - carga abierta en OFF con el bus de salidas apagado (REL-10 frente a ALI-13);
    - prueba de que el limitador está apagado durante el reset.
  - **09 (B):**
    - FAB-01 frente a D6;
    - L de la válvula a medir (REL-03);
    - corrección de T/HR sin ambigüedad en §6;
    - limitador y presupuesto de los bordes en la fase 2 de `docs/03`.
  - Las propuestas de VAL-0007-01 para la checklist de requisitos v3 y la de esquema v4.
- Excluye:
  - el estudio de salidas (SPEC-0008);
  - el módulo de expansión (SPEC-0006);
  - la memoria de ing-esquematicos, que la actualiza ese agente.

## Entradas

- `gestion/informes/VAL-0007-01.md`.
- `docs/02-especificaciones-v2.md` (v0.3) y `gestion/decisiones/DEC-0003-salidas-high-side-y-limitador.md`.
- El datasheet de la fuente del usuario.
- `gestion/checklists/requisitos.md`, `esquema.md` y `layout.md`.

## Entregables

- `docs/02-especificaciones-v2.md` v0.4.
- Una DEC si cambia una decisión o el coste.
- Las checklists actualizadas.

## Criterios de aceptación

- [ ] Cada hallazgo del alcance está resuelto o justificado uno a uno.
- [ ] El umbral del limitador es una banda con tolerancia, compatible con la fuente, y la prueba de §6 queda fuera de ella.
- [ ] Ninguna corriente entre la nominal de un canal y el umbral del limitador queda sin mecanismo de protección ni prueba.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | El usuario fija la fuente (LED de 24 V y 5 A) y descarta la protección por canal; abre la spec | DEC-0004 |
| 2026-11-05 | ing-validacion | VAL-0011-01: RECHAZADO (M 1 · B 8) | `4a0b771` |
| 2026-11-05 | coordinador | Corrige VAL-0011-01: fuente en su ajuste de fábrica, carga instalada en frío (3,9 A), banda 3,9–4,9 A y hallazgos B | VAL-0011-01 |
