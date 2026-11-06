---
spec: SPEC-0019
agente: ing-esquematicos
n: 04
fecha: 2026-11-06
estado: completado
---

# SPEC-0019 · 04 · ing-esquematicos

## Orden recibida

SPEC-0019 · rama spec/SPEC-0019-hoja-alimentacion (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/informes/VAL-0019-01.md (02, 03) · Haz: 02 cambiar la huella de U1 a `Package_DFN_QFN:Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm` (sin vías; las vías 0,3/0,6 al EP las pone el layout, SLVSE94G p. 39) en la hoja y en alimentacion.md §7, con nota en §8; revisa que ninguna otra pieza de la hoja use una huella *_ThermalVias con vías < 0,3/0,6; 03 alinear la huella de F1 en §3.2 con §7. No toques la PCB. Único usuario de KiCad; save_project y close_project al terminar. · Entrega: hoja + alimentacion.md + log gestion/logs/SPEC-0019/04-ing-esquematicos.md. Brevedad: solo contrato de salida; log telegráfico.

## Contexto consultado

- `gestion/informes/VAL-0019-01.md` (02, 03).
- `hardware/v2/alimentacion.kicad_sch`, `docs/diseno/alimentacion.md` §3.2, §7, §8.
- KiCad 10 `Package_DFN_QFN.pretty/Texas_RGE0024H_…EP2.7x2.7mm.kicad_mod` (0 pads `thru_hole`, EP = pad 25 SMD).
- `hardware/libraries/esp-riego.pretty/*.kicad_mod` (taladros).

## Acciones

- 02: `edit_schematic_component` U1 → `Package_DFN_QFN:Texas_RGE0024H_VQFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm`. Diff: 1 línea (instancia). Sin `open_project` (la herramienta edita el `.kicad_sch` directamente; así no se carga ni se reescribe la PCB).
- 02: `alimentacion.md` §7 (fila U1, huella + motivo) y §8 (fila «U1 EP, U2 EP»: vías 0,3/0,6 al EP las pone el layout, SLVSE94G p. 39; U2 ya las trae).
- 02: otras huellas con taladro en la hoja:
  - ninguna otra `*_ThermalVias`;
  - U2 `esp-riego:Texas_DDA0008B_…`: 8 vías 0,3/0,6 → cumple FAB-02;
  - J1 (taladro 1,3) y TP4 (`TestPoint_THTPad_D2.0mm_Drill1.0mm`): no son vías, cumplen.
- 03: `alimentacion.md` §3.2 → `esp-riego:Fuse_Littelfuse-NANO2-451_453`, igual que §7 y la hoja.

## Decisiones y justificación

- `lib_symbols` (l. 2130) conserva el `Footprint` por defecto del símbolo de la librería (`_ThermalVias`): es la copia en caché de `Power_Management:TPS26632RGE`. Si se cambiara, el ERC daría `lib_symbol_mismatch`. Lo que va a la PCB y a la BOM es el campo de la instancia.

## Verificación

- `verificar.py hardware/v2`: ERC 0 (0/0) · DRC 0 · paridad 55 `missing_footprint` (las 55 piezas de la hoja; falta la sincronización, VAL-0019-01-01, a cargo de ing-layout).
- MCP: no había proyecto cargado; `close_project` sin guardar. Sin `save_project`: no había nada abierto.

Checklist `esquema.md` v5 (solo lo que afecta a este cambio):

- Estructura / ERC: cumple (0).
- Estructura / referencias: sin cambios.
- Campos / huella existe (KIC-01): cumple (oficial KiCad 10).
- Campos / FAB-05: sin cambios en U1 (LCSC C1850278, MPN TPS26632RGER).
- Entregables / restricciones de layout: §8 actualizada (vías del EP de U1).
- Resto (cálculos, alimentación, MCU, salidas): no aplica; ningún valor ni ninguna red cambia (validados en VAL-0019-01).
- Paridad: pendiente (VAL-0019-01-01).

## Pendiente

- jr-conformidad: `hardware/componentes/TPS2663.md` l. 11 → huella sin vías (VAL-0019-01-02).
- ing-layout: sincronizar sin colocar (VAL-0019-01-01) y, al colocar U1, poner vías de 0,3/0,6 en el EP (§8).
- Coordinador: propuesta de checklist «`*_ThermalVias` cumplen FAB-02» (VAL-0019-01).

## Notas para el siguiente agente

- Las huellas oficiales `*_ThermalVias` de KiCad usan vías de 0,2/0,5: no cumplen FAB-02.
