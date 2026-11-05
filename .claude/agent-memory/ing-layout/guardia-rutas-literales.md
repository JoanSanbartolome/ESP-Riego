---
name: guardia-rutas-literales
description: La guardia de Bash no expande variables de shell: rm/mkdir/cp con $VAR se bloquean aunque apunten al scratchpad
metadata:
  type: feedback
---

En comandos Bash que escriben (mkdir, rm, cp, mv), usar la ruta literal completa del scratchpad o de `hardware/v2`, nunca `$S` ni otras variables.

**Why:** la guardia (hook PreToolUse) evalúa el texto del comando sin expandir variables y bloquea `$s/...` como fuera de zona (pasó en SPEC-0014).

**How to apply:** escribir rutas absolutas literales en cualquier comando que cree, borre o copie archivos.
