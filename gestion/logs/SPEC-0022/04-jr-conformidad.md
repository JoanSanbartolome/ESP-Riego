# SPEC-0022 · 04 · jr-conformidad

- Orden: ficha KT-0603R (VAL-0022-01-01).
- Creados: `hardware/componentes/KT-0603R.md`, `hardware/componentes/datasheets/KT-0603R.pdf` (copia del PDF de LCSC de `scratchpad\s22`, 11 págs.; fabricante Hubei KENTO).
- Polaridad (p. 2 del PDF): ② «−» = cátodo = pad 1 (K); ① «+» = ánodo = pad 2 (A). Marca verde superior en el lado ②; en la vista inferior, triángulo con base en ① y vértice hacia ②. Difiere del KT-0603YG (barra ancha de la T = cátodo): aquí lo ancho es el ánodo. Anotado en la ficha.
- Datos: V_F 1,8–2,4 V, I_V 145–300 mcd, 615–630 nm (pp. 3-4); I_F 25 mA, P_d 40 mW (p. 3).
- JLCPCB API (2026-11-07): C2286 Basic, stock 6 618 030; `dataManualUrl` = lcsc_datasheet_1810231112 (el de la ficha).
- `bloque-alimentacion.md` fila D4: C2286, Basic, 6 683 182 (stock antiguo). Sin contradicción de datos; solo stock desactualizado. Sin cambios (fuera de mi zona).
- Pendiente (otros): corregir la frase de `mcu.md` §11 («KT-0603R sin ficha propia») y `salidas.md` l. 434; `mcu.md` l. 426 menciona «ficha en bloque-alimentacion.md». Enlazar la ficha nueva.
- Curva p. 5 (V_F ≈ 1,85 V a 1 mA): tomada de VAL-0022-01, no releída (es gráfica).

## Requiere verificación de validación

- Ficha KT-0603R: polaridad y pinout, datasheet `datasheets/KT-0603R.pdf` p. 2 (dibujo). Sin piezas nuevas de librería (símbolo/huella/3D oficiales).

## Checklist (`librerias.md`)

- Polaridad con página y correspondencia datasheet↔KiCad: cumple.
- Origen del activo: oficial KiCad; sin pieza creada: no aplica.
- Fecha de stock/tipo: cumple.
- KiCad/`verificar.py`: no aplica (no se tocó ningún proyecto).
