---
spec: SPEC-0019
agente: ing-layout
n: 05
fecha: 2026-11-06
estado: completado
---

# SPEC-0019 · 05 · ing-layout

## Orden recibida

SPEC-0019 · rama spec/SPEC-0019-hoja-alimentacion (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/specs/SPEC-0019-hoja-alimentacion.md + gestion/informes/VAL-0019-01.md (01) + gestion/logs/SPEC-0019/04-ing-esquematicos.md · Haz: sincronizar hardware/v2/esp-riego.kicad_pcb con el esquema: las 55 huellas de la hoja de alimentación entran en la PCB fuera del contorno, agrupadas, sin colocar ni rutar; quita las huellas de la v1 de esa hoja que ya no existan en el esquema. Objetivo: verificar.py hardware/v2 con paridad 0 y DRC sin errores (los sin conectar por no rutar se anotan). No toques el esquema. Único usuario de KiCad; save y close_project al terminar. · Entrega: PCB + log gestion/logs/SPEC-0019/05-ing-layout.md con la salida de verificar.py. Brevedad: solo contrato de salida; log telegráfico.

## Contexto consultado

- SPEC-0019, VAL-0019-01 (01), log 04.
- `hardware/v2/esp-riego.kicad_pcb` (antes: solo H1–H4 y contorno 100 × 70 en x 100–200, y 60–130).
- Checklist `gestion/checklists/layout.md` v5.

## Acciones

1. Rama `spec/SPEC-0019-hoja-alimentacion` y KiCad cerrado (`check_kicad_ui`: no; sin `.lck`).
2. Prueba en copia (scratchpad `s19/`): `open_project` + `sync_schematic_to_board` del MCP. Resultado inválido: 55 huellas en (0, 0) apiladas; redes sin prefijo jerárquico (`VIN_PROT` en vez de `/Alimentacion/VIN_PROT`) → 87 `net_conflict`; sin campos MPN/LCSC → 55 `footprint_symbol_field_mismatch`; además escribió el archivo él solo y rechazó el autoguardado. `close_project(save=false)`; descartado.
3. Sustituto equivalente a F8, en la copia: netlist con `kicad-cli sch export netlist --format kicadsexpr` + script con el `pcbnew` de KiCad 10.0.6 (`python.exe` de KiCad, `-I`; script en el scratchpad, fuera del repo):
   - huellas desde la librería indicada en el campo `Footprint` (oficiales de KiCad 10 o `esp-riego.pretty`), con 3D de la librería;
   - referencia, valor, `path` (hoja + UUID del símbolo), `sheetname`/`sheetfile`, campos del símbolo ocultos en F.Fab, `exclude_from_bom`/`exclude_from_pos_files` (JP1 y TP);
   - redes de la netlist en todos los pads numerados, incluidas `unconnected-(…)` de los pines NC; pads sin número (pasta) sin red.
4. Colocación fuera del contorno, a la izquierda (x 10–92, y 60–113), por tipo en filas: J/F/D/Q · U/L/JP · C · R · TP. Sin rutar ni zonas.
5. Huellas de la v1 a quitar: ninguna (la PCB solo tenía H1–H4, que siguen en el esquema). H1–H4 sin cambios (sus líneas siguen íntegras).
6. Copiada la PCB resultante a `hardware/v2/esp-riego.kicad_pcb`. El `.kicad_pro` de la copia (reescrito por pcbnew) no se copia: el del repo queda intacto.

## Decisiones y justificación

- MCP `sync_schematic_to_board` descartado: no da paridad 0 (punto 2). El script reproduce el actualizador de KiCad y se comprueba con `verificar.py`.
- Sin grupo de KiCad (`PCB_GROUP`): agrupadas por posición, para no estorbar la colocación con el MCP.

## Verificación

`python herramientas/verificar.py hardware/v2`:

- ERC 0 (errores 0, avisos 0).
- DRC 0 (errores 0, avisos 0), **sin conectar 108**: todo el bloque sin rutar (más por pieza: U1 14, U2 8, C2 4, C16 4, U3 4).
- Paridad 0.

Checklist `layout.md` v5:

- Reglas / `.kicad_dru` y clases: no aplica (sin cambios en reglas).
- Reglas / DRC sin errores: cumple; sin conectar 108 → pendiente del rutado (fuera de alcance).
- Reglas / paridad: cumple (0).
- Reglas / zonas rellenadas: no aplica (no hay zonas).
- Reglas / cajetín en PDF: no aplica (sin cambios de cajetín).
- Reglas / `embedded_files`: cumple (no hay).
- Reglas / `outputdirectory`: cumple (vacío).
- Floorplan, Potencia, Masa, Fabricación: no aplica (sin colocar ni rutar; spec excluye colocación).
- 3D / modelo en todos: parcial — 49/59 con modelo; sin modelo H1–H4, TP1–TP5, JP1 (la librería no lo trae). Pendiente para la colocación (FAB-11).
- 3D / caja: no aplica.

## Pendiente

- Colocación y rutado del bloque (spec de layout futura): vías 0,3/0,6 al EP de U1 (`alimentacion.md` §8); 3D para TP y JP1 si FAB-11 lo exige.

## Notas para el siguiente agente

- `sync_schematic_to_board` del MCP (swig) no sirve en proyectos jerárquicos: nombres de red sin ruta de hoja y sin campos. Usar netlist de `kicad-cli` + `pcbnew` de KiCad sobre copia y comprobar con `verificar.py`.
- Las 55 huellas están a la izquierda del contorno (x 10–92 mm).
