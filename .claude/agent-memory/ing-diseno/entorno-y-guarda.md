---
name: entorno-y-guarda
description: Trampas de Bash/MSYS, CRLF y rutas de Windows, y límites de la guarda y de la zona de escritura de ing-diseno
metadata:
  type: reference
---

- Scripts y textos largos se escriben con Write en la carpeta temporal y se aplican con un script, no con heredocs: en un heredoc `\\` puede llegar a Python como `\`, y uno largo con comillas o Markdown falla con «unexpected EOF». Por qué: un parche dejó un byte 0x01 en `restricciones.py` que ninguna prueba vio, y varios heredocs no llegaron a ejecutarse. Fuente: SPEC-0027, SPEC-0031, SPEC-0034, SPEC-0039.
- `herramientas/`, `hardware/v2` y `docs/` están en CRLF en el árbol de trabajo: se parchean con Python en binario (no con `sed -i` de MSYS, que pasa a LF) y se comparan con `diff --no-index` de git o tras `tr -d '\r'`. Por qué: un `sed -i` dio un diff de 35 000 líneas. Fuente: SPEC-0027, SPEC-0034.
- En `python -c` o en un heredoc de Python, `/c/Users/...` se lee como `C:\c\Users\...`: se usa `C:/Users/...`. Por qué: se escribieron archivos fuera de la zona que no se pueden borrar. Fuente: SPEC-0035.
- MSYS convierte un argumento `/` (`vista.py hoja … --hoja /`) en `C:/Program Files/...`: esa orden se lanza desde PowerShell. Por qué: la raíz no se podía pintar desde Bash. Fuente: SPEC-0029.
- La guarda no resuelve `$(cygpath …)` y lo bloquea como fuera de zona: se usan rutas literales. Por qué: bloqueó parches dentro de la zona. Fuente: SPEC-0035; `.claude/hooks/guardia.py` no lo trata.
- En `gestion/logs/SPEC-NNNN/` solo se puede escribir `NN-ing-diseno.md`: los CSV de datos que la spec pida allí se dejan en la carpeta temporal y los copia el coordinador. Por qué: la guarda bloquea cualquier otro nombre. Fuente: SPEC-0039; `guardia.py`, `motivo_destino`.
- Antes de borrar o mover un archivo del repositorio, Grep de su nombre en `herramientas/pruebas/` (fuera de la zona) y, si una prueba lo usa, aviso en PENDIENTE. Por qué: borrar `colocacion-b2.csv` y `colocacion-b3.csv` deja sin datos a `ColocacionPaso5` y `ColocacionPaso6`. Fuente: SPEC-0039.
- La guarda bloquea escribir en los worktrees `KICAD_mcp-SPEC-NNNN` («fuera del repositorio»): si una orden pide un worktree, se comprueba antes que se puede escribir o se responde `bloqueado`. Por qué: la orden de SPEC-0020 pedía uno y no se pudo escribir en él. Fuente: SPEC-0020.
- La carpeta temporal la comparten los agentes que trabajan en paralelo: los scripts llevan el prefijo de la spec (`s39_*.py`). Por qué: otro agente sobrescribió un `dl.py`. Fuente: SPEC-0017.
- El diff de un `.kicad_pcb` se revisa con la opción `--patience`. Por qué: el algoritmo por defecto infla las líneas borradas. Fuente: SPEC-0022.
