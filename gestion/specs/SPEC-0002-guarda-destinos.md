---
id: SPEC-0002
titulo: Guarda: destinos ocultos y claves de destino del MCP
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

# SPEC-0002 · Guarda: destinos ocultos y claves de destino del MCP

> Nace de las observaciones M de [VAL-0001-03](../informes/VAL-0001-03.md). Validación recomienda cerrarla **antes de la primera spec que escriba en `hardware/v2/`**.

## Objetivo

Que la guarda vea los destinos que hoy se le escapan y compruebe todas las claves de escritura reales del servidor MCP. Las elusiones que queden tienen que estar en `LIMITES` y documentadas.

## Alcance

- Incluye:
  - VAL-0001-03-01: TFG alcanzado con comodines o desde una carpeta padre en tuberías (`Get-ChildItem …\proyectos\T* -Recurse | Remove-Item`); `Get-ChildItem docs | Remove-Item` y `xargs rm` dentro del repositorio; contenido de `find -exec`; `uniq` con segundo argumento; `cp --target-directory=`; `tar -cf`/`-rf` con el archivo dentro del TFG.
  - VAL-0001-03-02: invertir el criterio de `CLAVES_DESTINO`: toda clave con forma de ruta es destino salvo una lista explícita de orígenes. Cubrir `run_drc(reportPath)`, `subsheetPath`/`parentSchematicPath`, `schematic_path`, `schematicPaths`, `projectsDir` y `pcbPath`. Añadir una prueba que cruce las claves con el código del servidor (`C:\Users\josan\proyectos\KiCAD-MCP-Server\src\tools`).
  - VAL-0001-03-05: `git --config-env=`, variables `GIT_EXTERNAL_DIFF` y `GIT_CONFIG_*`; la sustitución de órdenes, a `LIMITES`.
  - VAL-0001-03-06: explicar `ZONAS_MCP` en "Guardas" y exigir a `ing-esquematicos` `close_project` con `save: false` (o aplicarle `AJENOS` en el MCP).
- Excluye: las B de detalle (SPEC-0003).

## Entradas

- `gestion/informes/VAL-0001-03.md` (hallazgos 01, 02, 05 y 06, con sus casos).
- `.claude/hooks/guardia.py`, `herramientas/pruebas/test_guardia.py` y `gestion/README.md` (Guardas).

## Entregables

- `guardia.py` y su batería con los casos nuevos.
- "Guardas" actualizada.

## Criterios de aceptación

- [ ] Los casos de VAL-0001-03-01, -02 y -05 están en la batería y se bloquean, o están en `LIMITES` y documentados.
- [ ] Una prueba cruza las claves de las herramientas de escritura del servidor MCP con las de la guarda.
- [ ] "Guardas" explica `ZONAS_MCP` y la regla de `close_project` de `ing-esquematicos`.
- [ ] Sin falsos positivos nuevos en la batería.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (propuesta) a partir de VAL-0001-03 | |
