---
spec: SPEC-0025
agente: jr-conformidad
n: 01
fecha: 2026-11-12
estado: completado
---

# SPEC-0025 · 01 · jr-conformidad

## Orden recibida

Paso 1: tabla de campos de las 87 referencias en `campos-salidas.csv` y stock/tipo con fecha en `stock-salidas.csv`.

## Entregado

- `hardware/componentes/campos-salidas.csv`: 17 filas (`Refs`) que cubren 87 referencias; formato del README de `herramientas/kicad/` («Formatos»). Fuente: tabla del log 01 de SPEC-0024. Los «(igual que …)» se han sustituido por la URL real. D6–D11 `Value` Rojo; D12–D17 `Value` M7 y `DNP` = sí. Sin columnas Tipo/Stock/Fecha (van en el otro archivo, para que `campos.py` no las trate como campos).
- `hardware/componentes/stock-salidas.csv`: 25 códigos de `salidas.md` (+ C126351, alternativa de R57–R62 que el documento no recoge), consulta 2026-11-12, con `jlc.py`.

## Hallazgos

- Todos los códigos con stock; ninguno cambia de tipo respecto a SPEC-0024. Sin cambios de compra (DEC-0007): no hay Basic equivalente nuevo.
- BTT6050 (C534868): 1 628 (igual que el 2026-11-10). 60 uds para 10 placas = 3,7 %. C7471274 (alternativa de C45/C46) solo 1 959.
- Stock de hoy distinto al del log de SPEC-0024 (2026-11-10): C8465 293 197; C513710 26 821 (140 uds para 10 placas, ok); C381466 37 932; C534865 10 556; C2286 5,99 M; C95872 6,49 M. Los cambios 5 y 6 de SPEC-0024 pueden usar las cifras del CSV de hoy.
- `campos.py revisar hardware/v2`: solo incoherencias ya conocidas (SPEC-0028: D5 LED/Rojo, 100n/100nF, Fabricante de alimentación) y «en la tabla y no en la hoja» (esperado hasta el paso 2).

## Herramientas y scripts

- Usos de `herramientas/kicad/`: 5 (`jlc.py --help`, `jlc.py` dos veces, `campos.py --help`, `campos.py revisar`).
- Scripts en la carpeta temporal: 0 (un recuento de referencias con Python en línea, sin archivo).

## Pendiente

- Paso 2: `hoja.py generar --campos hardware/componentes/campos-salidas.csv`.
- Nota: mi intento de `mkdir gestion/logs/SPEC-0025` lo bloqueó la guardia; el parte lo creó Write.
