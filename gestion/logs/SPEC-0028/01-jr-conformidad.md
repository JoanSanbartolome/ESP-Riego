---
spec: SPEC-0028
agente: jr-conformidad
n: 01
fecha: 2026-11-16
estado: completado
---

# SPEC-0028 · 01 · jr-conformidad

## Hecho

- `hardware/componentes/campos-alimentacion.csv` (53 filas, 55 refs) y `campos-mcu.csv` (21): nuevas, generadas de las hojas con la notación de las tablas existentes (`100n`, `1u`, LED `Rojo`) y `Fabricante` y `Datasheet` por código LCSC (PDF del fabricante o de LCSC, nunca la página de producto).
- `campos-sensores.csv` y `stock-sensores.csv`: U13 = SHT40-AD1B-R2 (C2909890); stock de 2026-11-16.
- `alimentacion.kicad_sch`, `mcu.kicad_sch` y `sensores.kicad_sch`: solo campos (`campos.py aplicar` sobre copia; el diff solo tiene bloques `property`).
- `SHT4x.md`: variante R2 (C2909890, Extended, 13 899, 2026-11-16); R2 y R3 son el mismo chip y solo cambia el carrete, 2 500 frente a 10 000 uds. (Tabla 11, p. 21; Tabla 12, p. 22; V7.3); `verificado_por: VAL-0015-02`.
- `BTT6050-1ERA.md` y `WJ500V-5.08-2P.md`: `verificado_por` con VAL-0015-02 (huella y 3D) y VAL-0024-01 (ficha). Los cambios que proponía SPEC-0023 (usos J1/J4–J9, BTT6030 con otro pinout, vías del EP a BUS_24V, sin R_GND) ya estaban en las fichas.
- `bloque-mcu.md` (nueva): C23162, C23186, C23345 y C45783, Basic, con stock del 2026-11-16.
- `0451010.MRL.md`: stock de C44479 (22 932, 2026-11-16) y comparación con §3.2 de 0453010.MR y TA10.

## Decisiones y desviaciones

- U13 pasa a C2909890 (cambio de compra DEC-0007, abarata 1,7493 $ frente a 1,8541 $ a 5 uds.).
- F1 se queda con 0451010.MRL. **0453010.MR (C178995) es alternativa válida**: misma hoja 451/453, 10 × 0,75 × 0,96 = 7,2 A (pp. 2–3), 125 V CC, I²t 26,46 A²s, misma huella (p. 4); Extended, 1 437 uds.
- **TA10 (C2998199) no cumple**: 125 Vac sin valor en CC, 200 A a 125 Vac, fusible lento con I²t «pendiente» (p. 3), curva ≈ 98 % a 60 °C (p. 6), *pad layout* distinto del NANO2 (8,0 / 3,0 mm, p. 3).
- Notación de condensadores: se mantienen `4.7uF` (C19666) y `22uF` (C45783) como están en `campos-conectores.csv` y en la hoja MCU; no se toca `conectores.kicad_sch` (paso 2).

## Verificación

- `campos.py revisar hardware/v2`: 0 que faltan, 0 distintos, 0 diferencias (DNP D12–D17 como antes).
- `comprobar.py hardware/v2`: 18 OK, 0 fallan, 2 N/A; `librerias.fichas` OK (52 códigos).
- `verificar.py hardware/v2`: ERC 0; DRC 0 errores (448 sin conectar, la PCB sin rutar); paridad 54 = 50 `footprint_symbol_field_mismatch` (campos nuevos y U13, que la PCB recibirá con `sincronizar.py` en el paso 2) + 4 `footprint_symbol_mismatch`.

## Pendiente

- ing-diseno (paso 2): `sincronizar.py` para llevar los campos y U13 a la PCB. `sensores.md` (§2 y tabla de piezas, l. 25, 72 y 203) sigue con SHT40-AD1B-R3 / C2848306 y 13 207 de stock: pasarlo a R2 (C2909890, 13 899) con el R3 como pieza anterior. Alternativa de F1 en `alimentacion.md` §2: 0453010.MR (C178995) en lugar de TA10, que no cumple.
- `SHT4x.md` solo se ha tocado en lo del R2; el calentador de 100 mA (p. 9) es de `mcu.md` §8.2.
