---
id: SPEC-0022
titulo: Hoja del MCU en el esquema v2
fase: 3
estado: propuesta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0022-hoja-mcu
requisitos: [MCU-01, MCU-02, MCU-03, MCU-04, MCU-05, MCU-06, MCU-07]
depende_de: [SPEC-0021, SPEC-0019]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0022 · Hoja del MCU en el esquema v2

## Objetivo

La hoja `hardware/v2/mcu.kicad_sch` pasa a ser el bloque MCU de la v2, según `docs/diseno/mcu.md`, con el ERC limpio.

## Alcance

- Incluye:
  - sustituir el contenido de la hoja por el bloque de la v2, con las piezas de SPEC-0021;
  - etiquetas jerárquicas según la tabla de GPIO, conectadas con las de `alimentacion.kicad_sch`;
  - mantener la paridad esquema–PCB que exija `verificar.py` (piezas nuevas sincronizadas sin colocar).
- Excluye: colocación y rutado; otras hojas, salvo las etiquetas que conecten con esta.

## Entradas

- `docs/diseno/mcu.md`, `gestion/logs/SPEC-0021/01-jr-conformidad.md`.
- Checklist `gestion/checklists/esquema.md`.

## Entregables

- `hardware/v2/mcu.kicad_sch`.
- Log `gestion/logs/SPEC-0022/01-ing-esquematicos.md` con el repaso de la checklist y la salida de `verificar.py`.

## Criterios de aceptación

- [ ] Cada pieza, valor y pin de la hoja coinciden con `docs/diseno/mcu.md`.
- [ ] `verificar.py hardware/v2`: ERC 0, sin errores de paridad nuevos.
- [ ] Ninguna pieza de la hoja usa una librería de la v1.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
