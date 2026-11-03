# Checklist de revisión de specs de proceso

Para specs que cambian el sistema de trabajo: agentes, hooks, scripts de `herramientas/` y convenciones.

**Versión:** v1 (2026-11-03), a partir de la propuesta de VAL-0001-01. Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Guardas y hooks

- [ ] `python -m py_compile` de `.claude/hooks/*.py`, `.githooks/*.py` y `herramientas/**/*.py` sin errores.
- [ ] `herramientas/pruebas/test_guardia.py` y `test_commit_msg.py` pasan. Cada fallo nuevo encontrado en la revisión se añade a la batería.
- [ ] La batería de la guarda cubre:
  - git directo y a través de envoltorios (`bash -c`, `cmd /c`, `pwsh -Command`, `iex`, `$(…)`);
  - el TFG por ruta absoluta, relativa (`../TFG`), por `cd` previo y por el MCP;
  - el borrado de `.git` y `.claude` enteros;
  - las escrituras por redirección dentro del repositorio;
  - falsos positivos en órdenes legítimas.
- [ ] Hooks registrados para `PreToolUse` y `PostToolUse` (en el frontmatter de cada agente) y `PostToolUseFailure` (en `.claude/settings.json`), con *matchers* que incluyan `mcp__.*`.

## Herramientas de los agentes

- [ ] Las herramientas MCP asignadas a un rol de solo lectura se han revisado por sus parámetros (`dryRun`, `fix`, `save`…), no solo por su nombre.
- [ ] Los `disallowedTools` de cada agente coinciden con su dominio y ningún agente tiene `Agent`.

## Efectos secundarios

- [ ] Las herramientas de verificación no modifican el proyecto que verifican: `md5sum` antes y después.
- [ ] `python herramientas/integridad_tfg.py verificar` da el TFG intacto.

## Documentación

- [ ] `gestion/README.md` (Guardas), `CLAUDE.md` y las definiciones de los agentes dicen lo mismo que hacen los hooks, incluidos sus límites.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial, a partir de la propuesta de VAL-0001-01 |
