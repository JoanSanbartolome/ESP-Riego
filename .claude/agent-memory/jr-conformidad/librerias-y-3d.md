---
name: librerias-y-3d
description: Conversión de librerías con kicad-cli, modelos 3D que faltan en KiCad 10.0.6, STEP válidos y vías térmicas del EP
metadata:
  type: reference
---

- `kicad-cli sym upgrade -o out.kicad_sym in.lib` convierte `.lib` y lee el `.dcm` si está junto (aporta Description); el destino no debe existir y conviene convertir desde `.lib`, no desde un `.kicad_sym` hermano. Por qué: así se reproduce lo embebido en el esquema y se evita `lib_symbol_mismatch`. Fuente: SPEC-0010.
- `kicad-cli fp upgrade <dir.pretty>` actualiza el formato; en una carpeta vacía da un error inocuo. Por qué: no es un fallo real. Fuente: SPEC-0010.
- KiCad 10.0.6 no instala `.wrl`: los modelos `.wrl` no se ven. Por qué: parecía una ruta rota. Fuente: SPEC-0010.
- `kicad-cli sch|pcb upgrade --force <archivo>` migra el formato sin GUI ni MCP y crea un `.kicad_prl` que hay que borrar. Por qué: queda como archivo suelto. Fuente: SPEC-0010.
- La carpeta `3dmodels` de KiCad 10.0.6 es un subconjunto: faltan el `.step` del HRO `USB_C_Receptacle_HRO_TYPE-C-31-M-12`, el de SHT4x y el de `Fuse_Littelfuse-NANO2-451_453` (el HRO está en `share/kicad/demos/royalblue54L_feather/lib/3dmodels/Connector_USB.3dshapes/`). Por qué: la huella oficial carga sin modelo. Fuente: SPEC-0015, SPEC-0024.
- KiCad 10.0.6 no trae símbolo TPS2553/TPS2552 (sí `Interface_Expansion:TCA9554PW`): mirar con Grep en `share/kicad/symbols` antes de prometer «oficial». Por qué: la ficha prometía un símbolo inexistente. Fuente: SPEC-0031.
- Símbolos oficiales con `extends` (LM5069MM-2, USBLC6-2SC6): los pines están en el padre. Por qué: el símbolo derivado no los lista. Fuente: SPEC-0015.
- Un STEP que carga `kicad-cli pcb export step` necesita `MANIFOLD_SOLID_BREP` con `ADVANCED_FACE` + `PLANE` + `EDGE_LOOP`; `FACETED_BREP` con `FACE` simple se ignora sin error. Por qué: el modelo no sale en el 3D ni avisa. Fuente: SPEC-0015.
- 3D propio: `hardware/libraries/3d/fuentes-solidcraft/gen_*.py` + `solidcraft-cli run x.json --out y.step`; `sketch.create` en el plano `XY` con `offset` para extruir polígonos. Por qué: es la forma que dio STEP válidos. Fuente: SPEC-0021.
- En `.kicad_mod` los hijos directos se sangran con una tabulación; con dos, un replace no encaja y falla en silencio. Por qué: la huella quedaba sin cambiar. Fuente: SPEC-0024.
- Vías térmicas del EP: copiar el patrón de `Package_SO.pretty/*_ThermalVias` (vías `*.Cu` sin máscara, `pad_prop_heatsink`, `zone_connect 2`, pad B.Cu del EP); JLCPCB pide 0,2 mm de taladro a taladro y la página de Infineon del encapsulado no da vías. Por qué: es lo que aceptó la clase de fabricación. Fuente: SPEC-0024.
- El render de `kicad-cli pcb render` no modela el tapado de vías ni la polaridad del LED 0603 oficial. Por qué: el banco de render engaña en esos dos casos. Fuente: SPEC-0024.
