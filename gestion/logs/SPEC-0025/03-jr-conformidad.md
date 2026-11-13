---
spec: SPEC-0025
agente: jr-conformidad
n: 03
fecha: 2026-11-13
estado: completado
---

# SPEC-0025 · 03 · jr-conformidad

## Orden recibida

Paso 1b: ficha de bloque para que C17713, C17902 y C23253 (y el resto de piezas de salidas) cuenten en `librerias.fichas`.

## Entregado

- `hardware/componentes/bloque-salidas.md`: tabla con columna `LCSC`, tipo y stock en la misma fila, fecha 2026-11-12 en el archivo y la palabra «datasheet» (URLs en `campos-salidas.csv`). Cubre los 13 códigos principales de salidas; las alternativas van fuera de la tabla (entre paréntesis no cuentan). Datos de `stock-salidas.csv`.

## Verificación

- `comprobar.py hardware/v2 --punto librerias.fichas`: FALLA con 6 líneas, las de SPEC-0028 (C19666, C23162, C23179, C23186, C23345, C45783). Estos tres códigos aún no salen en la lista porque `hardware/v2` todavía no tiene la hoja de salidas (paso 2 pendiente): no he podido ver el cambio de "sin ficha" a "con ficha". Tras el paso 2, deben seguir sin aparecer C17713, C17902 y C23253; si salen, es un fallo del formato de mi ficha.
- Usos de `herramientas/kicad/`: 1 (`comprobar.py`). Scripts en la carpeta temporal: 0.

## Pendiente

- Coordinador: repetir `comprobar.py hardware/v2 --punto librerias.fichas` tras el paso 2.
