---
id: SPEC-0019
titulo: Hoja de alimentación de la v2
fase: 3
estado: abierta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0019-hoja-alimentacion
requisitos: [ALI-01, ALI-02, ALI-03, ALI-04, ALI-05, ALI-06, ALI-07, ALI-08, ALI-09, ALI-10, ALI-11, ALI-12, ALI-13]
depende_de: [SPEC-0018]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0019 · Hoja de alimentación de la v2

## Objetivo

La hoja `hardware/v2/alimentacion.kicad_sch` deja de ser la de la v1 y pasa a ser el bloque de entrada y limitador de la v2, según `docs/diseno/alimentacion.md`, con el ERC limpio.

## Alcance

- Incluye:
  - sustituir el contenido de la hoja por el bloque de la v2, con las piezas de SPEC-0018;
  - etiquetas jerárquicas para 24 V del bus de salidas, 5 V, 3,3 V, GND, VIN_SENSE, habilitación e IMON del limitador;
  - VAL-0014-01-01 (textos de bloque de `conectores.kicad_sch` y `alimentacion.kicad_sch`) y VAL-0014-01-02 (quitar de `fp-lib-table` y `sym-lib-table` las librerías de la v1 que no se usen);
  - JP1 en paralelo con U1 (DEC-0006), con el texto «abierto = limitador · cerrado = sin limitador», y en `hardware/v2/README.md` lo que se pierde con el puente cerrado;
  - VAL-0018-02-04: poner al día §7 y §8 de `docs/diseno/alimentacion.md` con `esp-riego:SMBJ33A` (D2), la huella `esp-riego:Texas_DDA0008B_…` (U2), C22 y JP1 con conexión sólida; C3 y C10 en 0805 con sus LCSC nuevos;
  - cambios de compra de DEC-0007: R8 → C136967; C5, C9, C13, C14, C20 y C21 → C14663 solo si JLCPCB confirma stock (LCSC daba 0 el 2026-11-06; si no, se quedan en C1591) (en `alimentacion.md`, la ficha del bloque la ajusta jr-conformidad en SPEC-0021 o mantenimiento);
  - referencias del bloque MCU reservadas (C23–C26, R16–R25, D5, J2–J3, U5–U6, SW1–SW2; `mcu.md` §11): la hoja de alimentación no las usa;
  - mantener la paridad esquema–PCB que exija `verificar.py` (las piezas nuevas se sincronizan con la PCB sin colocarlas).
- Excluye:
  - colocación y rutado;
  - otras hojas, salvo las etiquetas que conecten con esta.

## Entradas

- `docs/diseno/alimentacion.md`, `gestion/logs/SPEC-0018/01-jr-conformidad.md`.
- `gestion/informes/VAL-0014-01.md` (01 y 02) y `gestion/informes/VAL-0018-02.md` (04).
- `hardware/componentes/bloque-alimentacion.md`.
- Checklist `gestion/checklists/esquema.md`.

## Entregables

- `hardware/v2/alimentacion.kicad_sch` y las tablas de librerías de `hardware/v2` corregidas.
- Log `gestion/logs/SPEC-0019/01-ing-esquematicos.md` con el repaso de la checklist y la salida de `verificar.py`.

## Criterios de aceptación

- [ ] Cada pieza y cada valor de la hoja coinciden con `docs/diseno/alimentacion.md`.
- [ ] `verificar.py hardware/v2`: ERC 0, sin errores de paridad nuevos (se justifican las diferencias por piezas sin colocar).
- [ ] VAL-0014-01-01 y 02 resueltas.
- [ ] Ninguna pieza de la hoja usa una librería de la v1.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-06 | coordinador | Abre la spec (aprobada por el usuario) | |
