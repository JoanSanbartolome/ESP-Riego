---
id: SPEC-0001
titulo: Sistema de orquestación de agentes
fase: 0
estado: abierta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0001-orquestacion
requisitos: []
depende_de: [SPEC-0000]
creada: 2026-11-03
cerrada:
validacion:
---

# SPEC-0001 · Sistema de orquestación de agentes

> Bootstrapping: esta spec se abre dentro de su propia rama porque crea el sistema que define cómo se abren las specs. A partir de SPEC-0002 se aplica el flujo completo.

## Objetivo

Poner en marcha el sistema de trabajo de [DEC-0001](../decisiones/DEC-0001-orquestacion-de-agentes.md): coordinador, cuatro agentes, specs atómicas, logs, ramas por spec, guardas y registro automático.

## Alcance

- Incluye: definiciones de agentes, `CLAUDE.md`, manual, plantillas y checklists de `gestion/`, scripts de `herramientas/`, hooks de Claude Code y de git, y actualización de `README.md` y `docs/03-plan-de-diseno.md`.
- Excluye: cualquier cambio de diseño de hardware y la importación de la v1 (SPEC-0002).

## Entradas

- `gestion/decisiones/DEC-0001-orquestacion-de-agentes.md`
- `docs/02-especificaciones-v2.md` (IDs de requisitos para la trazabilidad)
- `docs/01-analisis-v1.md` (recuentos de referencia: ERC 1, DRC 40, paridad 77)

## Entregables

- `.claude/agents/`: `ing-esquematicos.md`, `ing-layout.md`, `jr-conformidad.md`, `ing-validacion.md`
- `.claude/hooks/`: `guardia.py`, `auditoria.py`; `.claude/settings.json`
- `.githooks/`: `commit-msg`, `commit_msg.py`
- `herramientas/`: `gestion.py`, `verificar.py`, `integridad_tfg.py`, `revisar_zonas.py` y las baterías `pruebas/test_guardia.py` y `pruebas/test_commit_msg.py` (añadidos tras VAL-0001-01)
- `CLAUDE.md`
- `gestion/`: `README.md`, `plantillas/`, `checklists/` (incluida `proceso.md`), `TABLERO.md`, `TRAZABILIDAD.md` y `tfg-manifiesto.json`
- `README.md` y `docs/03-plan-de-diseno.md` actualizados

## Criterios de aceptación

- [ ] Los 4 agentes tienen el modelo, esfuerzo, herramientas, memoria y hooks de DEC-0001.
- [ ] `ing-validacion` no tiene ninguna herramienta MCP de KiCad que modifique el diseño.
- [ ] Ningún agente puede lanzar otros agentes (`Agent` fuera de `tools`).
- [ ] `guardia.py` bloquea git de escritura, escrituras fuera de zona y comandos destructivos sobre la carpeta del TFG, y deja pasar las operaciones permitidas.
- [ ] `auditoria.py` añade una línea JSONL por acción.
- [ ] El hook `commit-msg` exige formato de asunto, y los trailers `Spec`/`Agente` en ramas `spec/*` y `Spec`/`Validacion` en merges a `main`.
- [ ] `gestion.py` genera `TABLERO.md` y `TRAZABILIDAD.md`, esta última con los 61 requisitos de `docs/02`.
- [ ] `verificar.py` reproduce sobre una copia del proyecto del TFG los recuentos del análisis (ERC 1, DRC 40, paridad 77).
- [ ] Pruebas en vivo: los agentes se cargan, la guardia bloquea un `git commit` de un agente y los agentes de diseño acceden al MCP de KiCad.
- [ ] `README.md` y `docs/03-plan-de-diseno.md` enlazan al manual del sistema.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-03 | usuario | Aprueba el plan de orquestación | DEC-0001 |
| 2026-11-03 | coordinador | Abre la spec en su rama | `spec/SPEC-0001-orquestacion` |
| 2026-11-03 | jr-conformidad, ing-esquematicos, ing-layout | Pruebas en vivo de carga, MCP y guardia | `gestion/logs/SPEC-0001/01-jr-conformidad.md` |
| 2026-11-03 | ing-validacion | Primera revisión: RECHAZADO (2 A, 9 M, 8 B) | [VAL-0001-01](../informes/VAL-0001-01.md) |
| 2026-11-03 | coordinador | Corrige los hallazgos 01–19 de VAL-0001-01 | commits `fix(...)` de la rama |
| 2026-11-03 | jr-conformidad | Prueba en vivo con las definiciones nuevas | `gestion/logs/SPEC-0001/03-jr-conformidad.md` |
| 2026-11-03 | ing-validacion | Segunda revisión: RECHAZADO (2 A, 2 M, 6 B) | [VAL-0001-02](../informes/VAL-0001-02.md) |
| 2026-11-03 | usuario | Confirma que mantiene su propia copia del TFG fuera del sistema | respuesta en la sesión |
| 2026-11-03 | coordinador | Corrige los hallazgos 01–09 de VAL-0001-02; las ofuscaciones con variables quedan como límite documentado | commits `fix(...)` posteriores a `a42e462` |
