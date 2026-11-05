# v1-tfg — proyecto del TFG en formato KiCad 10

Copia de la v1 (`Control_De_Riego`) del TFG de Joan San Bartolomé Ferri. **El diseño no se ha tocado**: solo se han cambiado las rutas de librería, la hoja de dibujo, los modelos 3D y el formato de archivo (SPEC-0009). Los hallazgos H1–H12 de `docs/01-analisis-v1.md` siguen presentes.

## Origen

`C:\Users\josan\proyectos\TFG\KiCad_PCB\Control_De_Riego` (carpeta de trabajo, igual que `PCB_FINAL.rar`) y `C:\Users\josan\proyectos\TFG\Llibreries_Kicad`. Solo se leyó del TFG; su huella (`gestion/tfg-manifiesto.json`) sigue intacta.

## Qué se copió

- Proyecto: `Control_De_Riego.kicad_pro`, `.kicad_sch` (raíz), `allimentacion`, `conectores`, `modulo_reles`, `wemos_s2mini` (`.kicad_sch`) y `Control_De_Riego.kicad_pcb`.
- `referencia/Panel_Control.kicad_sch`: hoja fuera de la jerarquía (H9), solo como referencia. Está guardada también en formato KiCad 10.
- Librerías propias en `../libraries/` con los mismos nicknames que las tablas originales (ver abajo).

No se copió: `Control_De_Riego-backups/`, `fp-info-cache`, `.kicad_prl`, `.step` del proyecto, `untitled.kicad_sch` (duplicado del Wemos) ni los `.rar`.

## Librerías (`../libraries/`)

| Nickname | Tipo | Archivo | Origen |
|---|---|---|---|
| `PS2705-1-F3-A`, `BC817-25-7-F`, `1548129`, `PRT-10811` | símbolos | `<nick>.kicad_sym` | `.lib` + `.dcm` de la librería del TFG, convertidos con `kicad-cli sym upgrade` |
| `Wemos s2 mini` | símbolo | `Wemos s2 mini.kicad_sym` | JSON de EasyEDA (`SCHLIB_WEMOS-S2-MINI-…json`) convertido tal cual con `kicad-cli sym upgrade -o` (SPEC-0010) |
| `PS2705`, `BC817-25-7`, `PRT10811`, `KiCad`, `PhoenixTerminal`, `SMMS0530-150M` | huellas | `<nick>.pretty` | `.kicad_mod` de la librería del TFG, actualizados con `kicad-cli fp upgrade` (`KiCad` = `1548129`; `SMMS0530-150M` incluye también `IND-SMD_L5.5-W5.2`) |
| `Wemos s2 mini` | huella | `Wemos s2 mini.pretty` | JSON de EasyEDA (`PCBLIB_WEMOS-S2-MINI_…json`) convertido tal cual con `kicad-cli fp upgrade -o` (SPEC-0010); no lleva modelo 3D |
| `DC-Jack` | huella | `DC-Jack.pretty/DC-IN-TH_XDJK-0051-025` | JSON de EasyEDA convertido tal cual con `kicad-cli fp upgrade -o` (SPEC-0010). Tiene 3 pads; el pad 3 es `custom` con polígono de 3,56 × 1,60 mm y taladro oblongo de 3×1 mm, equivalente a los pads 1 y 2 girados 90° (no es un artefacto). No se usa en la PCB (el jack real es `Connector_BarrelJack`) |

También `Cajetin_Kicad.kicad_wks` (hoja de dibujo) y `3d/` (`TLP185.step`, `Transistor.IGS`, `PSMT3012.STEP`, `Wemos S2 Mini V1.0.0.step`).

## Cambios de ruta

- `sym-lib-table` y `fp-lib-table`: reescritas con `${KIPRJMOD}/../libraries/...` y tipo `KiCad` (antes `Legacy` y EasyEDA, con rutas `G:/…`).
- `Control_De_Riego.kicad_pro`: `page_layout_descr_file` (dos apariciones) a `${KIPRJMOD}/../libraries/Cajetin_Kicad.kicad_wks`; `export… svg` (ruta `C:/Users/josan/Desktop/…`, último directorio de exportación) vaciado.
- `Control_De_Riego.kicad_pcb`: 10 modelos 3D con ruta `G:/…` a `${KIPRJMOD}/../libraries/3d/<archivo>` (4× TLP185, 4× Transistor, 1× PSMT3012, 1× Wemos); 43 modelos `${KICAD9_3DMODEL_DIR}` a `${KICAD10_3DMODEL_DIR}` (normalización a la variable de KiCad 10; la antigua también resuelve, así que el cambio es inocuo).
- Modelos 3D: 42 de los 53 modelos de la PCB apuntan a un `.wrl`, y KiCad 10.0.6 no instala ningún `.wrl` (solo `.step`), así que esos modelos no se ven en el visor 3D ni en el STEP (`Could not add 3D model`). Viene de la v1; se corrige en la copia de trabajo de la v2 (`.wrl` a `.step`).
- Esquemas y PCB: `kicad-cli sch|pcb upgrade --force` (esquema `20260306`, PCB `20260206`).

## Verificación

`python herramientas/verificar.py hardware/v1-tfg`:

| | Antes (copia sin migrar) | Después |
|---|---|---|
| ERC | 1 (`pin_to_pin`) | 1 (`pin_to_pin`) |
| DRC | 1 error `starved_thermal`, 39 `lib_footprint_mismatch`, 0 sin conectar | 1 error `starved_thermal`, 39 `lib_footprint_mismatch`, 0 sin conectar (40 en total, como antes) |
| Paridad | 77 (61 `LCSC Part#`, 10 `net_conflict`, 6 huellas) | 77 (igual) |

Tras SPEC-0010 el DRC coincide con la copia sin migrar: la huella `Wemos s2 mini` de la librería es la conversión del JSON de EasyEDA, igual que en el TFG, y vuelve a no coincidir con la copia de U1 en la PCB (`lib_footprint_mismatch`). Con la copia embebida en la PCB (SPEC-0009) el DRC era 39. Netlist (61 componentes, 70 redes), posiciones, pistas (262), vías (36) y zonas (3) son idénticas antes y después. Detalle en `gestion/logs/SPEC-0009/01-jr-conformidad.md`.
