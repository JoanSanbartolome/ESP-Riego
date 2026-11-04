---
id: SPEC-0002
titulo: Guarda: claves de destino del MCP que faltan
fase: 0
estado: propuesta
responsable: coordinador
revisor: ing-validacion
rama: spec/SPEC-0002-guarda-destinos
requisitos: []
depende_de: [SPEC-0001]
creada: 2026-11-04
cerrada:
validacion:
---

# SPEC-0002 · Guarda: claves de destino del MCP que faltan

> Mínimo imprescindible de las observaciones de [VAL-0001-03](../informes/VAL-0001-03.md), por decisión del usuario de no complicar más la orquestación. Se cierra antes de la primera spec que escriba en `hardware/v2/`.

## Objetivo

Que la guarda compruebe la zona de las claves de escritura del MCP que hoy no mira. El caso grave es `run_drc(reportPath)`, que permitiría a un agente de diseño sobrescribir cualquier archivo, `.claude/settings.json` incluido.

## Alcance

- Incluye: añadir a `CLAVES_DESTINO` de `.claude/hooks/guardia.py` las claves `reportPath`, `subsheetPath`, `parentSchematicPath`, `schematic_path`, `schematicPaths`, `projectsDir` y `pcbPath` (VAL-0001-03-02), con un caso por clave en `herramientas/pruebas/test_guardia.py`.
- Excluye: todo lo demás de VAL-0001-03 (descartado por el usuario el 2026-11-04).

## Entradas

- `gestion/informes/VAL-0001-03.md`, hallazgo 02.
- `.claude/hooks/guardia.py` y `herramientas/pruebas/test_guardia.py`.

## Entregables

- `guardia.py` con las claves nuevas y la batería ampliada.

## Criterios de aceptación

- [ ] `run_drc` con `reportPath` fuera de las zonas MCP se bloquea; dentro, pasa.
- [ ] Las otras seis claves se comprueban igual.
- [ ] La batería pasa entera, sin falsos positivos nuevos.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) a partir de VAL-0001-03 | |
| 2026-11-04 | usuario | Pide reducir SPEC-0002 y SPEC-0003 al mínimo; queda solo VAL-0001-03-02 | |
