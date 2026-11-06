---
spec: SPEC-0019
agente: ing-validacion
n: 07
fecha: 2026-11-06
estado: completado
---

# SPEC-0019 · 07 · ing-validacion

## Orden

Revalidación completa de VAL-0019-01-01 a 04 y búsqueda de regresiones en la hoja y la PCB (DRC con las reglas de v2). Checklist `esquema.md` v6.

## Hecho

- Rama correcta, commit c6b24e2. No se abrió ningún proyecto en el MCP, así que no hizo falta `close_project`. Sin `.lck`.
- Copia en `…/scratchpad/v19b/`. `verificar.py`: ERC 0, DRC 0 (108 sin conectar por no rutar), paridad 0. MD5 de `hardware/v2` iguales antes y después.
- Cruce de la netlist XML con la PCB (`pcb_an.py` y `cruce.py` en el *scratchpad*): 0 diferencias de huella, valor, LCSC o red de pad. 55 huellas fuera del contorno. H1–H4 iguales a e4dbf44.
- Huella de U1 sin vías en la hoja, la PCB, `alimentacion.md` §7 y §8 y en las dos fichas. F1 en §3.2 coincide con §7. Nota de VAL-0019-01-04 en la spec.
- Logs 04, 05 y 06 leídos al final: coinciden con los artefactos.

## Resultado

APROBADO, 0 hallazgos. Informe: `gestion/informes/VAL-0019-02.md`.

## Pendiente

- Coordinador: propuestas de checklist del informe (cruce pad↔netlist cuando la sincronización se hace con script; paridad 0 en `esquema.md`).
