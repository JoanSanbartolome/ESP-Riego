---
spec: SPEC-0016
agente: ing-validacion
n: 03
fecha: 2026-11-05
estado: completado
---

# SPEC-0016 · 03 · ing-validacion

## Orden recibida

SPEC-0016 · nivel ligero · observaciones del alcance, muestreo de `git diff main...HEAD`, detalle de pines BTT6050/BTT6030 y cajetín. Sin MCP.

## Acciones

- Rama y commit: `spec/SPEC-0016-mantenimiento-fases-0-2`, d125c37.
- Spec, SPEC-0008 y SPEC-0012 leídas antes que los logs.
- `verificar.py hardware/v2`: ERC 0, DRC 0, paridad 0.
- Pines: `pdftotext` de §3.2 (p. 4) de ambos datasheets frente a los pines del `.kicad_sym` (script de comparación). Coinciden; solo cambian los nombres.
- Símbolos: `sym export svg` → PNG con PyMuPDF. Solapan nombres (VAL-0016-01-01).
- Cajetín: copia de `hardware/v2` y de la `.wks` en `scratchpad\v16\hw`, `sch export pdf`, recorte a 300 dpi. Sin solapes.
- Estudio: grep de términos y avisos, recálculo de energía y coste en Python.
- INFORME 3D: pads de la huella, p. 15 del SHT4x, `git ls-files`, CARTESIAN_POINT del STEP.
- Logs de autores leídos al final: sin afirmaciones que los artefactos desmientan. El log 02 deja «pendiente verificar visualmente el símbolo»: es lo que revela el hallazgo 01.

## Resultado

APROBADO_CON_OBSERVACIONES: 0 C, 0 A, 1 M, 2 B. Informe: `gestion/informes/VAL-0016-01.md`.
