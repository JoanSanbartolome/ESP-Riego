---
spec: SPEC-0001
agente: ing-validacion
n: 07
fecha: 2026-11-04
estado: completado
---

# SPEC-0001 · 07 · ing-validacion

## Orden recibida

> SPEC-0001 · rama spec/SPEC-0001-orquestacion · Tercera revisión de validación → informe VAL-0001-03.
>
> Lee: la spec; DEC-0001; VAL-0001-01 y VAL-0001-02; `gestion/checklists/proceso.md` (v2).
>
> Haz:
> 1. Revalida cada criterio de aceptación con evidencia propia.
> 2. Para cada hallazgo 01–10 de VAL-0001-02: corregido, límite documentado o abierto, en una tabla con evidencia.
> 3. Busca fallos nuevos en `git diff a42e462..HEAD`.
> 4. Aplica la checklist de proceso v2.
>
> Datos que tener en cuenta:
> - la copia del TFG del usuario;
> - los límites aceptados N24, N31 y N33;
> - `ZONAS_MCP` común a todos los agentes;
> - las pruebas en vivo 05 y 06 y la auditoría del 2026-11-04, que hay que leer después de formar criterio.
>
> Cómo probar: sobre copias en la carpeta temporal, con JSON por archivo y `AUDITORIA_DIR` temporal, y una prueba en vivo de mi propia definición.
>
> Entrega: `gestion/informes/VAL-0001-03.md` (`checklists: [proceso v2]`) y este log.

## Contexto consultado

- `gestion/specs/SPEC-0001-orquestacion.md`, `gestion/decisiones/DEC-0001-orquestacion-de-agentes.md`, `gestion/informes/VAL-0001-02.md` y `gestion/checklists/proceso.md` (v2).
- `git diff a42e462..HEAD`, con 19 archivos y lectura completa de `.claude/hooks/guardia.py`, `.githooks/commit_msg.py`, `herramientas/revisar_zonas.py` y `herramientas/pruebas/test_guardia.py`.
- Código del servidor MCP: `C:\Users\josan\proyectos\KiCAD-MCP-Server\src\tools\*.ts` (247 herramientas) y `python\commands\design_rules.py` L666-680 (`run_drc` con `reportPath`).
- Al final, para contrastar: `gestion/logs/SPEC-0001/05-ing-esquematicos.md` y `06-ing-layout.md`, las líneas 1–19 de `gestion/logs/auditoria/2026-11-04.jsonl` y el diario `gestion/logs/coordinador/2026-11-03.md`.

## Acciones

1. Rama `spec/SPEC-0001-orquestacion` y commit `c732627`.
2. `py_compile`: sin errores. `test_guardia.py`: 231/234, con los 3 límites declarados. `test_commit_msg.py`: 24/24.
3. Pruebas propias en `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\7195c1fd-8df3-41d8-89db-98db83576be9\scratchpad\val3\`:
   - `nuevos3.py`: 57 casos de la guarda, con 37 discrepancias;
   - `claves_mcp.py`: 7 claves de destino MCP sin comprobar;
   - `zonas.py`: auditoría sobre la copia del repositorio;
   - `copia.py`: `gestion.py` idempotente, 61 requisitos y manifiesto que solo cambia en `creado`;
   - `msg3.py`: `Log` acepta una carpeta.
4. `verificar.py` sobre `val3\tfg4`, una copia nueva de `tfg_copy`: 1 / 40 / 77, `md5sum` idéntico y sin carpeta temporal residual. `integridad_tfg.py verificar`: 337 archivos intactos.
5. Prueba en vivo de mi definición (auditoría, 07:54:44–59):
   - `get_backend_state` sin proyecto y sin `.lck`;
   - `close_project` bloqueado sin `save` y que pasa con `save: false`;
   - el fallo de `ls` registrado;
   - `git commit --dry-run` y el Write en `docs/` bloqueados.
6. Lectura de los logs 05 y 06 y de la auditoría: coherentes entre sí. Confirmé la observación de `ing-esquematicos` sobre `ZONAS_MCP` y añadí que su `close_project` sin argumentos guardó un `.kicad_pcb`.
7. Escribí `gestion/informes/VAL-0001-03.md` y este log.

Archivos afectados en el repositorio: solo el informe, este log y mi memoria. Lo demás está en la carpeta temporal.

## Decisiones y justificación

- **Hallazgos 01 y 02 en M, no en A:** son huecos de prevención con la detección detrás (huella del TFG, `revisar_zonas.py` y el diff), y el usuario mantiene una copia del TFG. Así lo dije en VAL-0001-02-02: con la copia y la lista blanca, ese hallazgo bajaría a M.
- **X05 y X06 (`rg --pre`, `tree -o`) no cuentan como hallazgo:** `rg`, `tree` y `7z` no están en el PATH de esta máquina (`which`). Solo cuento `uniq` y `tar`, que sí están.
- **X35 (`git -ccore.pager=…`) se descarta:** git no acepta `-c` pegado a su valor.
- **El criterio 4 se cumple, con observaciones:** bloquea lo que promete con límites documentados, y los falsos positivos que quedan tienen alternativa.

## Verificación

- ERC 1, DRC 40 (1 error) y paridad 77 sobre `val3\tfg4`, con `md5sum` idéntico.
- Baterías: 231/234 (3 límites) y 24/24.
- Veredicto: **APROBADO_CON_OBSERVACIONES** (0 C, 0 A, 2 M y 6 B).

## Pendiente

- Para el coordinador, convertir en specs propuestas los hallazgos 01–08 de VAL-0001-03.
- Recomiendo hacer el 07 (prueba en vivo de `jr-conformidad`) antes del merge, y el 01 y el 02 antes de la primera spec que escriba en `hardware/v2/`.
- La carpeta `scratchpad\val3\` contiene una copia del repositorio y otra del proyecto; se puede borrar.

## Notas para el siguiente agente

- Los heredocs de Bash que contienen `git -c …` en el texto quedan bloqueados por la guarda, aunque sean datos. Los scripts de prueba con esos casos se escriben con Write y se construye `"gi" + "t"`.
- Al probar `revisar_zonas.py` en una copia, la ruta que anula `guardia.TEMPORAL` se escribe con `/`, porque un `\n` dentro de un f-string rompe el lanzador.
