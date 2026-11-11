---
id: SPEC-0026
titulo: Orquestación v2: roles, ciclo, registro y trámite
fase: 0
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0026-orquestacion-v2
requisitos: []
depende_de: []
creada: 2026-11-11
cerrada:
validacion:
---

# SPEC-0026 · Orquestación v2: roles, ciclo, registro y trámite

> Aplica las medidas M2 a M9 de [DEC-0009](../decisiones/DEC-0009-orquestacion-v2.md), aceptada entera por el usuario el 2026-11-11. M1 (caja de herramientas) va en SPEC-0027 y M10 en el desglose de la fase 4.

## Objetivo

El sistema de trabajo pasa a tres agentes, una spec por bloque o hito, un parte corto por intervención y el trámite del coordinador en cuatro órdenes de `gestion.py`, y cada arranque de agente deja anotado lo que ha costado.

## Alcance

- Incluye:
  - **Agentes (M2, M7, M8).** `.claude/agents/ing-diseno.md` sustituye a `ing-esquematicos.md` e `ing-layout.md`: zona `hardware/` (salvo `v1-tfg/`), `docs/diseno/`, `firmware/` y `herramientas/kicad/` (para SPEC-0027); todas las herramientas del MCP salvo las de la interfaz gráfica; `model: inherit`; cuerpo con el método de trabajo (plan, herramienta, comprobación, imagen, cuándo parar a preguntar) para esquema, piezas y layout. `jr-conformidad.md`: tipo y stock, fichas, tablas de campos, BOM, CPL y paquete de fabricación; lista blanca corta de herramientas del MCP en vez de lista negra; `sonnet`. `ing-validacion.md`: `model: inherit`, sin log propio, sigue el plan de validación de la spec. Las memorias de esquemáticos y layout se funden en `.claude/agent-memory/ing-diseno/`.
  - **Instrucciones comunes (M7).** `CLAUDE.md` recoge una sola vez el protocolo de inicio y cierre, el contrato de salida y las prohibiciones; la sección del coordinador queda en un puntero a `gestion/README.md` y a `gestion/ESTADO.md`. Las definiciones no repiten nada de eso.
  - **Ciclo (M3, M4).** `gestion/README.md`: una spec por bloque o por hito de layout con pasos internos; comprobaciones automáticas entre pasos; una validación completa al final; correcciones y revalidaciones continuando la misma instancia; instancia nueva para cada paso nuevo.
  - **Registro (M5).** `plantillas/parte.md` (40 líneas como máximo: decisiones no obvias, desviaciones, pendientes y, de la checklist, solo lo que no cumple o no aplica) sustituye a `log.md`; la ruta `gestion/logs/SPEC-NNNN/NN-<agente>.md` y el trailer `Log` no cambian. `plantillas/spec.md` gana «Plan de validación» y las columnas de tokens y acciones en el registro. `gestion/ESTADO.md` sustituye al diario: siguiente paso, pendientes del usuario y notas para layout y fabricación, tomados de los diarios del 2026-11-07 y del 2026-11-10. Las observaciones de mantenimiento acumuladas en esos diarios pasan a una spec de mantenimiento en `propuesta`.
  - **Checklists (M7).** Cada punto de las seis checklists se marca `[auto]` o `[juicio]`, con el script que cubre cada `[auto]`; los que aún no tienen script se listan para SPEC-0027. Sube la versión de cada una.
  - **Trámite y medida (M6).** `gestion.py abrir`, `revisar <agente>`, `integrar`, `cerrar` y `registrar` (fila en el registro de la spec con tokens, acciones y duración del arranque, que `integrar --tokens` anota en el mismo commit); el tablero suma tokens por spec y por agente. `auditoria.py` corta `objetivo` a 160 caracteres. `AGENTES`, `revisar_zonas.py` y `.githooks/commit_msg.py` aceptan `ing-diseno` y siguen aceptando los nombres antiguos en el historial.
  - **Guarda (M9).** Zonas de `ing-diseno`; la carpeta temporal se puede escribir aunque la ruta vaya en una variable; el código en línea que no toca el TFG pasa, y también el cuerpo de un heredoc que no va a una shell. Además, los dos falsos positivos anotados en el diario del 2026-11-10 y en las memorias: las palabras de control de la shell (`do`, `then`…) y `find -exec` con órdenes de lectura. Un caso por cambio en `herramientas/pruebas/test_guardia.py`. SPEC-0002 pasa a `descartada`.
- Excluye:
  - la caja de herramientas de `herramientas/kicad/` (SPEC-0027);
  - cualquier cambio en `docs/`, `hardware/`, `firmware/` y `fabricacion/`;
  - reescribir logs, informes o diarios anteriores;
  - endurecer o reescribir la guarda más allá de los cambios citados.

## Entradas

- DEC-0009, DEC-0001 y DEC-0005.
- `CLAUDE.md`, `gestion/README.md`, `.claude/agents/*.md`, `.claude/agent-memory/`, `gestion/plantillas/`, `gestion/checklists/`.
- `herramientas/gestion.py`, `herramientas/revisar_zonas.py`, `.claude/hooks/*.py`, `.githooks/commit_msg.py` y `herramientas/pruebas/`.
- `gestion/logs/coordinador/2026-11-07.md` y `2026-11-10.md`.

## Entregables

- Las tres definiciones de agente, `CLAUDE.md` y `gestion/README.md`.
- `gestion/plantillas/parte.md` y `spec.md`; `gestion/ESTADO.md`; las seis checklists marcadas.
- `herramientas/gestion.py` con las cinco órdenes nuevas y su batería en `herramientas/pruebas/test_gestion.py`.
- `auditoria.py`, `guardia.py`, `revisar_zonas.py` y `commit_msg.py` ajustados, con sus baterías.
- Spec de mantenimiento en `propuesta` con las observaciones acumuladas.

## Criterios de aceptación

- [ ] `.claude/agents/` tiene exactamente `ing-diseno.md`, `jr-conformidad.md` e `ing-validacion.md`; ninguna repite el protocolo, el contrato ni las prohibiciones de `CLAUDE.md`, y ninguna tiene `Agent`.
- [ ] En una sesión nueva, prueba en vivo de los tres agentes: una escritura dentro de su zona pasa, una fuera se bloquea, y `ing-diseno` escribe en `hardware/libraries/` y en un `.kicad_pcb` de una copia.
- [ ] `python -m py_compile` de hooks y scripts sin errores; `test_guardia.py`, `test_commit_msg.py` y `test_gestion.py` pasan, con los casos nuevos de la carpeta temporal y del código en línea.
- [ ] `gestion.py revisar <agente>` da su salida en 25 líneas como máximo e incluye zonas, parte, bloqueos y fallos de la auditoría y, si cambió KiCad, los recuentos de `verificar.py`.
- [ ] `gestion.py abrir` y `cerrar`, probados en una copia del repositorio, dejan el mismo resultado que los pasos 2 y 7 del ciclo actual, con los trailers que exige `commit-msg`.
- [ ] `gestion.py registrar` añade la fila al registro de la spec y el tablero muestra la suma por spec y por agente.
- [ ] `gestion/ESTADO.md` tiene 50 líneas como máximo y recoge todos los pendientes de los diarios del 2026-11-07 y del 2026-11-10.
- [ ] `gestion/README.md` y `CLAUDE.md` describen lo que hacen los hooks y los scripts, sin referencias a los agentes retirados fuera del historial.

## Plan de validación

Nivel **ligero** con la checklist de proceso v4. Se reproduce de forma independiente: las tres baterías, la prueba en vivo y `abrir` y `cerrar` en una copia. Por muestreo: la coherencia de los textos y el marcado de las checklists. La prueba en vivo y la validación se hacen en una sesión nueva, porque las definiciones de agente se cargan al arrancar.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-11 | coordinador | Crea la spec (propuesta) a partir de la revisión de la orquestación | DEC-0009 |
| 2026-11-11 | coordinador | Abre la spec: el usuario acepta la opción B completa | DEC-0009 |
| 2026-11-11 | coordinador | Implementa M2 a M9: guarda, gestion.py, tres agentes, instrucciones, plantillas, checklists, ESTADO.md y las specs 0027 y 0028 propuestas. Baterías: guarda 254/255 (N33, límite conocido), commit-msg 25/25 y gestión 27/27 | 8a3f4c0, b8ad21e, ce3d649, fc45962 |  |  |  |
| 2026-11-11 | ing-diseno | Prueba en vivo: escribe en hardware/libraries; gestion/, hardware/v1-tfg/ y herramientas/ bloqueados; copia en la carpeta temporal y texto en su .kicad_pcb por el MCP y por sed; sin Agent ni herramientas de la interfaz gráfica | auditoria/2026-11-11 | 48223 | 14 | 1 |
| 2026-11-11 | jr-conformidad | Prueba en vivo: escribe en hardware/componentes; docs/diseno/, gestion/ y herramientas/ bloqueados; sin Agent ni herramientas de símbolos, huellas o rutado | auditoria/2026-11-11 | 37231 | 8 | 0 |
| 2026-11-11 | ing-validacion | Prueba en vivo: escribe en gestion/informes; hardware/, gestion/checklists/ y docs/diseno/ bloqueados; sin Agent ni herramientas que modifican el diseño | auditoria/2026-11-11 | 37673 | 8 | 0 |
| 2026-11-11 | ing-validacion | Validación ligera: 8 criterios cumplen; 1 M (heredocs de la guarda) y 5 B | VAL-0026-01 | 179638 | 48 | 12 |
| 2026-11-11 | coordinador | Corrige VAL-0026-01: heredocs (M-01), variables en orden (B-02), find -exec uniq/tree, Requisitos en abrir (B-04), textos (B-06) y checklist de proceso v5. B-03 va a ESTADO.md y B-05 se resuelve en SPEC-0027. Baterías: guarda 270/273 (N33, K07 y HD12, límites), commit-msg 25/25 y gestión 28/28 | VAL-0026-01 |  |  |  |
| 2026-11-11 | ing-validacion | Revalidación: M-01, B-02, B-04 y B-06 corregidos; 2 B nuevas de la guarda (ofuscaciones deliberadas y falsos positivos) | VAL-0026-02 | 35121 | 14 | 6 |
