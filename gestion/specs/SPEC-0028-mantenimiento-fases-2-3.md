---
id: SPEC-0028
titulo: Mantenimiento de las fases 2 y 3
fase: 3
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0028-mantenimiento-fases-2-3
requisitos: []
depende_de: []
creada: 2026-11-11
cerrada:
validacion:
---

# SPEC-0028 · Mantenimiento de las fases 2 y 3

## Objetivo

Corregir las observaciones B y M no bloqueantes acumuladas en las fases 2 y 3. Se abre al cerrar la fase 3 o cuando acumule bastante trabajo (DEC-0005). El coordinador añade aquí una línea por observación nueva.

## Alcance

- Incluye:
  - **Campos (VAL-0024-01-07):** `Datasheet` distinto para la misma pieza según la hoja, `Fabricante` ausente en `alimentacion.kicad_sch` y `Value` del LED sin unificar («Rojo» en D4, «LED» en D5), y «100n»/«100nF» y «1u»/«1uF». Con `campos.py revisar`.
  - **Fichas:** `verificado_por` de `BTT6050-1ERA.md` y `WJ500V-5.08-2P.md` sigue «pendiente».
  - **Puntos `[auto]` que fallan hoy en `verificar.py hardware/v2` (SPEC-0027):** `librerias.fichas`, seis pasivos del MCU sin ficha (C19666, C23162, C23179, C23186, C23345 y C45783; `jr-conformidad`), y `librerias.gitattributes`, falta `*.WRL` como `binary`.
  - **H1–H4:** el símbolo dice `in_pos_files yes` y la huella `exclude_from_pos_files`; la paridad no lo ve (parte 01 de SPEC-0027).
  - **Batería (VAL-0027-02-02):** casos de `test_kicad.py` para `verificar.py` con un `comprobar.py` roto y con una zona sin rellenar.
  - **Documentos:** cambios propuestos en `gestion/logs/SPEC-0023/01-ing-esquematicos.md` a `alimentacion.md` y a `estudio-salidas.md` S7; citar la página del pinout (VAL-0021-01-07).
  - **Checklists:** `librerias.md`, cobertura de pasta y tratamiento de las vías en pads expuestos, y Grep de todas las menciones del rasgo cambiado al proponer cambios a un documento (VAL-0024-01); `layout.md`, cruce pad ↔ netlist (VAL-0019-02).
  - **Guarda (VAL-0026-02), a cargo del coordinador:** en un heredoc sin comillas, analizar solo el texto de `$(…)` y de las comillas invertidas, no la línea entera (-02); no dar por buena una asignación tras `||` (`A || S=… && rm $S`, -01 b). Toca un hook: sondas nuevas y validación.
  - **Proyecto:** versionar el `.kicad_pro` que reescribe KiCad 10 al abrirlo, si el usuario lo quiere.
  - **`salidas.md` (VAL-0025-01-01):** la cabecera cita `docs/02` v0.4 en lugar de v0.5.
  - **Herramientas (SPEC-0025):** `hoja.py raiz` (pines de hoja y no conexiones de la raíz, que hoy se editan con Python en línea) y `hoja.py netlist --plan` (netlist frente al plan de conexiones del documento de diseño; lo escribieron por separado el autor y validación). Con su prueba en `test_kicad.py`.
  - **Posible:** campo de tipo *Basic*/*Extended* en los símbolos de todas las hojas.
- Excluye: lo que es del layout o de la fabricación, que está en `gestion/ESTADO.md` (vías y pasta del EPAD de U5, polígono BUS_24V, serigrafía «STATUS», estado de las vías en los Gerber).

## Entradas

- Los informes y partes citados en cada línea.

## Entregables

- Por definir al abrirla.

## Criterios de aceptación

- [ ] Por definir al abrirla: uno por línea del alcance.

## Plan de validación

Nivel **ligero**, salvo que alguna línea toque una huella o una hoja: entonces, completo para esa parte.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-11 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-11 | coordinador | Recoge las observaciones de los diarios del 2026-11-07 y del 2026-11-10 | DEC-0009 |  |  |  |
| 2026-11-12 | coordinador | Recoge lo pendiente de SPEC-0027 | VAL-0027-02 |  |  |  |
