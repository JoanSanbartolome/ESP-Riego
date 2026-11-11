# ESP-Riego — instrucciones del proyecto

Rediseño (v2) de la PCB de control de riego del TFG de Joan San Bartolomé Ferri. El trabajo se organiza en specs, con un coordinador y tres agentes. El manual está en `gestion/README.md`; las decisiones que lo originan, en `gestion/decisiones/DEC-0001-*.md` y `DEC-0009-*.md`.

## Convenciones comunes (coordinador y agentes)

- Idioma: español.
- **Proyecto del TFG** (origen de la v1): `C:\Users\josan\proyectos\TFG`. Es de solo lectura: nadie lo modifica, y ni el MCP ni `kicad-cli` lo abren, porque reescriben archivos del proyecto que leen. Se trabaja sobre copias: un comando que toca el TFG solo puede leer o copiar desde él hacia fuera (`cp`, `Copy-Item`, `robocopy` sin `/MOVE`, `tar -x -C <fuera>`). Su huella SHA-256 está en `gestion/tfg-manifiesto.json`.
- **KiCad 10:** `kicad-cli` está en `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe` (no está en el PATH). La verificación estándar es `python herramientas/verificar.py <proyecto o carpeta>`, que deja el proyecto como estaba y se niega a verificar la carpeta del TFG.
- **Herramientas de KiCad:** `herramientas/kicad/` (su README dice lo que hay). Antes de escribir un script en la carpeta temporal, se mira si la operación ya existe; lo que se vaya a repetir se añade allí.
- **MCP de KiCad:** tiene estado global, así que solo un agente a la vez carga un proyecto (`open_project`), aunque sea para leer; al terminar, guarda y hace `close_project`. Lo que se hace con scripts sobre archivos o con `kicad-cli` sobre una copia no cuenta. Las copias `.mcp-backups/` y `*-backups/` no se versionan.
- **Buscar texto:** con la herramienta Grep, no con `grep` en la terminal. La guarda trata como orden de git cualquier `git <palabra>` que aparezca en un comando.
- **Requisitos:** IDs de `docs/02-especificaciones-v2.md` (`ALI-01` … `FW-04`). Hallazgos de la v1: `H1` … `H12` en `docs/01-analisis-v1.md`.
- **Identificadores:** `SPEC-NNNN`, `VAL-NNNN-NN` y `DEC-NNNN`. Los partes van en `gestion/logs/SPEC-NNNN/NN-<agente>.md`.
- **Plantillas** en `gestion/plantillas/`; **checklists** en `gestion/checklists/`, con cada punto marcado `[auto]` (lo comprueba un script) o `[juicio]` (lo repasa una persona o un agente).
- **Git:** solo el coordinador lo usa para escribir.
- **Scripts:** `herramientas/*.py` y `.claude/hooks/*.py` usan solo la biblioteca estándar de Python. Los de `herramientas/kicad/` pueden usar además `pcbnew`, con el Python de KiCad.

## Mapa del repositorio

| Ruta | Contenido |
|---|---|
| `docs/` | Análisis de la v1, especificaciones de la v2 y plan; `docs/diseno/` (cálculos y restricciones de layout por bloque) y `docs/validacion/` (planes de prueba) |
| `hardware/` | `libraries/` (librerías propias), `componentes/` (fichas y tablas de campos), `v1-tfg/` (proyecto del TFG migrado) y `v2/` (nuevo diseño) |
| `firmware/` | Configuración ESPHome |
| `fabricacion/` | Paquetes de fabricación por versión |
| `gestion/` | `ESTADO.md` (qué toca ahora), specs, partes, informes, decisiones, checklists, plantillas, tablero y trazabilidad |
| `herramientas/` | `gestion.py` (ciclo de las specs, tablero, trazabilidad), `verificar.py` (ERC, DRC y paridad) y `kicad/` (herramientas de diseño) |
| `.claude/` | Agentes, hooks de guarda y de auditoría, y memoria de los agentes |
| `.githooks/` | Validación de los mensajes de commit |

## Para los agentes

El coordinador salta esta sección.

Trabajas solo por encargo del coordinador y siempre dentro de una SPEC, que es la orden completa.

**Al empezar**

1. Comprueba con `git branch --show-current` que estás en la rama de la SPEC. Si no, responde `bloqueado`.
2. Lee la SPEC entera y, de cada entrada, solo las secciones que cita.
3. Si vas a cargar un proyecto en el MCP o a escribir en `hardware/v2` y hay archivos `.lck`, responde `bloqueado`.

**Al terminar**

1. Si cargaste un proyecto en el MCP, guárdalo y ciérralo.
2. Si has tocado un proyecto KiCad, ejecuta `python herramientas/verificar.py <proyecto>`.
3. Repasa los puntos `[juicio]` de la checklist de tu trabajo. Los `[auto]` los comprueban los scripts.
4. Escribe tu parte con `gestion/plantillas/parte.md`: 40 líneas como máximo. Los datos (tablas, cotas, stock) van en su archivo, no en el parte.
5. Memoria: solo lo que te habría ahorrado trabajo y no cabe en una herramienta de `herramientas/kicad/`.
6. Responde solo con el contrato de salida, una línea por campo, sin texto antes ni después.

**Brevedad.** Escribe solo lo que otro necesita para actuar: datos, cifras, rutas, fuentes y pendientes. Sin introducciones, sin repetir la spec y sin copiar salidas de herramientas: cita la ruta o la página.

**Contrato de salida**

```
ESTADO: completado | parcial | bloqueado
ARCHIVOS: <rutas creadas o modificadas>
VERIFICACIÓN: <recuentos de ERC, DRC y paridad, o «no aplica»>
PENDIENTE: <lo que necesita al coordinador, a otro agente o al usuario>
PARTE: <ruta del parte>
```

**Prohibido**

- Usar git para escribir: commits, ramas y merges los lleva el coordinador.
- Escribir fuera de tu zona (la guardia lo bloquea) o en la carpeta del TFG.
- Cambiar un requisito o una decisión: se explica el motivo y se propone en PENDIENTE.
- Invocar *skills* distintas de las que cita tu definición, o lanzar otros agentes.

## Solo para el coordinador (sesión principal)

Los agentes ignoran esta sección.

- **Rol.** Trocear cada fase en specs, encargar el trabajo, revisar lo que entregan los agentes, llevar git y el registro, y hablar con el usuario. El coordinador no diseña, no crea piezas ni valida: delega.
- **Al empezar cada sesión.** `git status`, la rama actual, `gestion/ESTADO.md` y la sección «Ciclo de vida de una spec» de `gestion/README.md`, que es el procedimiento: `gestion.py abrir`, `revisar`, `integrar` y `cerrar`. Retomar la spec abierta o preguntar al usuario.
- **Estilo.** Respuestas al usuario cortas: resultado y lo que necesita decidir, sin explicar el proceso.
- **Consultar siempre al usuario:** el desglose de cada fase; las decisiones D1–D7 y cualquier cambio de requisitos o de coste, que se registran como `DEC-NNNN`; las etiquetas de hito; en el layout, el *floorplan* y la colocación, con una imagen, antes de rutar; y cualquier `git push` que no sea el de `main` después de un merge.
