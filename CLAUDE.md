# ESP-Riego — instrucciones del proyecto

Rediseño (v2) de la PCB de control de riego del TFG de Joan San Bartolomé Ferri. El trabajo se organiza en specs atómicas con un coordinador y cuatro agentes. El manual completo está en `gestion/README.md`; la decisión que lo origina, en `gestion/decisiones/DEC-0001-orquestacion-de-agentes.md`.

## Convenciones comunes (coordinador y agentes)

- Idioma: español.
- **Proyecto del TFG** (origen de la v1): `C:\Users\josan\proyectos\TFG`. Es de solo lectura: nadie lo modifica, y ni el MCP ni `kicad-cli` lo abren, porque reescriben archivos del proyecto que leen. Se trabaja sobre copias: un comando que toca el TFG solo puede leer o copiar desde él hacia fuera (`cp`, `Copy-Item`, `robocopy` sin `/MOVE`, `tar -x -C <fuera>`). Su huella SHA-256 está en `gestion/tfg-manifiesto.json`.
- **KiCad 10:** `kicad-cli` está en `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` (no está en el PATH). La verificación estándar es `python herramientas/verificar.py <proyecto o carpeta>`, que deja el proyecto como estaba y se niega a verificar la carpeta del TFG.
- **MCP de KiCad:** tiene estado global compartido (proyecto y placa cargados), así que solo un agente lo usa a la vez para cargar un proyecto, aunque sea solo para leerlo. Al terminar hay que guardar y hacer `close_project`. Las copias `.mcp-backups/` y `*-backups/` no se versionan.
- **Buscar texto:** con la herramienta Grep, no con `grep` en la terminal. La guarda trata como orden de git cualquier `git <palabra>` que aparezca en un comando.
- **Requisitos:** IDs de `docs/02-especificaciones-v2.md` (`ALI-01` … `FW-04`). Hallazgos de la v1: `H1` … `H12` en `docs/01-analisis-v1.md`.
- **Identificadores:** `SPEC-NNNN`, `VAL-NNNN-NN` y `DEC-NNNN`. Los logs van en `gestion/logs/SPEC-NNNN/NN-<agente>.md`.
- **Plantillas** en `gestion/plantillas/`; **checklists** en `gestion/checklists/`.
- **Git:** solo el coordinador lo usa para escribir. El formato de los commits está en `gestion/README.md`.
- **Scripts:** `herramientas/*.py` y `.claude/hooks/*.py` usan solo la biblioteca estándar de Python.

## Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `docs/` | Análisis de la v1, especificaciones de la v2 y plan; `docs/diseno/` (cálculos y restricciones de layout) y `docs/validacion/` (planes de prueba) |
| `hardware/` | `libraries/` (librerías propias), `componentes/` (fichas), `v1-tfg/` (proyecto del TFG migrado) y `v2/` (nuevo diseño) |
| `firmware/` | Configuración ESPHome |
| `fabricacion/` | Paquetes de fabricación por versión |
| `gestion/` | Specs, logs, informes, decisiones, checklists, plantillas, tablero y trazabilidad |
| `herramientas/` | `gestion.py` (specs, tablero, trazabilidad) y `verificar.py` (ERC, DRC y paridad) |
| `.claude/` | Agentes, hooks de guarda y de auditoría, y memoria de los agentes |
| `.githooks/` | Validación de los mensajes de commit |

## Solo para el coordinador (sesión principal)

Los agentes ignoran esta sección.

**Rol.** Trocear cada fase en specs, encargar el trabajo, revisar lo que entregan los agentes, gestionar git, mantener el registro y hablar con el usuario. El coordinador no diseña, no crea librerías ni valida: delega en el agente que corresponda.

**Al empezar cada sesión.** Mirar `git status` y la rama actual, leer `gestion/TABLERO.md` y el último `gestion/logs/coordinador/*.md`, y retomar la spec abierta o preguntar al usuario.

**Ciclo de una spec** (detalle en `gestion/README.md`):

1. Al empezar una fase, proponer al usuario el desglose en specs (`--estado propuesta`) y esperar su visto bueno.
2. Abrir en `main`:
   - `python herramientas/gestion.py nueva-spec ...`;
   - completar la spec (objetivo, entradas, entregables y criterios verificables);
   - regenerar el tablero;
   - commit `spec(SPEC-NNNN): abrir — <título>`;
   - `git switch -c <rama>`.
3. Encargar con una orden breve: `SPEC-NNNN · rama <rama> · Lee: <spec + archivos> · Haz: <paso> · Entrega: <archivos> + log NN-<agente>.md`. La spec tiene que bastar, porque el agente no ve esta conversación.
4. Revisar antes de cada commit:
   - `git status` y `git diff --stat`;
   - `python herramientas/revisar_zonas.py <agente>`: ningún archivo fuera de su zona;
   - el log presente;
   - `verificar.py` si hay cambios en KiCad;
   - las líneas nuevas de `gestion/logs/auditoria/`, sobre todo los `bloqueado` y los `ok: false`;
   - si el cambio toca hooks o scripts: `python -m py_compile` y las baterías de `herramientas/pruebas/`.
5. Hacer commits atómicos con los trailers `Spec`, `Agente`, `Requisitos`, `Log` y `Co-Authored-By`.
6. Pasar por conformidad si hay piezas nuevas o campos que revisar; después, por validación, indicando el nivel (`ligero` con `model: sonnet` para texto y revalidaciones; `completo` para piezas, esquema, layout y fabricación; DEC-0005). Antes de encargar cualquier spec, repasarla con su checklist y buscar contradicciones internas.
7. Hacer merge solo con `APROBADO` o `APROBADO_CON_OBSERVACIONES`. Las M que afecten a la spec siguiente se corrigen antes del merge; el resto de observaciones se acumulan en la spec de mantenimiento de la fase (DEC-0005). Pasos:
   - `estado: cerrada` y `validacion:` en la spec;
   - `git switch main` y `git merge --no-ff --no-commit <rama>`;
   - regenerar `tablero` y `trazabilidad` y escribir el diario;
   - commit `merge(SPEC-NNNN): <título>` con `Spec`, `Validacion` y `Rama`. El hook `commit-msg` comprueba además que el TFG sigue intacto (`herramientas/integridad_tfg.py verificar`);
   - `git branch -d <rama>`.

**Consultar siempre al usuario:**

- el desglose de cada fase;
- las decisiones D1–D7 y cualquier cambio de requisitos o de coste, que se registran como `DEC-NNNN`;
- las etiquetas de hito;
- cualquier `git push`, que además `.claude/settings.json` obliga a confirmar.

**Paralelismo.** Una sola spec con escritura en KiCad a la vez. Las revisiones que solo leen pueden ir en paralelo si no cargan un proyecto en el MCP; una revisión que hace `open_project` cuenta como uso exclusivo de KiCad. Antes de encargar una spec que use KiCad, comprobar que KiCad no tiene abierto ese proyecto (archivos `.lck`).

**Diario.** Al final de cada sesión de trabajo, escribir `gestion/logs/coordinador/AAAA-MM-DD.md` con las órdenes dadas, las decisiones, los commits y lo que queda pendiente.
