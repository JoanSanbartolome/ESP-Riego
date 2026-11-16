---
name: mantenimiento-campos-trucos
description: Trucos de SPEC-0028 paso 1: generar tablas de campos desde las hojas, datasheets de LCSC por API, python de Windows con rutas
metadata:
  type: reference
---

- Python de Windows no entiende `/c/...`: dentro de `python` usar `C:/Users/...`; con `PYTHONUTF8=1` para imprimir Ω, µ.
- `hoja.py extraer` se niega con `alimentacion.kicad_sch` (tiene cables). Para volcar sus campos: `campos.piezas_de([Path(hoja)])` desde `herramientas/kicad/` (da `props`, `dnp`, `ref`) y `campos.rangos(refs)` para la celda `Refs` (cambiar «–» por «-»).
- Una tabla de campos se genera agrupando por (Value, Footprint, LCSC, MPN, Fabricante, Datasheet, Description, DNP); Fabricante y Datasheet por código LCSC salen de las tablas existentes y, si no, de `dataManualUrl` de la API.
- `dataManualFileAccessIdUrl` baja el PDF real (LCSC bloquea curl); hojas TLC/Littelfuse en pdftotext con `-layout`; la curva de derating hay que verla en PNG (`pdftoppm -png -r 70`).
- `verificar.py` no admite `--detalle`; solo `--json` y `--salida`.
