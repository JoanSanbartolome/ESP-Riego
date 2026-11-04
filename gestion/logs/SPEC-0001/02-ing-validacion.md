---
spec: SPEC-0001
agente: ing-validacion
n: 02
fecha: 2026-11-03
estado: completado
---

# SPEC-0001 · 02 · ing-validacion

## Orden recibida

SPEC-0001 · rama spec/SPEC-0001-orquestacion · Revisión de validación → informe VAL-0001-01.

- **Lee:** `gestion/specs/SPEC-0001-orquestacion.md` (criterios de aceptación y entregables) y `gestion/decisiones/DEC-0001-orquestacion-de-agentes.md`.
- **Haz:** valida cada criterio de aceptación de la spec con evidencia propia. No es una spec de hardware, así que ninguna checklist aplica. Revisa además:
  - la coherencia entre DEC-0001, `CLAUDE.md`, `gestion/README.md` y las definiciones de `.claude/agents/`;
  - la calidad de los scripts de `herramientas/`, `.claude/hooks/` y `.githooks/`: errores, casos límite y huecos de la guardia.
- **Cómo probar:**
  - `verificar.py`, sobre `scratchpad\tfg_copy`;
  - `gestion.py`, solo sobre una copia del repositorio;
  - la guardia y la auditoría, con el JSON en un archivo temporal y `AUDITORIA_DIR` temporal;
  - `commit_msg.py`, con un archivo de mensaje temporal.
- **Entrega:** `gestion/informes/VAL-0001-01.md` y `gestion/logs/SPEC-0001/02-ing-validacion.md`.

## Contexto consultado

- **Spec, decisiones y sistema:**
  - SPEC-0001, DEC-0001, SPEC-0000, `CLAUDE.md`, `README.md`, `docs/03-plan-de-diseno.md` (diff con `main`) y `docs/02-especificaciones-v2.md` (recuento de ID);
  - `gestion/README.md`, plantillas, checklists, `TABLERO.md` y `TRAZABILIDAD.md`;
  - `.claude/agents/*.md`, `.claude/settings.json`, `.claude/hooks/*.py`, `.githooks/*`, `.gitattributes`, `.gitignore` y `herramientas/*.py`.
- **Esquemas de parámetros de las herramientas MCP** (`ToolSearch`), entre ellas:
  - `lint_offgrid`, `lint_schematic_cosmetic` y `close_project`;
  - `open_project` y `open_board`;
  - `validate_*`, `find_*` y `check_*`.
- **Carpeta del TFG, solo lectura:** `ls` y `md5sum -c` de `KiCad_PCB\Control_De_Riego`.
- **Al final**, para contrastar: `gestion/logs/SPEC-0001/01-jr-conformidad.md`, `gestion/logs/coordinador/2026-11-03.md` y la auditoría versionada (`git show HEAD:…jsonl`).

## Acciones

1. Rama `spec/SPEC-0001-orquestacion` comprobada. Commit revisado: `57e8448`.
2. `verificar.py` sobre `tfg_copy` y sobre una copia nueva del original (`val\tfg2`): las dos dan ERC 1, DRC 40 (1 error y 39 avisos) y paridad 77. Casos límite: `--json`, entrada `.kicad_pcb`, ruta inexistente, carpeta sin `.kicad_pro` y esquema corrupto con y sin `--salida` reutilizada.
3. `md5sum` antes y después de `verificar.py`: `kicad-cli` reescribe el `.kicad_prl`.
4. Copia del repositorio en `scratchpad\val\repo`:
   - `gestion.py tablero` y `trazabilidad` son idempotentes;
   - `nueva-spec` funciona con los casos válidos y rechaza los inválidos;
   - recuento propio de 61 requisitos.
5. `commit_msg.py`:
   - 12 mensajes en la rama `spec/*`;
   - 5 mensajes en un merge a `main` simulado en la copia (`HEAD` → `main` y `MERGE_HEAD` escritos con Write en la copia temporal; no usé git para escribir).
6. Guardia: batería propia de 90 casos (`scratchpad\val\prueba_guardia.py`) con `AUDITORIA_DIR` temporal. Hay 25 discrepancias; los 43 bloqueos dejan 43 líneas de auditoría. También probé el JSON inválido y la entrada vacía.
7. Auditoría: 6 entradas sintéticas, más las pruebas en vivo:
   - `git commit --dry-run` bloqueado y registrado;
   - Write en `docs/` bloqueado y registrado;
   - `ls` con salida 2, que no se registra.
8. Comprobé que todos los enlaces relativos de los `.md` resuelven.
9. Contrasté los resultados con los logs y el diario, y escribí el informe.

No he abierto ningún proyecto en el MCP, así que no hacía falta `close_project`.

## Decisiones y justificación

- **Hallazgo 01 de severidad A y criterio 2 incumplido:** la descripción de los parámetros del MCP muestra que tres herramientas asignadas a validación escriben, una de ellas por defecto. Se decidió por los parámetros, no por el nombre.
- **Hallazgo 02 de severidad A:** `../TFG` es la ruta relativa natural, porque el TFG está al lado del repositorio, y el TFG queda fuera de la revisión de diffs del coordinador. No hay control que lo compense.
- **Rotura de `.git` y `.claude` (hallazgo 05) como M y no como A:** el impacto es crítico, pero que un agente lo haga por accidente es poco probable. Propongo además hacer el push como copia de seguridad.
- **Criterio 5 como parcial:** las acciones que fallan son acciones y no quedan registradas.

## Verificación

```
ERC         1  (errores 0, avisos 1)        pin_to_pin [warning]
DRC        40  (errores 1, avisos 39, sin conectar 0)
Paridad    77  (61 field_mismatch, 10 net_conflict, 6 footprint_symbol_mismatch)
Guardia: 90 casos, 25 discrepancias (G30-G36, T10-T17, S03-S05, S10, Z01-Z06)
```

## Pendiente

- **Coordinador:** corregir los hallazgos 01, 02, 04, 05, 06 y 08, y el 03 (o documentar su límite), y encargar VAL-0001-02. Los demás M y B, como specs propuestas.
- **Coordinador:** decidir si la batería `scratchpad\val\prueba_guardia.py` se versiona como prueba de regresión. La carpeta es temporal.
- **Coordinador:** limpiar las carpetas temporales `C:\Users\josan\AppData\Local\Temp\verificar_*` que dejó `verificar.py` sin `--salida`.

## Notas para el siguiente agente

- `close_project` guarda por defecto: en las revisiones, usarlo siempre con `save: false`.
- `verificar.py` modifica el `.kicad_prl`: ejecutarlo solo sobre copias o sobre `hardware/`.
- `PostToolUse` no ve las acciones que fallan.
