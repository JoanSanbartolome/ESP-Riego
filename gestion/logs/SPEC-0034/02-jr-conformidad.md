---
spec: SPEC-0034
agente: jr-conformidad
n: 02
fecha: 2026-11-17
estado: completado
---

# SPEC-0034 · 02 · jr-conformidad

## Hecho

- `hardware/componentes/campos-salidas.csv`: fila D12–D17 con `DNP = no` y la `Description` del esquema («…, montado (DEC-0014)»), entre comillas por la coma.
- Esquema: no hizo falta copiar; `hardware/v2/salidas.kicad_sch` ya tenía los campos de ing-diseno. `campos.py revisar hardware/v2`: 0 diferencias (antes 12).
- `hardware/componentes/M7.md`: función, «Uso» (montado por DEC-0014), layout sin la nota de DNP, aprovisionamiento y stock al 2026-11-17.
- `hardware/componentes/bloque-salidas.md`: fila D12–D17 sin «(DNP)», stock con fecha.
- Memoria `piezas-salidas-trucos.md`: D12–D17 montados; comillas en las `Description` con coma.

## M7 (C95872), JLCPCB 2026-11-17 (`jlc.py`)

| Tipo | Stock | 1–999 ud. | 1000–4999 ud. |
|---|---|---|---|
| Basic | 6 231 565 | 0,0103 USD | 0,0085 USD |

Coste por placa de D12–D17: 6 × 0,0103 = **0,062 USD**. Es Basic, así que no hay cargo de montaje de Extended. No hace falta cambio de compra (DEC-0007).

## Verificación

`verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar: no hay rutado), paridad 0; [auto] 18 OK, 0 fallan, 2 no aplican.

## Para validación

- Muestreo: D12–D17 en `salidas.kicad_sch` con `dnp no`, `in_bom yes` y `on_board yes`.
- No he regenerado BOM ni CPL: es trabajo de la fase 5.
