---
spec: SPEC-0004
agente: ing-validacion
n: 02
fecha: 2026-11-04
estado: completado
---

# SPEC-0004 · 02 · ing-validacion

## Orden recibida

> SPEC-0004 · rama spec/SPEC-0004-requisitos-v02 (activa, commit b9e0032) · Lee: la spec, VAL-0004-01, DEC-0002, docs/02, docs/03, las checklists de requisitos, esquema y layout, la Responsabilidad de ing-layout.md y `git diff 28ad302 b9e0032` · Haz: segunda validación. Por cada hallazgo 01–16 de VAL-0004-01, comprobar si está resuelto o ya no aplica; aplicar la checklist de requisitos v1; revisar la coherencia de la cadena DC (18–30 V, SMBJ33A, Vc, buck ≥ 60 V, UVLO ≈ 15 V, ALI-12 con 5 A y 4 A) y que no quede rastro de la entrada de AC. La trazabilidad, con el método en memoria. Sin MCP de KiCad · Entrega: VAL-0004-02.md y este log.

Corrección a mitad de tarea: la revisión se cortó por el límite de uso. El coordinador añadió el commit `924371f` (las electroválvulas instaladas son de 24 V DC, ≈ 0,2 A) y pidió revisar hasta HEAD (`git diff 28ad302 HEAD`).

## Contexto consultado

- **Gestión:** SPEC-0004, VAL-0004-01, DEC-0002 y la checklist de requisitos v1. Como entregables, las checklists de esquema v2 y layout v2. La checklist de proceso v2, para saber si el cambio de `ing-layout` exige una prueba en vivo.
- **Documentación:** docs/02 en HEAD (completo), docs/03, y docs/02 de `main` y de `28ad302`, con `git show`.
- **Specs y agentes:** SPEC-0005, SPEC-0006 y `.claude/agents/ing-layout.md`.
- **Git (solo lectura):** `git diff 28ad302 b9e0032`, `git diff b9e0032 924371f` y los mensajes de los dos commits.
- **Web:**
  - SMBJ33A: VRWM de 33 V, VBR de 36,7–40,6 V, Vc de 53,3 V a 11,3 A (10/1000 µs). Fichas de DigiKey de Littelfuse y de LCSC C294879; el PDF de Littelfuse devolvió 403.
  - MEAN WELL LRS-150-24: ajuste de 21,6–28,8 V según varias fichas de distribuidor. La OVP de 28,8–33,6 V solo sale en una ficha. El PDF del datasheet tiene el texto convertido en trazos y no se pudo extraer.

## Acciones

1. Rama `spec/SPEC-0004-requisitos-v02`; HEAD `b9e0032` al empezar y `924371f` al retomar.
2. Script `scratchpad/val0402/traza.py`:
   - ejecuta `gestion.trazabilidad()` en memoria (sustituye `escribir`) y lo compara con el `TRAZABILIDAD.md` versionado;
   - compara las tablas de `main`, `28ad302` y HEAD;
   - busca los IDs cambiados que la spec no cita.
3. Script `scratchpad/val0402/ids.py`: comprueba que los IDs citados existen en docs, checklists, agentes, DECs y specs abiertas o propuestas.
4. Grep de términos obsoletos (AC, puente, bulk, `AC_In`, SMBJ40, 4–20, IP65, DIN, batería…) en todo el repositorio, salvo los informes, los logs y docs/01.
5. Recálculo de la cadena DC:
   - Vc · 1,1 = 58,6 V;
   - UVLO tras las protecciones con 0,1–0,3 V de caída;
   - presupuesto de 4,49 A frente a 5 A;
   - REL-02 a 31,7 V AC en vacío y 45 V de pico;
   - REL-05 frente a 2 × 0,2 A.
6. Estado de los hallazgos 01–16 de VAL-0004-01, uno por uno.
7. Formé los hallazgos antes de contrastar los mensajes de commit y el registro de la spec (SPEC-0004 no tiene log de autor).
8. Informe `gestion/informes/VAL-0004-02.md`.

## Decisiones y justificación

- **TVS frente a la polaridad (01) en M:** el texto permite un diseño que incumple un criterio de §6, pero se puede corregir en la redacción o en el esquema. Ya estaba en la v0.1, así que no es una regresión.
- **SPEC-0005 (03) en M y no en A:** no es un entregable de SPEC-0004 ni un criterio de aceptación. Pero la checklist de requisitos v1 pide revisar las specs abiertas, y la spec alimenta D8 con un dato erróneo.
- **Hallazgo 07 de VAL-0004-01 resuelto sin prueba en vivo:** solo cambia el texto de Responsabilidad, no `tools`, `disallowedTools` ni *matchers*, que es lo que exige el punto 24 de la checklist de proceso v2.
- **Veredicto:** solo hay M y B, y los 5 criterios se cumplen. Por tanto, APROBADO_CON_OBSERVACIONES.

## Verificación

- Trazabilidad en memoria: 0 avisos, 55 requisitos vigentes. El archivo versionado solo difiere en la columna *Commits* (33 filas).
- IDs: ninguno inexistente; ningún retirado fuera de §9 y DEC-0002.
- Requisitos cambiados que no cita SPEC-0004: solo ALI-03.
- Hallazgos de VAL-0004-01: 13 resueltos, 2 en parte (10 y 11) y 1 que ya no aplica (02).
- Nuevos: C 0 · A 0 · M 3 · B 7.

## Pendiente

- Coordinador: actualizar SPEC-0005 con las válvulas de 24 V DC (03) antes de cerrar D8. Si el estudio de la otra rama parte de válvulas de AC, revisarlo.
- Coordinador: 01 y 02 en docs/02 antes del merge, o como specs propuestas. Añadir ALI-03 al campo `requisitos` y al tráiler del merge (04).
- Usuario: modelo de la fuente (ajuste y OVP) para cerrar el hallazgo 05.
- Los scripts de `scratchpad/val0402/` y el PDF de `scratchpad/mw/` se pueden borrar. No contienen nada del TFG.

## Notas para el siguiente agente

- Cuando el usuario aclara un dato de entrada a mitad de una spec, hay que buscar sus apariciones en las specs abiertas de otras ramas o de `main`. El commit de la aclaración suele tocar solo docs/02 y la DEC.
