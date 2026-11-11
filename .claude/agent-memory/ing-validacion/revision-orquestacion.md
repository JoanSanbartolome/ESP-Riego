---
name: revision-orquestacion
description: Cómo revisar cambios de agentes, guarda y gestion.py (VAL-0026-01): sondas adversarias contra la guarda comparadas con la versión anterior, ciclo abrir/cerrar en copia, lista de herramientas frente al servidor MCP
metadata:
  type: feedback
---

- **Guarda nueva = regresiones posibles.** Además de la batería, lanzo sondas con `test_guardia.ejecutar(agente, "Bash", {"command": c}, auditoria_temporal)` y las repito con la guarda de la versión anterior (`git show <sha>:.claude/hooks/guardia.py`, con `RAIZ` y `TEMPORAL` cambiados por `sed` y `G.GUARDIA` apuntando a la copia). Lo que antes bloqueaba y ahora pasa es el hallazgo. En VAL-0026-01 salieron los heredocs (`| bash`, `$(…)` sin comillas, `<<` entre comillas, delimitador con guion) y las variables reasignadas.
- Las sondas con la ruta del TFG en un heredoc de Bash las bloquea la guarda: escribo el script con Write y construyo `"TF" + "G"`.
- **Ciclo en copia:** `test_gestion.preparar()` crea el repositorio temporal; con `gestion(tmp, …)` y `escribir(tmp, …)` recorro nueva-spec → abrir → integrar → cerrar sin git propio. Comparo los commits con los de `60cec8d` (abrir) y `ceb209c`/`ec6a400` (cerrar).
- **Herramientas de los agentes:** cruzo cada `mcp__kicad__x` con `KiCAD-MCP-Server/src/tools/*.ts` (`.tool("x"`), 247 el 2026-11-11; las 12 de la interfaz gráfica son las 11 de `gui-driver.ts` más `launch_kicad_ui`.
- **Prueba en vivo propia:** Write fuera de zona (queda una línea `ok:false` en la auditoría versionada, inevitable) y `close_project` sin `save:false`, que se bloquea con el MCP descargado.
- `uniq IN OUT` y `tree -o` pasan directos y dentro de `find -exec` (limite antiguo, no regresión).
- **Revalidación de la guarda (VAL-0026-02):** repetir las sondas anteriores y probar formas nuevas (shell invocada con `env -i`, `busybox sh`, `$SHELL`, `>(bash)`, `eval "$(cat <<…)"`, `||` seguido de `&&`) y falsos positivos (heredoc sin comillas con `>` y backticks, programas fuera de `cat`/`tee`/intérpretes). Salieron solo B, ofuscaciones deliberadas.
