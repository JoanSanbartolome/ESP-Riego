---
spec: SPEC-0019
agente: ing-validacion
n: 03
fecha: 2026-11-06
estado: completado
---

# SPEC-0019 · 03 · ing-validacion

## Orden

Validación completa de `alimentacion.kicad_sch` frente a `alimentacion.md`, checklist `esquema.md` v5, VAL-0014-01-01/02, VAL-0018-02-04, JP1 y README; valorar los 55 `missing_footprint` y los símbolos de alimentación globales.

## Hecho

- Rama correcta; commit e4dbf44. MCP: nada cargado (`get_backend_state`); no se abrió ningún proyecto, así que no hizo falta `close_project`.
- Copia en `…/scratchpad/v19/` (v2 y librerías). `verificar.py`: ERC 0, DRC 0, paridad 55 `missing_footprint`. MD5 del repositorio iguales antes y después.
- Netlist XML de la copia: 55 piezas y todas las redes comparadas con §2, §3 y §7. Pinouts de TPS2663, TPS2116, LMR36520, TLV1117 y TO-252 frente a datasheet.
- PDF de la copia: cajetín correcto en la pág. 4/5.
- API de JLCPCB: C14663 Basic, C136967 Extended, con stock.
- DRC de placas de prueba con el `.kicad_pro` de v2: U1 da 9 `drill_out_of_range`; las otras 20 huellas, 0 errores.
- Logs 01 y 02 leídos al final: coinciden con los artefactos. El log 01 atribuye la paridad a una tarea de otra zona, sin cumplir el criterio.

## Resultado

RECHAZADO: 1 A (01, paridad), 1 M (02, vías de U1), 2 B (03 y 04). Informe: `gestion/informes/VAL-0019-01.md`.

## Pendiente

- Coordinador: arreglar la huella de U1 (ing-esquematicos y jr-conformidad). Después, sincronizar la PCB (ing-layout) y hacer una revalidación ligera.
