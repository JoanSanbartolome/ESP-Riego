# Checklist de revisión de specs de proceso

Para specs que cambian el sistema de trabajo: agentes, hooks, scripts de `herramientas/` y convenciones.

**Versión:** v2 (2026-11-03), con las propuestas de VAL-0001-02. Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Guardas y hooks

- [ ] `python -m py_compile` de `.claude/hooks/*.py`, `.githooks/*.py` y `herramientas/**/*.py` sin errores.
- [ ] `herramientas/pruebas/test_guardia.py` y `test_commit_msg.py` pasan. Cada fallo nuevo encontrado en la revisión se añade a la batería. Los límites aceptados se marcan en `LIMITES` y se documentan en `gestion/README.md`.
- [ ] La batería de la guarda cubre:
  - git directo y a través de envoltorios (`bash -c`, `cmd /c`, `pwsh -Command`, `iex`, `$(…)`);
  - el TFG por ruta absoluta, relativa (`../TFG`), por nombre corto 8.3, por `cd` previo, por el MCP y en tuberías hacia órdenes que borran (`Get-ChildItem … | Remove-Item`, `find -delete`);
  - el borrado de `.git` y `.claude` enteros;
  - las escrituras por redirección dentro del repositorio, también tras `git` y tras los envoltorios;
  - **llamadas MCP de escritura legítimas** de cada agente de diseño: orígenes fuera del repositorio (librería oficial, descargas), valores `${KIPRJMOD}` y `${KICAD10_3DMODEL_DIR}`, y textos y valores con `/`. Todas deben pasar;
  - otros falsos positivos en órdenes legítimas.
- [ ] Hooks registrados para `PreToolUse` y `PostToolUse` (en el frontmatter de cada agente) y `PostToolUseFailure` (en `.claude/settings.json`), con *matchers* que incluyan `mcp__.*`.

## Herramientas de los agentes

- [ ] Las herramientas MCP asignadas a un rol de solo lectura se han revisado por sus parámetros (`dryRun`, `fix`, `save`…), no solo por su nombre.
- [ ] Los `disallowedTools` de cada agente coinciden con su dominio y ningún agente tiene `Agent`.
- [ ] Tras cambiar la definición de un agente (herramientas, `disallowedTools`, *matchers*), hay una **prueba en vivo de ese agente**, con su log, que incluye una herramienta prohibida (no debe aparecer) y una herramienta de escritura permitida (debe pasar).

## Efectos secundarios

- [ ] Las herramientas de verificación no modifican el proyecto que verifican: `md5sum` antes y después.
- [ ] `python herramientas/integridad_tfg.py verificar` da el TFG intacto, y existe una copia recuperable del TFG (la mantiene el usuario).
- [ ] `herramientas/revisar_zonas.py` confirma que la auditoría solo ha crecido. Para probarlo en una copia del repositorio dentro de la carpeta temporal, hay que anular la exención de esa carpeta.

## Documentación

- [ ] `gestion/README.md` (Guardas), `CLAUDE.md` y las definiciones de los agentes dicen lo mismo que hacen los hooks, incluidos sus límites.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial, a partir de la propuesta de VAL-0001-01 |
| v2 | 2026-11-03 | Propuestas de VAL-0001-02: MCP legítimo en la batería, redirecciones y tuberías, prueba en vivo tras cambiar un agente, auditoría que solo crece, copia del TFG |
