---
spec: SPEC-0039
agente: ing-validacion
n: 04
fecha: 2026-11-26
estado: completado
---

# SPEC-0039 · 04 · ing-validacion

## Hecho

- Memoria: 13 archivos (389 líneas) y 341 afirmaciones → 5 archivos por tema, 112 líneas sin `MEMORY.md` (132 VIGENTE, 142 DUPLICADA, 37 OBSOLETA, 16 RECETA, 14 ESTADO). Clasificación: `gestion/logs/SPEC-0039/memoria-ing-validacion.csv` (la generó un script que ejecuta cada Grep o Glob; los recuentos son los del árbol en `3c9f78a` con la memoria nueva).
- Archivos nuevos: `guarda-y-gestion.md`, `copias-y-comparaciones.md`, `fuentes-y-datasheets.md`, `piezas-y-huellas.md` y `revision-calculos.md`; borrados los 12 `revision-*.md` y `comprobaciones-utiles.md`.
- Grep de los `antiguo` de `superados.csv` en la memoria nueva: 0 (tampoco cita b, b2 ni b3).

## Decisiones y desviaciones

- Las viñetas con varias afirmaciones se parten en filas; varias VIGENTE se funden en una viñeta (mismo `destino`).
- DUPLICADA cuenta también los cálculos que ya están en `docs/diseno/*.md` (datos de TPS2663, LMR36520, BTT6050, M7, HDG) y los puntos `[juicio]` de las checklists, que recogen casi todas las listas de «fallos típicos» de requisitos y alimentación.
- Las rutas `scratchpad\<carpeta>\…` de sesiones anteriores son OBSOLETA (Glob en la carpeta temporal actual → 0). Siguen en carpetas de sesiones viejas (`%TEMP%\claude\2c54f79e79dd3002\<sesión>\scratchpad\val27`, `v15`, `v21`, `v28`, `v29`…), sin garantía de que duren.
- Dos afirmaciones resultaron falsas al comprobarlas: «LCSC bloquea la descarga de PDF por curl» (el `pdfUrl` de C150716 baja un PDF de 32 p.) y «`auditoria_de` cuenta todo el `agent_id`» (desde SPEC-0039 cuenta desde el último `integrar`).

## Verificación

- `python herramientas/gestion.py comprobar`: todo correcto.
- Sin cambios en proyectos KiCad: `verificar.py` no aplica. MCP sin cargar.

## Pendiente

- Coordinador: copiar `memoria-ing-validacion.csv` y este parte a `gestion/logs/SPEC-0039/`.
- Propuestas de herramienta (filas RECETA; se han repetido en 2 specs o más):
  - copia de un commit (`hardware/v2`, `libraries`, `componentes`) a la carpeta temporal sin `git archive` (VAL-0014-01, VAL-0028-01, VAL-0038-01);
  - comparación semántica de PCB huella a huella, sin `uuid`, `path` ni `sheetname`, con renombrado de redes (VAL-0022-01, VAL-0027-01, VAL-0029-01, VAL-0035-01);
  - `hoja.py netlist` con propiedades (`dnp`, `exclude_from_*`) y cruce de la red de cada pad de la PCB con la netlist (VAL-0019-02, VAL-0025-01, VAL-0027-01, VAL-0031-01, VAL-0034-01);
  - placa de prueba con DRC de una huella, con el `.kicad_pro` y el `setup` de `hardware/v2`, redes en los pads del EP y una huella de control (VAL-0015-01, VAL-0018-02, VAL-0019-01, VAL-0021-01, VAL-0024-01);
  - `vista.py simbolo` (render de un símbolo con sus pines y su `Value`) (VAL-0015-01, VAL-0016-01, VAL-0016-02);
  - mutaciones de la batería (archivo, texto, sustituto, casos), en `herramientas/pruebas/` (VAL-0027-01, VAL-0027-02, VAL-0028-01, VAL-0035-02);
  - sondas contra la guarda de un commit anterior en `test_guardia.py` (VAL-0026-01, VAL-0026-02).
- `herramientas/kicad/README.md` («Formatos», descripción de hoja) dice que `extraer` + `generar` reproduce la hoja, pero `extraer` no lee el `justify` de los textos (`hoja.py` l. 241; VAL-0032-01): corregir el README o la herramienta.
