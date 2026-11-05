# SPEC-0013 · Log 03 · ing-validacion (segunda validación)

Rama `spec/SPEC-0013-copia-v2`. Commit revisado: `8e0fd4e` (cambios desde `886d8e1`: `f1c9d77` y `8e0fd4e`). Sin MCP; git solo para leer; `kicad-cli` solo sobre `scratchpad\copia2\`.

## Pasos

1. `git diff 886d8e1 HEAD`: la spec corregida y los cambios de `hardware/v2` (`comment 1` y `.kicad_pro`), además de la hoja nueva `hardware/libraries/ESP-Riego.kicad_wks`.
2. Comparé con `diff` `Cajetin_Kicad.kicad_wks` y `ESP-Riego.kicad_wks`: estructura igual; quitados los textos fijos del TFG y añadidas las variables.
3. `git diff --stat 298af3c HEAD` y `v1.1-tfg HEAD` sobre `hardware/v1-tfg hardware/libraries`: solo aparece `ESP-Riego.kicad_wks`. `integridad_tfg.py`: TFG intacto. `find`: ni `.lck` ni copias de seguridad.
4. `verificar.py hardware/v2` (`ver_v2b`): ERC 1, DRC 40, paridad 77. `cmp_inf.py` frente a `ver_v1`: idéntico. `md5sum` sin cambios.
5. Copia nueva en `copia2`: netlist (`cmp_net.py` frente a la v1: idéntica tras el mapeo) y `diff` de la PCB v1 mapeada (solo cambia el `title_block`).
6. Exporté `sch_v2.pdf` (5 págs.) y `pcb_v2.pdf` (`--include-border-title`) y los revisé como imagen: cajetín v2 completo y ningún resto del TFG.
7. Grep en `hardware/v2` de `Cajetin_Kicad`, `../..` y textos del TFG. Encontré `pcbplotparams/outputdirectory "../../"` (l. 127) y `embedded_files` con `Cajetin_Kicad.kicad_wks` (l. 24013) en la PCB. Las dos vienen de la v1. No pude descomprimir el bloque incrustado (zstd), porque no hay herramienta en el equipo; lo identifico por el nombre y el tipo `worksheet`.
8. Al final leí la sección «Corrección (VAL-0013-01)» del log del autor y la contrasté.

## Resultado

Informe `gestion/informes/VAL-0013-02.md`: **APROBADO_CON_OBSERVACIONES**. Hallazgos de VAL-0013-01 cerrados; 3 observaciones B nuevas (`outputdirectory` de la PCB, hoja antigua incrustada en la PCB, y título repetido y casillas vacías en el cajetín).

Archivos de trabajo en `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\7195c1fd-8df3-41d8-89db-98db83576be9\scratchpad\` (`copia2\`, `ver_v2b\`, `cmp_net.py`, `cmp_inf.py`).
