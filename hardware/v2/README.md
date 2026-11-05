# v2 — ESP-Riego (copia de trabajo)

Proyecto KiCad 10 `esp-riego`. Es una copia del diseño de la v1 (`hardware/v1-tfg/`, etiqueta `v1.1-tfg`, commit `ec3527c`): circuito, componentes, huellas y PCB son los de la v1. Solo cambian los nombres de proyecto, archivos y hojas, y el cajetín (título «ESP-Riego v2», revisión 2.0-dev). SPEC-0013.

## Hojas

| Hoja v1 (`Sheetname` · archivo) | Hoja v2 (`Sheetname` · archivo) |
|---|---|
| `Alimentacion` · `allimentacion.kicad_sch` | `Alimentacion` · `alimentacion.kicad_sch` |
| `ESP32_S2` · `wemos_s2mini.kicad_sch` | `MCU` · `mcu.kicad_sch` |
| `Modulo_reles` · `modulo_reles.kicad_sch` | `Salidas` · `salidas.kicad_sch` |
| `Conectores y agujeros PCB` · `conectores.kicad_sch` | `Conectores` · `conectores.kicad_sch` |

La hoja `Sensores` llega con el bloque de temperatura y humedad. Los nombres de red llevan el prefijo de la hoja nueva (`/Salidas/…`, `/MCU/…`, `/Conectores/…`).

## Cómo se trabaja

Cada bloque se sustituye con su propia spec. El layout de la PCB se rehace cuando el esquema esté estable; mientras tanto la PCB es la de la v1 y los hallazgos H1–H12 de `docs/01-analisis-v1.md` siguen presentes.

Las librerías están en `../libraries/` (tablas con `${KIPRJMOD}/../libraries/...`). Verificación: `python herramientas/verificar.py hardware/v2` (estado inicial: ERC 1, DRC 40, paridad 77, igual que la v1).
