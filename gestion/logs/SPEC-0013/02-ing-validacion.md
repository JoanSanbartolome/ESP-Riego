# SPEC-0013 · Log 02 · ing-validacion

Rama `spec/SPEC-0013-copia-v2`. Commit revisado: `e808e47`, que incluye `dd9d7a9` del coordinador. No usé el MCP. `kicad-cli` solo trabajó sobre copias en el scratchpad; `verificar.py`, sobre el repositorio, con `md5sum` antes y después.

## Pasos

1. Leí la spec, `CLAUDE.md`, `docs/02` (KIC-01, KIC-02), `docs/03` (fases 2–4) y las checklists `librerias.md` v1, `proceso.md` v2 y `esquema.md` v4 (estructura).
2. `find hardware`: sin `.lck`, `*-backups`, `.mcp-backups`, `.kicad_prl` ni `fp-info-cache`.
3. `verificar.py hardware/v2` y `hardware/v1-tfg` (salidas `scratchpad\ver_v2` y `ver_v1`). Las dos dan ERC 1, DRC 40 y paridad 77. Con `cmp_inf.py` las comparé violación por violación como multiconjunto, con el mapeo de hojas: son idénticas. El `md5sum` de las dos carpetas no cambia.
4. Copié `hardware/{v1-tfg,v2,libraries}` a `scratchpad\copia\` y exporté las netlists con `kicad-cli sch export netlist --format kicadsexpr`. Con `cmp_net.py`: 61/61 componentes iguales en todos los campos; 70/70 redes con los mismos nodos tras el mapeo; partición de nodos idéntica. Único prefijo de red con hoja: `/Modulo_reles/` → `/Salidas/`.
5. PCB: apliqué los mapeos de hoja, de red y de `sheetfile` a la PCB v1. El `diff --strip-trailing-cr` frente a v2 solo da el `title_block`.
6. Esquemas: el `diff` de cada hoja frente a la v1 solo da el `title_block` y `(project "esp-riego")`. `.kicad_pro`: `filename`, `step`, `bom_export_filename` y `sheets`. Tablas idénticas.
7. Grep de los nombres antiguos y de rutas absolutas: limpio, salvo la tabla del README, que es intencionada.
8. `git diff 298af3c HEAD -- hardware/v1-tfg hardware/libraries` y `git diff v1.1-tfg HEAD -- …`: vacíos. `integridad_tfg.py verificar`: intacto.
9. Cajetín: miré `Cajetin_Kicad.kicad_wks` y exporté los PDF (`sch_v2.pdf`, `sch_v1.pdf`, `pcb_v2_cajetin.pdf`). La hoja de dibujo no usa `${TITLE}` ni `${REVISION}`, tiene fijo el título del TFG y pinta `comment 1` como «PROYECTO:». Resultado visible: «PROYECTO: Joan San Bartolomé Ferri» y el título del TFG, sin «ESP-Riego v2» ni «2.0-dev» (hallazgos 01 y 02).
10. Revisé el cambio de `docs/03` (`dd9d7a9`): coherente con la spec.
11. Solo al final leí el log `01-jr-conformidad.md` y la auditoría (l. 145–164). Contraste en el informe.

## Resultado

Informe `gestion/informes/VAL-0013-01.md`: **RECHAZADO**, con 1 hallazgo A, 1 M y 1 B. Criterio 4 sin cumplir. Los criterios 1, 2, 3 y 5 se cumplen.

Archivos de trabajo: `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\7195c1fd-8df3-41d8-89db-98db83576be9\scratchpad\` (`cmp_net.py`, `cmp_inf.py`, `copia\`, `ver_v1\`, `ver_v2\`).
