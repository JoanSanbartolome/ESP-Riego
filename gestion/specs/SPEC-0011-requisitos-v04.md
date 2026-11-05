---
id: SPEC-0011
titulo: Requisitos v0.4: ventana del limitador y sobrecarga por canal
fase: 0
estado: propuesta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0011-requisitos-v04
requisitos: [ALI-04, ALI-09, ALI-12, ALI-13, REL-03, REL-05, REL-10, FAB-01]
depende_de: [SPEC-0007]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0011 · Requisitos v0.4: ventana del limitador y sobrecarga por canal

> Propuesta: observaciones 01, 02, 05, 06 y 09 de VAL-0007-01. **Necesita del usuario:** el modelo de la fuente de 24 V (corriente nominal, protección de sobrecarga y OVP) para el 01, y una decisión sobre la sobrecarga de un canal para el 02. Se abre cuando estén los dos.

## Objetivo

`docs/02-especificaciones-v2.md` pasa a la v0.4: la ventana del limitador común queda cerrada contra la fuente real, la sobrecarga de un solo canal tiene un mecanismo de protección, y se resuelven las observaciones B de VAL-0007-01 que afectan a los requisitos.

## Alcance

- Incluye los hallazgos de `gestion/informes/VAL-0007-01.md`:
  - **01 (M):** la fuente como dato de entrada o requisito (corriente nominal, protección de sobrecarga y OVP). Con ella:
    - ALI-12 y ALI-13 definen el umbral del limitador como una banda con tolerancia, entre 4 A y la protección de la fuente menos la lógica;
    - la prueba de §6 se hace por encima de la banda;
    - ALI-04 elige entre la SMBJ33A y la SMBJ36A, y fija la tensión del limitador (≥ 60 V o ≥ 64 V).
  - **02 (M):** la sobrecarga de un canal entre 1 A y el umbral del limitador, según la decisión del usuario:
    - pistas y bornes de cada salida dimensionados hasta el umbral;
    - corte por firmware con IS, documentado y con prueba en §6;
    - o una protección por canal (PTC o fusible).
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
