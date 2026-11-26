---
id: SPEC-0039
titulo: Revisión general: documentación, decisiones vigentes, memorias y ruido
fase: 4
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0039-revision-general
requisitos: []
depende_de: [SPEC-0038]
creada: 2026-11-24
cerrada:
validacion:
---

# SPEC-0039 · Revisión general: documentación, decisiones vigentes, memorias y ruido

## Objetivo

Que la fase 4 parta de un repositorio sin datos superados, con estas cuatro cosas:
- **Documentos** sin menciones de piezas ni cifras sustituidas.
- **Decisiones:** una sola tabla de decisiones vigentes que se pueda comprobar.
- **Memorias** de los agentes y del coordinador depuradas con reglas fijas, de modo que dos personas que las apliquen lleguen al mismo resultado.
- **Herramientas:** ni la guarda ni `gestion.py` tienen los dos fallos que se conocen.

## Alcance

- Incluye:
  - **Paso 1 · coordinador** (`gestion/`, `docs/02`, `docs/03`, `herramientas/gestion.py`, `.claude/hooks/`):
    - **Términos superados:**
      - `gestion/logs/SPEC-0039/superados.csv`, con las columnas `antiguo`, `vigente`, `fuente` y `alcance`;
      - sale del diff de `hardware/componentes/campos-*.csv` entre la etiqueta `v2.0-sch` y `main` (Value, LCSC, MPN y huella que hayan cambiado);
      - se añaden las piezas y cifras sustituidas que citan DEC-0016 a DEC-0019 (por ejemplo, TLV1117LV, BH254V-10P, «58 objetivos» y PUNTOS 6251).
      - Esta lista es la única entrada de los barridos de los pasos 2 y 3.
    - **Decisiones vigentes:** ver «Regla de las decisiones».
    - **`docs/02` §7:** D5 y D6 según DEC-0019, con la línea en el historial. **`docs/03`:** casillas de la fase 4 según lo hecho.
    - **`gestion.py`:**
      - `integrar` cuenta solo las acciones y los minutos posteriores al último `integrar` del mismo `agent_id` (VAL-0037-01-05);
      - una comprobación `[auto]` de que `decisiones/VIGENTES.md` cita cada DEC en `aceptada` o `modificada`;
      - otra de que el `MEMORY.md` de cada memoria coincide con sus archivos.
    - **Guarda (VAL-0038-01-04):** sacar del registro de auditoría del 2026-11-23 (instancia ab5487) el comando con el que `jr-conformidad` escribió en `docs/` sin ser bloqueado. Cerrar ese caso y añadir una prueba en `herramientas/pruebas/test_gestion.py`.
    - **Memoria del coordinador**, con la «Regla de las memorias».
  - **Paso 2 · `ing-diseno`:**
    - Barrido con Grep de `superados.csv` en `docs/diseno/`, `herramientas/kicad/` y `firmware/`. Cada coincidencia se marca como `actualizar`, `histórica` u `otra placa`. Las de `actualizar` se corrigen y las `histórica` se rotulan «(hasta SPEC-NNNN)».
    - Borrar `colocacion-b`, `b2` y `b3` (`.csv` y `.png`): en `experimento-colocacion.md` y en los demás documentos que los citen, se cambia la cita por el commit en el que están.
    - Su memoria, con la «Regla de las memorias».
  - **Paso 3 · `jr-conformidad`:** el mismo barrido en `hardware/componentes/` y `fabricacion/`, y su memoria.
  - **Paso 4 · `ing-validacion`:** su memoria. Lo hace una instancia distinta de la que valida.
- Excluye:
  - **El diseño:** no se cambia, ni `hardware/v2` ni el contenido de ningún requisito.
  - **Los registros, que no se reescriben:** los informes VAL, los partes, la auditoría, el cuerpo de los DEC y el registro de las specs cerradas.
  - SPEC-0036.

## Regla de las decisiones

- **Los DEC no se reescriben.** En su frontmatter:
  - `estado` pasa a `aceptada`, `modificada` o `sustituida`;
  - se añade `modificada_por: [DEC-NNNN]`.
- **`gestion/decisiones/VIGENTES.md`:** una tabla con las columnas `tema | regla vigente (una frase) | DEC | requisitos`, ordenada por tema:
  - **temas:** orquestación, agentes, requisitos, alimentación, salidas, MCU, sensores, conectores, colocación, coste y fabricación;
  - **regla vigente:** el texto de un DEC o de una de sus secciones «Tras …» que no contradiga otro posterior;
  - **en caso de conflicto**, gana la fecha más reciente y el DEC anterior pasa a `modificada`;
  - **un DEC sin ninguna regla vigente** pasa a `sustituida`.
- **El índice de `gestion/README.md`** apunta a `VIGENTES.md`. Los agentes leen `VIGENTES.md` y no los DEC sueltos, salvo que la spec los cite.

## Regla de las memorias

**Qué se clasifica.** Cada viñeta o párrafo con una sola afirmación. Se le aplican estas pruebas en orden, y la primera que se cumple decide:

1. **OBSOLETA:** nombra un archivo, una función, una opción, una orden, una pieza (MPN o LCSC) o una cifra que Grep o Glob ya no encuentran, o que contradice el valor actual en el repositorio. → Se borra.
2. **DUPLICADA:** lo mismo ya está en `CLAUDE.md`, en `gestion/README.md`, en `herramientas/kicad/README.md`, en `.claude/agents/*.md`, en una checklist, en `docs/` o en `VIGENTES.md`. → Se borra y se anota dónde está.
3. **ESTADO:** describe el estado del proyecto (valores elegidos, qué hizo cada spec, pendientes). → Se borra: vive en `ESTADO.md`, en `docs/` y en git.
4. **RECETA:** un procedimiento de 3 pasos o más, o un script en línea, que se repite en 2 specs o más. → Pasa a una sección «Recetas» de `herramientas/kicad/README.md` (paso 2) o se propone como herramienta en PENDIENTE, y se borra de la memoria.
5. **VIGENTE:** todo lo demás. → Se queda, reescrito así: `- <hecho en una frase>. Por qué: <motivo>. Fuente: <ruta, página o SPEC>.`

**Forma de lo que queda:**
- archivos por tema, sin ninguno de tipo `project_*`;
- 40 líneas como máximo por archivo y 120 por memoria, sin contar `MEMORY.md`;
- `MEMORY.md`, con una línea por archivo;
- sin fechas relativas.

**Prueba de la clasificación:** `gestion/logs/SPEC-0039/memoria-<agente>.csv`, con una fila por afirmación y estas columnas:
- `archivo`;
- `n`;
- `resumen` (12 palabras como máximo);
- `clase`;
- `comprobación` (la orden de Grep o Glob y su resultado);
- `destino`.

## Entradas

- `gestion/decisiones/DEC-*.md` (todos), `gestion/README.md` (índice y «Ciclo de vida»), `CLAUDE.md`.
- `gestion/informes/VAL-0037-01.md` (hallazgo 05) y `VAL-0038-01.md` (hallazgos 01 y 04).
- `.claude/agent-memory/*/`, `herramientas/kicad/README.md` y `.claude/agents/*.md`.

## Entregables

- `superados.csv`, `VIGENTES.md`, el frontmatter de los DEC, `docs/02` §7 y `docs/03`.
- `gestion.py`, `guardia.py` y sus pruebas.
- Documentos barridos y los intermedios de colocación borrados.
- Las cuatro memorias depuradas y sus `memoria-<agente>.csv`.
- Los partes de cada paso.

## Criterios de aceptación

- [ ] Grep de cada `antiguo` de `superados.csv` en `docs/`, `hardware/componentes/`, `herramientas/kicad/` y `fabricacion/`: solo quedan menciones rotuladas «(hasta SPEC-NNNN)» o de otra placa, y cada una está anotada en el parte.
- [ ] `VIGENTES.md` cita todos los DEC en `aceptada` o `modificada`, y ninguna regla contradice otra. La comprobación `[auto]` pasa.
- [ ] Cada `memoria-<agente>.csv` tiene una fila por afirmación, con su clase y su comprobación. Las memorias cumplen la forma y los límites, y su `MEMORY.md` coincide con sus archivos (`[auto]`).
- [ ] `integrar` con un agente continuado anota solo la tanda nueva, con una prueba en `test_gestion.py`.
- [ ] La guarda bloquea el caso de VAL-0038-01-04, con una prueba.
- [ ] `test_gestion.py` y `test_kicad.py` pasan. `verificar.py hardware/v2` da lo mismo que en SPEC-0038: ERC 0, DRC 0 (448 sin conectar) y paridad 0.

## Plan de validación

Nivel **completo** en la guarda y en `gestion.py`, porque cambian el control de los agentes. **Ligero** en lo demás.

- Se reproduce de forma independiente:
  - las pruebas nuevas y un intento de saltarse la guarda con el caso de VAL-0038-01-04, sobre una copia;
  - el Grep de `superados.csv`.
- Por muestreo:
  - el 20 % de las filas de cada `memoria-<agente>.csv`, repitiendo su `comprobación`, y todas las filas en `VIGENTE`;
  - 5 reglas de `VIGENTES.md` frente a su DEC.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-24 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-24 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-24 | ing-diseno | paso 2 — barrido de docs/diseno, b/b2/b3 borrados, recetas y memoria | 02-ing-diseno | 382904 | 103 | 65 |
| 2026-11-24 | jr-conformidad | paso 3 — barrido de componentes y fabricación, y memoria | 03-jr-conformidad | 193260 | 105 | 11 |
| 2026-11-26 | ing-validacion | paso 4 — memoria de ing-validacion | 04-ing-validacion | 290312 | 39 | 2402 |
