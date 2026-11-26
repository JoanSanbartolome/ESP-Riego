---
name: piezas-y-huellas
description: Lo que no dice la checklist de librerías al validar símbolos, huellas, pads expuestos, 3D y polaridades (LED, TVS), con los datos de JLCPCB que cuentan
metadata:
  type: reference
---

- Polaridad de un LED: con el PDF de cada MPN, no con el de la familia (el KT-0603R numera al revés que el KT-0603YG); en PDF chinos, la barra ancha de la «T» de la vista inferior queda del lado del cátodo, y la ficha tiene que decir qué extremo de la marca es el cátodo. Por qué: el pad 1 de `LED_0603` es el cátodo. Fuente: VAL-0021-01, VAL-0022-01.
- `Device:D_TVS` es bidireccional (A1/A2): una TVS unidireccional (SMBJxxA) va con `Diode:SM6Txx A` (pin 1 = K) o `D_Zener`; en listas con piezas oficiales se mira también el símbolo heredado de las fichas viejas. Por qué: VAL-0015-01 lo pasó por alto. Fuente: VAL-0018-01.
- Huellas oficiales de TI con EP (`Texas_HTSOP-8…ThermalVias`): pad de 0,5 < patilla de 0,51, máscara y pasta del EP pequeñas y vías `*.Mask` bajo la pasta; en huellas de potencia se mira `zone_connect` (el de la huella manda sobre la zona) y los restos de la oficial (`Value` de la huella, `ki_fp_filters` del símbolo). Por qué: se apartan del *land pattern* vigente. Fuente: VAL-0018-01, VAL-0018-02.
- Placa de prueba de una huella: la oficial al lado como control (WROOM: 12 `drill_out_of_range` frente a 0); `lib_footprint_mismatch` con la oficial en una placa de 2 capas con zona en In1–30 es un artefacto. Por qué: separa el defecto de la huella del de la placa. Fuente: VAL-0021-01.
- JLCPCB solo rellena con máscara las vías sin apertura en ninguna cara y a ≥ 0,35 mm de otras aperturas; las vías-pad se rigen por «Pad Hole-to-Hole» (0,45 mm), no por la regla de vías (0,2 mm); estarcido estándar de 0,10–0,20 mm, y la pasta del EP de TI depende del espesor. Por qué: cambian la cobertura y el tapado. Fuente: VAL-0018-02, VAL-0024-01.
- Caja de un STEP: sus `CARTESIAN_POINT`, que delatan también salientes pequeños (marco a y = 5,6); el perfil de un borne, con `kicad-cli pcb render --side left` frente a la sección A-A y recortes con PIL sobre un render de 8000 px. Por qué: el render frontal no muestra la altura. Fuente: VAL-0015-01, VAL-0015-02.
- Altura de un DFN: en la vista lateral de la figura (SHT4x: 0,54 ± 0,05, no 0,5). Por qué: la tabla da el nominal redondeado. Fuente: VAL-0015-01.
- Símbolos: un esquema de prueba con los símbolos en `lib_symbols` y `kicad-cli sch erc`; en KiCad 10 los NC y los `power_out` apilados no dan `pin_to_pin`. Por qué: si no, se espera un error que no sale. Fuente: VAL-0015-01.
- Un cambio solo de nombre de pin no altera el ERC pero puede solapar (en un cuerpo de 15,24 mm caben ≈ 12 caracteres por lado); el diff de pines, con regex sobre `git show <commit>~1:…kicad_sym` (número, tipo, y, giro, largo y `hide` iguales). Por qué: el ERC no lo ve. Fuente: VAL-0016-01, VAL-0016-02.
- En un `.kicad_wks`, el origen de las cotas del cajetín es la esquina inferior derecha; se valida con `sch export pdf` de una copia y un recorte a 300 dpi. Por qué: si no, se mide al revés. Fuente: VAL-0016-01; `hardware/libraries/ESP-Riego.kicad_wks`.
- Variables 3D: se prueba con `kicad-cli pcb export step --component-filter <ref> -D VAR=/inexistente`; un 3D de respaldo se ve con el `.kicad_mod` oficial con el `model` en ruta absoluta y `vista.py huella <archivo> --3d`. Por qué: KiCad 10 resuelve por su cuenta variables de versiones anteriores. Fuente: VAL-0009-01, VAL-0029-01.
- Antes de afirmar que una pieza «se extrajo de otro sitio y difiere», `cmp` del archivo completo, no solo de los pines. Por qué: el Wemos de SPEC-0009 ya era idéntico. Fuente: VAL-0010-01.
- Campo `Datasheet` de una tabla de campos: URL o `${KIPRJMOD}`, no marcadores (la API de JLCPCB da `dataManualUrl`). Por qué: `esquema.campos` solo mira que exista. Fuente: VAL-0021-01; `herramientas/kicad/README.md`.
