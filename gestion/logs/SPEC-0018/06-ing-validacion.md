---
spec: SPEC-0018
agente: ing-validacion
n: 06
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 06 · ing-validacion

## Orden
Revalidar VAL-0018-01 01–07 y buscar regresiones. Nivel completo. Commit revisado: 6250829. Informe: `gestion/informes/VAL-0018-02.md`.

## Hecho
- Rama correcta. `get_backend_state` vacío, sin `.lck`. Sin `open_project`, así que no hace falta `close_project`.
- `verificar.py` sobre una copia (`scratchpad\v18r\hw\v2`): LIMPIO.
- `validate_symbol_library` sobre la copia: válida, 5 símbolos.
- Placa de prueba con el `.kicad_pro` de v2 (`scratchpad\v18r\mk.py`): 6 `drill_out_of_range` en las vías de la U2 nueva (0,2 mm < 0,3 mm). JP1 y D_SMB, limpios.
- Gerber de máscara y pasta: el EP abre 2,71 × 3,4 en F.Mask y F.Paste, con las vías dentro. B.Mask no tiene aperturas.
- Render superior e inferior de U2: pin 1 correcto. Render de JP1 y D2: correctos.
- `sym export svg` de SMBJ33A + Edge: los nombres «AK» se ven dentro del cuerpo.
- Cotas de U2 frente a LMR36520.pdf pp. 38-40: pads, máscara y pasta coinciden. Las vías no (FAB-02).
- Recalculados CIN (5,07 µF mín.), C10 (0,85–0,96 µF), C3 (0,15–0,17 µF) y el recuento 19 Extended / 10 Basic: coinciden.
- Grep: §7 de `alimentacion.md` desfasado (U2, lista de piezas nuevas). C22 no choca con otras referencias.

## Resultado
APROBADO_CON_OBSERVACIONES: 0 C, 0 A, 1 M y 4 B. 01–07 resueltos; 08 sigue abierto (mantenimiento).

## Pendiente
- 02-01 (vías de 0,3 / 0,6, y corregir «tapadas»): mejor antes del merge.
- 02-02 y 02-03 en la misma librería.
- 02-04 y 02-05: SPEC-0019 o mantenimiento.
