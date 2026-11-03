---
id: DEC-0001
titulo: Orquestación de agentes para el diseño de la v2
fecha: 2026-11-03
estado: aceptada
decide: usuario
specs: [SPEC-0001]
requisitos: []
---

# DEC-0001 · Orquestación de agentes para el diseño de la v2

## Contexto

El rediseño de la PCB tiene varias disciplinas (esquema, layout, librerías y fabricación, validación) y debe quedar trazable y auditable en cualquier momento: quién cambió qué, por qué, contra qué requisito y con qué revisión.

## Decisión

Un **coordinador** (la sesión principal de Claude Code) y cuatro **subagentes** especialistas, en modelo en estrella: los agentes no se comunican entre sí y toda orden y entrega pasa por el coordinador y por archivos del repositorio.

| Agente | Modelo · esfuerzo | Responsable de |
|---|---|---|
| coordinador | Opus | Specs, órdenes, revisión de diffs, git, tablero, decisiones, comunicación con el usuario. No diseña ni valida. |
| `ing-esquematicos` | Opus · high | Selección eléctrica, cálculos, esquemas, restricciones de layout, YAML de ESPHome |
| `ing-layout` | Opus · high | Floorplan, colocación, rutado, zonas, reglas, 3D |
| `jr-conformidad` | Sonnet · medium | Librerías, campos, aprovisionamiento LCSC, base de componentes, BOM, CPL, coherencia de docs |
| `ing-validacion` | Opus · high | Revisión contra specs y checklists, huellas nuevas contra datasheet, plan de pruebas, informes con veredicto |

Reglas de trabajo:

1. **Specs atómicas.** Cada unidad de trabajo es una spec (`SPEC-NNNN`) con un responsable, entregables y criterios de aceptación verificables.
2. **Una rama por spec** (`spec/SPEC-NNNN-<slug>`), integrada en `main` con `merge --no-ff` solo si el informe de validación es `APROBADO` o `APROBADO_CON_OBSERVACIONES`.
3. **El usuario aprueba** el desglose de cada fase, las etiquetas de hito y los push a GitHub.
4. **Commits con trailers** (`Spec`, `Agente`, `Requisitos`, `Log`, `Validacion`) validados por un hook `commit-msg`.
5. **Guardas y registro automático** con hooks: los agentes no pueden usar git de escritura ni escribir fuera de su zona, y cada acción queda anotada en `gestion/logs/auditoria/`.
6. **Un solo agente escribe en KiCad a la vez**, porque el servidor MCP de KiCad tiene estado global.
7. **Revisión independiente:** el junior no valida sus propias huellas; validación revisa los artefactos antes de leer el log del autor y aplica checklists versionadas.

## Opciones consideradas

- **Ramas:** una rama por spec (elegida), una rama por fase, o todo en `main`. La rama por spec aísla el trabajo no validado y deja una entrada en `main` por cada spec cerrada.
- **Modelos:** todos Opus, todos Sonnet, u Opus en los ingenieros y Sonnet en el junior (elegida, por equilibrio entre calidad y coste).
- **Control humano:** OK en cada merge, autonomía total, o merge validado con OK del usuario en hitos y push (elegida).
- **Auditoría:** solo logs escritos por los agentes, o logs más hooks de registro y guarda (elegida).
- **Equipos de agentes** que se comunican entre sí: descartado, porque la comunicación directa entre agentes no quedaría registrada.

## Consecuencias

- Todo el historial es consultable con git y con los logs de `gestion/`.
- Más pasos por cambio (spec, rama, validación, merge) a cambio de trazabilidad completa.
- Las specs que escriben en KiCad se ejecutan en serie.
- El manual del sistema está en `gestion/README.md`.
