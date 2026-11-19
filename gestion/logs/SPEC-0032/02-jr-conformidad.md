---
spec: SPEC-0032
agente: jr-conformidad
n: 02
fecha: 2026-11-19
estado: completado
---

# SPEC-0032 · 02 · jr-conformidad

## Hecho

- `fabricacion/v2.0-sch/bom.csv`: 53 líneas, 187 piezas montadas (sin H1–H4, TP1–TP5 ni el puente, que son `in_bom no`; 0 DNP). Stock y precio con `jlc.consultar` (`herramientas/kicad/jlc.py`) el 2026-11-19, tramo de 5 placas (cantidad × 5).
- **Coste por placa: 27,46 USD** (solo piezas, precio LCSC del tramo de 5 placas; sin PCB, montaje ni recargos).
- `fabricacion/v2.0-sch/esquema.pdf`: 12 páginas en el orden del árbol (raíz, Salidas, Canal1–6, MCU, Alimentacion, Conectores, Sensores); el «Id» del cajetín = página del PDF; `hoja.py paginas` código 0.
- VAL-0028-01-03: `campos-mcu.csv` (C24 `22u`, C26 `4.7u`) y `campos-conectores.csv` (C50 `4.7u`), sin tensión porque esas tablas no la llevan en ningún condensador. `campos.py aplicar` en `mcu.kicad_sch` y `conectores.kicad_sch` y `sincronizar.py` a la PCB: 3 campos `Value` cambiados, 0 redes ni huellas.
- VAL-0028-01-04: `BTT6050-1ERA.md`, `verificado_por` con «VAL-0028-01 (pasta corregida del EP)».

Huellas que cambian frente a `main`: C24, C26, C50 (solo el campo `Value`, VAL-0028-01-03).

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar, sin rutar), paridad 0. `esquema.pcb_main` declara C24, C26 y C50 arriba.
- `campos.py revisar`: 197 piezas · 0 · 0 · DNP 0 · 0 diferencias.
- BOM: MPN de la API igual al del esquema en las 53 líneas; ninguna con stock por debajo de 5 placas.

## Para validación

- Stock más justo (todos ≥ 5 placas): TLV1117LV33DCYR C15578 (37), TPS26632RGER C1850278 (93), MVK 63V47 C165628 (718).
- 27 códigos *Extended* (uno, C23159, *preferida*, sin recargo): con JLCPCB son 26 × 3 USD por pedido, unos 15,6 USD/placa en un pedido de 5 placas, aparte del coste de piezas.

## Pendiente

- Ninguno.
