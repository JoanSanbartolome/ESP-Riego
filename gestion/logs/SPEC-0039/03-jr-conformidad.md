---
spec: SPEC-0039
agente: jr-conformidad
n: 03
fecha: 2026-11-24
estado: completado
---

# SPEC-0039 · 03 · jr-conformidad

## Hecho

- Barrido de los 23 `antiguo` de `superados.csv` en `hardware/componentes/` y `fabricacion/` (sin `datasheets/` ni PNG; respeta `alcance`): 133 líneas con el término tras editar → 58 `histórica` (rotuladas «hasta SPEC-0037»), 60 `otra placa`, 15 fuera de `alcance` o falso positivo y 4 `actualizar`. Lista por archivo y línea (numeración anterior al barrido): `gestion/logs/SPEC-0039/barrido-jr-conformidad.csv`.
- `actualizar`: `bloque-conectores.md` l. 3 (BH254V-10P → BH254R-10P), `bloque-alimentacion.md` l. 78 (C18/C19 frente al AP2114H, no al TLV1117LV), y las filas de `stock-conectores.csv` (BH254V-10P → BH254R-10P C492448) y `stock-salidas.csv` (C513710 → C28233), consultadas con `jlc.py` el 2026-11-24.
- `histórica`: fichas BZT52C15, SMBJ33A, SS310, AP2114H, BH254R-10P, `bloque-*` y BTT6050 con «hasta SPEC-0037» en cada mención; `BH254V-10P.md` y `TLV1117LV.md` con aviso de ficha histórica bajo el título.
- `fabricacion/v2.0-sch` es el paquete de la etiqueta y no se reescribe: añadido `README.md` («hasta SPEC-0037») con la tabla de lo vigente. `v2.0-prueba` no tiene coincidencias (solo C3/C8 y R24/R25).
- `otra placa`: `bom-expansion.csv` (46 líneas) y 14 de `stock-expansion.csv` (módulos de expansión). La l. 143 de `stock-expansion.csv` es la única de la placa principal: rotulada.
- Memoria: 10 archivos y 74 filas (incluye 2 afirmaciones nuevas) → 3 archivos por tema, 54 líneas (38 VIGENTE, 18 DUPLICADA, 8 OBSOLETA, 7 ESTADO, 3 RECETA). Clasificación: `gestion/logs/SPEC-0039/memoria-jr-conformidad.csv`. Corregida una receta que daba mal (SimSurfing: el MPN va sin el sufijo de embalaje).

## Decisiones y desviaciones

- Las filas de stock sustituidas pierden el dato de BH254V-10P y C513710-en-salidas; sigue en las fichas y en `fabricacion/v2.0-sch`.
- La regla de DUPLICADA no lista `hardware/componentes/`; lo del código de pedido del TS-1187A lo marqué DUPLICADA de su ficha por analogía.
- Un script de Python con las 48 sustituciones lo denegó el clasificador del modo automático; las hice con Edit.

## Verificación

- Grep final de los términos: cada línea es rótulo «hasta SPEC-…», `otra placa` o fuera de alcance.
- `gestion.py comprobar`: 0 incidencias en la memoria de jr-conformidad (quedan las de ing-validacion). Sin cambios en `hardware/v2`: `verificar.py` no aplica.

## Pendiente

- Coordinador: copiar `barrido-jr-conformidad.csv` y `memoria-jr-conformidad.csv` desde el scratchpad a `gestion/logs/SPEC-0039/`.
- RECETA a `herramientas/kicad/README.md` o herramienta: (1) banco de render, placa mínima con huellas incrustadas y `pcb render` (3 specs); (2) BOM con coste, `export bom --exclude-dnp` más `jlc.consultar` por referencia (SPEC-0032, 0038).
- Fuera de mi zona: `docs/diseno/conectores.md` l. 6 cita `stock-conectores.csv` con fecha 2026-11-15 (ahora 2026-11-24 en la fila de J10).
