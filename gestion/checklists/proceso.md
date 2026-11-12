# Checklist de revisión de specs de proceso

Para specs que cambian el sistema de trabajo: agentes, hooks, scripts de `herramientas/` y convenciones.

**Versión:** v7 (2026-11-12). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

`[auto: X]`: lo comprueba X y nadie lo repasa a mano. `[juicio]`: lo repasan el autor, antes de entregar, y validación.

## Guardas y hooks

- [ ] [auto: py_compile] `python -m py_compile` de `.claude/hooks/*.py`, `.githooks/*.py` y `herramientas/**/*.py` sin errores.
- [ ] [auto: baterías] `herramientas/pruebas/test_guardia.py`, `test_commit_msg.py` y `test_gestion.py` pasan; si cambian `herramientas/kicad/` o `verificar.py`, también `test_kicad.py`. Cada fallo nuevo encontrado en la revisión se añade a la batería. Los límites aceptados se marcan en `LIMITES` y se documentan en `gestion/README.md`: la batería falla si el manual no cita alguno.
- [ ] [auto: test_gestion.py] `abrir`, `integrar` y `cerrar` dejan los trailers que leen `commit-msg` y la trazabilidad (`Spec`, `Agente`, `Requisitos`, `Validacion`, `Rama`).
- [ ] [juicio] Cada heurística nueva de la guarda se prueba con sondas adversarias (comillas, delimitadores, tuberías hacia una shell, expansiones dentro del texto que se salta) y se compara con la versión anterior: lo que antes se bloqueaba y ahora pasa se corrige o va a `LIMITES`, y cada sonda, a la batería. La revalidación de una corrección repite las sondas con formas nuevas, no solo las del informe anterior.
- [ ] [juicio] La batería de la guarda cubre:
  - git directo y a través de envoltorios (`bash -c`, `cmd /c`, `pwsh -Command`, `iex`, `$(…)`);
  - el TFG por ruta absoluta, relativa (`../TFG`), por nombre corto 8.3, por `cd` previo, por el MCP y en tuberías hacia órdenes que borran (`Get-ChildItem … | Remove-Item`, `find -delete`);
  - el borrado de `.git` y `.claude` enteros;
  - las escrituras por redirección dentro del repositorio, también tras `git` y tras los envoltorios;
  - **llamadas MCP de escritura legítimas** de cada agente de diseño: orígenes fuera del repositorio (librería oficial, descargas), valores `${KIPRJMOD}` y `${KICAD10_3DMODEL_DIR}`, y textos y valores con `/`. Todas deben pasar;
  - otros falsos positivos en órdenes legítimas.
- [ ] [juicio] Hooks registrados para `PreToolUse` y `PostToolUse` (en el frontmatter de cada agente) y `PostToolUseFailure` (en `.claude/settings.json`), con *matchers* que incluyan `mcp__.*`.

## Herramientas de los agentes

- [ ] [juicio] Las herramientas MCP asignadas a un rol de solo lectura se han revisado por sus parámetros (`dryRun`, `fix`, `save`…), no solo por su nombre.
- [ ] [juicio] Las herramientas de cada agente (lista blanca o `disallowedTools`) coinciden con su dominio y ningún agente tiene `Agent`.
- [ ] [juicio] Tras cambiar la definición de un agente (herramientas, `disallowedTools`, *matchers*), hay una **prueba en vivo de ese agente**, en una sesión nueva: una escritura dentro de su zona pasa, una fuera se bloquea y una herramienta que no está en su lista no aparece.

## Efectos secundarios

- [ ] [juicio] Las herramientas de verificación no modifican el proyecto que verifican: `md5sum` antes y después.
- [ ] [juicio] En una spec que copia o renombra un proyecto, un `diff` frente al origen, con los nombres nuevos aplicados, muestra solo lo que la spec permite; lo heredado sin cambios (p. ej. `outputdirectory`, `embedded_files`) se busca a propósito.
- [ ] [juicio] En una spec de limpieza, el inventario de lo retirado se coteja con la netlist del estado de partida (referencias, valores y redes), no solo con recuentos.
- [ ] [juicio] Cuando un log justifica una desviación con «no se convierte» o «no resuelve», validación la reproduce con una orden concreta.
- [ ] [auto: commit-msg en el merge] `python herramientas/integridad_tfg.py verificar` da el TFG intacto.
- [ ] [juicio] Existe una copia recuperable del TFG (la mantiene el usuario).
- [ ] [auto: gestion.py revisar] `herramientas/revisar_zonas.py` confirma que la auditoría solo ha crecido. Para probarlo en una copia del repositorio dentro de la carpeta temporal, hay que anular la exención de esa carpeta con `GUARDIA_TEMPORAL`.

## Documentación

- [ ] [juicio] `gestion/README.md` (Guardas), `CLAUDE.md` y las definiciones de los agentes dicen lo mismo que hacen los hooks, incluidos sus límites.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial, a partir de la propuesta de VAL-0001-01 |
| v2 | 2026-11-03 | Propuestas de VAL-0001-02: MCP legítimo en la batería, redirecciones y tuberías, prueba en vivo tras cambiar un agente, auditoría que solo crece, copia del TFG |
| v3 | 2026-11-05 | Propuestas de VAL-0009-01, VAL-0013-01 y VAL-0014-01: diff frente al origen en copias, inventario frente a la netlist de partida y reproducción de las justificaciones |
| v4 | 2026-11-11 | DEC-0009: cada punto marcado `[auto]` o `[juicio]`; agentes y baterías nuevos |
| v5 | 2026-11-11 | Propuestas de VAL-0026-01: sondas adversarias para cada heurística nueva de la guarda, límites citados en el manual, trailers de `abrir` y `cerrar`, y la copia del TFG separada de su huella |
| v6 | 2026-11-11 | Propuesta de VAL-0026-02: la revalidación de una corrección de la guarda repite las sondas con formas nuevas |
| v7 | 2026-11-12 | SPEC-0027: batería `test_kicad.py`; la leyenda ya no cita `[auto: pendiente]` |
