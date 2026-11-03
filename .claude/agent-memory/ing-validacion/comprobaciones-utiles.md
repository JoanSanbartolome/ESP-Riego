---
name: comprobaciones-utiles
description: Trampas comprobadas en el MCP de KiCad, verificar.py, los hooks y la auditoría de ESP-Riego, para revisar herramientas, guardas y verificaciones (VAL-0001-01)
metadata:
  type: feedback
---

Hay que juzgar las herramientas del MCP de KiCad por sus parámetros, no por su nombre. Para verlos, se cargan con ToolSearch "select:...".

**Por qué:** en VAL-0001-01, el diario del coordinador daba como "de consulta" las 74 herramientas de ing-validacion, y tres escriben: `lint_schematic_cosmetic` (dryRun es false por defecto), `lint_offgrid` (fix) y `close_project` (save es true por defecto).

**Cómo aplicarlo:**
- Cuando revise listas de herramientas de roles de solo lectura, miro los parámetros.
- Yo mismo uso siempre `close_project` con `save: false`.
- `open_project` cambia el estado global del MCP: es un uso exclusivo de KiCad, aunque solo se vaya a leer.

Otras trampas comprobadas el 2026-11-03:
- **`kicad-cli`, y por tanto `verificar.py`, reescribe el `.kicad_prl`** del proyecto que verifica. Solo hay que ejecutarlo sobre copias en la carpeta temporal, nunca sobre el TFG. Cuando haga falta, compruébalo con `md5sum` antes y después.
- **`verificar.py --salida <carpeta reutilizada>` puede leer informes viejos** si `kicad-cli` falla. Para mis verificaciones, uso siempre una carpeta `--salida` nueva.
- **`PostToolUse` no se dispara si la herramienta falla:** las acciones que fallan no llegan a la auditoría salvo que haya un hook `PostToolUseFailure`.
- **Para probar la guardia sin riesgo:** una batería en Python que pase el JSON por archivo con `AUDITORIA_DIR` temporal; en vivo, `git commit --dry-run`. En el VAL-0001-01 fallaron estos casos de elusión:
  - `../TFG`;
  - `cd TFG && rm`;
  - `bash -c "git commit"`, `$(…)`, `iex`;
  - `rm -rf .claude` y `rm -rf .git .claude`;
  - las redirecciones dentro del repositorio fuera de zona;
  - todo lo que pasa por el MCP, que no tiene *matcher*.
- **Para simular un merge a `main` con `commit_msg.py`:** copiar el repositorio a la carpeta temporal y escribir con Write los archivos `.git/HEAD` y `.git/MERGE_HEAD` de la copia. Así no hace falta usar git para escribir.
