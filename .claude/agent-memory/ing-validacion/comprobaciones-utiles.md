---
name: comprobaciones-utiles
description: Trampas comprobadas en el MCP de KiCad, verificar.py, los hooks y la auditoría de ESP-Riego, para revisar herramientas, guardas y verificaciones (VAL-0001-01 y VAL-0001-02)
metadata:
  type: feedback
---

Hay que juzgar las herramientas del MCP de KiCad por sus parámetros, no por su nombre. Para verlos, se cargan con ToolSearch "select:...". La lista completa de herramientas y sus esquemas `zod` están en `C:\Users\josan\proyectos\KiCAD-MCP-Server\src\tools\*.ts` (247 herramientas el 2026-11-03).

**Por qué:** en VAL-0001-01, el diario del coordinador daba como "de consulta" las 74 herramientas de ing-validacion, y tres escriben: `lint_schematic_cosmetic` (dryRun es false por defecto), `lint_offgrid` (fix) y `close_project` (save es true por defecto).

**Cómo aplicarlo:**
- Cuando revise listas de herramientas de roles de solo lectura, miro los parámetros.
- Yo mismo uso siempre `close_project` con `save: false`.
- `open_project` cambia el estado global del MCP: es un uso exclusivo de KiCad, aunque solo se vaya a leer.
- Cruzo `disallowedTools` con el código del servidor: un nombre inexistente no protege nada, y hay herramientas con nombre inocente que escriben en la PCB (`batch_move_components` guarda por defecto).

Otras trampas comprobadas el 2026-11-03:
- **`kicad-cli` reescribe el `.kicad_prl`** del proyecto que verifica. Desde VAL-0001-02, `verificar.py` lo restaura, pero lo sigo comprobando con `md5sum` antes y después, sobre una copia nueva.
- **`verificar.py --salida`:** para mis verificaciones, uso siempre una carpeta nueva.
- **`PostToolUse` no se dispara si la herramienta falla:** hace falta `PostToolUseFailure` (ahora en `settings.json`).
- **Para probar la guardia sin riesgo:** una batería en Python que pase el JSON por archivo con `AUDITORIA_DIR` temporal; en vivo, `git commit --dry-run`.
- **Las guardas MCP basadas en "cualquier cadena con forma de ruta" dan falsos positivos:** orígenes de solo lectura (librería oficial en Program Files), `${KIPRJMOD}`, `${KICAD10_3DMODEL_DIR}`, textos, nombres de red y valores con `/`. Pruebo siempre **llamadas legítimas** de escritura de cada agente de diseño, no solo los bloqueos.
- **Las guardas por lista negra de órdenes se eluden** con órdenes no listadas (`find -delete`, `rsync --delete`, `Get-ChildItem | Remove-Item`, `perl -pi`, `tar -C`, `Export-Csv`) y con las redirecciones de segmentos que se saltan con `continue` (`git show HEAD:x > x`, `bash -c "…" > x`).
- **La guardia no expande variables:** en mis órdenes uso rutas literales (`$S/x` se bloquea como relativa).
- **`revisar_zonas.py` sobre una copia en %TEMP% no detecta nada**, porque `motivo_destino` exime primero la carpeta temporal. Para probarlo hay que anular `guardia.TEMPORAL` (ejemplo en `scratchpad\val2\zonas_copia.py`).
- **El TFG no tiene copia:** su `.git` no tiene commits ni remoto. Cualquier elusión de la guardia sobre el TFG es irreparable, y la huella solo la detecta. Para leer su git, uso `git --no-optional-locks`.
- **Para simular un merge a `main` con `commit_msg.py`:** basta con usar `test_commit_msg.preparar()` y `probar()` de la batería versionada, que crean un repositorio temporal con `MERGE_HEAD`.
