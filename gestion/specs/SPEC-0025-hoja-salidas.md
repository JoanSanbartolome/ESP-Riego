---
id: SPEC-0025
titulo: Hoja de salidas en el esquema v2
fase: 3
estado: propuesta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0025-hoja-salidas
requisitos: [REL-01, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-10]
depende_de: [SPEC-0024, SPEC-0022]
creada: 2026-11-06
cerrada:
validacion:
---

# SPEC-0025 · Hoja de salidas en el esquema v2

## Objetivo

La hoja `hardware/v2/salidas.kicad_sch` pasa a ser el bloque de salidas de la v2, según `docs/diseno/salidas.md`, con el ERC limpio.

## Alcance

- Incluye:
  - sustituir el contenido de la hoja por los 6 canales de la v2, con las piezas de SPEC-0024;
  - etiquetas jerárquicas según `salidas.md`, conectadas con `alimentacion.kicad_sch` (`BUS_24V`) y `mcu.kicad_sch` (IN1–IN6, IS1–IS6, OUT_DEN);
  - la paridad esquema–PCB que exija `verificar.py` (piezas nuevas sincronizadas sin colocar; la sincronización con la PCB es de ing-layout).
- Excluye: colocación y rutado; otras hojas, salvo las etiquetas que conecten con esta.

## Entradas

- `docs/diseno/salidas.md`, `gestion/logs/SPEC-0024/01-jr-conformidad.md`.
- Checklist `gestion/checklists/esquema.md` (v6).

## Entregables

- `hardware/v2/salidas.kicad_sch`.
- Log `gestion/logs/SPEC-0025/01-ing-esquematicos.md` con el repaso de la checklist y la salida de `verificar.py`.

## Criterios de aceptación

- [ ] Cada pieza, valor y pin de la hoja coinciden con `docs/diseno/salidas.md`.
- [ ] `verificar.py hardware/v2`: ERC 0, sin errores de paridad nuevos.
- [ ] Mismo orden de pines en los 6 bornes (REL-06).
- [ ] Ninguna pieza de la hoja usa una librería de la v1.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-06 | coordinador | Crea la spec (propuesta) | |
