---
spec: SPEC-0018
agente: jr-conformidad
n: 07
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 07 · jr-conformidad

## Orden
Corregir VAL-0018-02-01, 02 y 03.

## Acciones
- 01: huella `Texas_DDA0008B_…Mask2.71x3.4mm`: 6 vías 0,2/0,45 -> 8 vías 0,3/0,6 en (± 0,65; ± 0,65 / ± 1,95), disposición de TI. B.Cu del EP 2,6 x 3,3 -> 2,95 x 4,9 (con 2,6 x 3,3 las vías de y = ± 1,95 quedaban tangentes: `connection_width`). Sin cambios en F.Cu, F.Mask ni F.Paste.
- Estado real (descr y `LMR36520.md` corregidos): abajo tapadas (sin apertura en B.Mask); arriba, las 4 de y = ± 0,65 abiertas bajo la pasta, las 4 de y = ± 1,95 tapadas por la máscara. No se han tapado por arriba; rellenado/tapado = decisión de fase 5.
- 02: `esp-riego:SMBJ33A` `pin_names` con `(hide yes)`. `sym export svg` OK.
- 03: `Value` de la huella = su nombre; `ki_fp_filters` de LMR36520FADDA = `Texas*DDA0008B*`.
- `LMR36520.md`: fila «Vías» y B.Cu actualizados.

## Verificación
- Placa de prueba (copia de `hardware/v2` con su `.kicad_pro` + U2 nueva en 60,60, en el scratchpad): DRC 0 violaciones, 0 sin conectar, paridad 0 (antes 6 `drill_out_of_range`; tras vías 0,3/0,6 y B.Cu pequeño, 2 `connection_width`).
- `verificar.py hardware/v2`: ERC 0 / DRC 0 / paridad 0 (U2 aún no está en la PCB real).
- Gerber de máscara no repetido: por construcción, las vías no tienen capas de máscara.
- Checklist librerías (huella): vías según FAB-02 cumple; selector `ki_fp_filters` y `Value` cumple; polaridad/nombres de pin SMBJ33A cumple; resto sin cambios.

## Pendiente
- 04 y 05 de VAL-0018-02 (alimentacion.md §7/§8; estarcido 0,12 mm en la ficha y en el plan de fase 5): no pedidos aquí.

## Requiere verificación de validación
- Huella `esp-riego:Texas_DDA0008B_…Mask2.71x3.4mm` (modificada: vías y B.Cu). LMR36520.pdf (SNVSBF0C) pp. 38-40, dibujo 4214849/B, nota 10 (p. 39).
- Símbolo `esp-riego:SMBJ33A` (modificado: `pin_names` ocultos) y `LMR36520FADDA` (`ki_fp_filters`). Datasheet: ver ficha `SMBJ33A.md`.
