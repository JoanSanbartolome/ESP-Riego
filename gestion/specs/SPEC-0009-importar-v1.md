---
id: SPEC-0009
titulo: Importar la v1 del TFG a KiCad 10
fase: 1
estado: cerrada
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0009-importar-v1
requisitos: [KIC-01]
depende_de: []
creada: 2026-11-04
cerrada: 2026-11-04
validacion: VAL-0009-01
---

# SPEC-0009 · Importar la v1 del TFG a KiCad 10

> Fase 1 del plan (`docs/03-plan-de-diseno.md`). La v1 se conserva **tal como está en el TFG**: solo se arreglan las rutas de librería y el formato de archivo, sin tocar el diseño. La copia de trabajo de la v2 es otra spec (SPEC-0010).

## Objetivo

`hardware/v1-tfg/` contiene el proyecto del TFG en formato KiCad 10, abre en cualquier equipo con librerías propias del repositorio (`${KIPRJMOD}`) y da en `herramientas/verificar.py` las mismas incidencias que el análisis de la v1 (`docs/01-analisis-v1.md` §2).

## Alcance

- Incluye:
  - Copiar desde `C:\Users\josan\proyectos\TFG\KiCad_PCB\Control_De_Riego` (la carpeta de trabajo, idéntica a `PCB_FINAL.rar`), **solo leyendo del TFG** (`cp`/`Copy-Item` hacia `hardware/`), con sus nombres originales:
    - `Control_De_Riego.kicad_pro`, `Control_De_Riego.kicad_sch` (raíz), `allimentacion.kicad_sch`, `conectores.kicad_sch`, `modulo_reles.kicad_sch`, `wemos_s2mini.kicad_sch` y `Control_De_Riego.kicad_pcb`;
    - `Panel_Control.kicad_sch` en `hardware/v1-tfg/referencia/`, como referencia (no está en la jerarquía; H9).
  - Pasar a formato nativo de KiCad, en `hardware/libraries/`, las librerías que hoy apuntan a `G:/…/Llibreries_Kicad` (origen en `C:\Users\josan\proyectos\TFG\Llibreries_Kicad`), incluidas las dos que se leen de JSON de EasyEDA (símbolo y huella del Wemos, huella del jack DC). Se conservan los **mismos nombres (nicknames)** que en las tablas originales, para que los `lib_id` del esquema y la PCB sigan resolviendo. Si un JSON de EasyEDA no se puede convertir con KiCad, la pieza se extrae de la copia embebida en el esquema (`lib_symbols`) o en la PCB.
  - Reescribir `sym-lib-table` y `fp-lib-table` de `hardware/v1-tfg/` con rutas `${KIPRJMOD}/../libraries/...` y tipo `KiCad`.
  - Hoja de dibujo (`page_layout_descr_file` del `.kicad_pro`, hoy en `G:/…/Cajetin_Kicad.kicad_wks`): copiarla a `hardware/libraries/` y apuntarla con ruta relativa a `${KIPRJMOD}`.
  - Modelos 3D con ruta absoluta `G:/…` (inductor PSMT3012, TLP185, transistor y Wemos): copiarlos a `hardware/libraries/3d/` y apuntarlos con `${KIPRJMOD}/../libraries/3d/…`. Las rutas `${KICAD9_3DMODEL_DIR}` se dejan si KiCad 10 las resuelve; si no, se cambian a `${KICAD10_3DMODEL_DIR}`. Cada cambio de ruta queda en el log.
  - Guardar esquema y PCB en formato KiCad 10 (MCP `open_project` → guardar → `close_project`, o `kicad-cli … upgrade` si existe), sin cambiar el diseño.
- Excluye:
  - Copiar `-backups/`, `fp-info-cache`, `.kicad_prl`, `.step`, `untitled.kicad_sch` (duplicado del Wemos) y los `.rar`.
  - Corregir cualquier hallazgo H1–H12 del análisis (desincronización esquema↔PCB, error `starved_thermal`, huellas distintas de la librería, campos LCSC…): la v1 queda como estaba.
  - Fichas de `hardware/componentes/` (no hacen falta para la v1).
  - La copia de trabajo `hardware/v2/` (SPEC-0010) y la etiqueta `v1.1-tfg` (la pone el coordinador con el OK del usuario).

## Entradas

- Esta spec y `CLAUDE.md` (reglas del TFG de solo lectura y del MCP).
- `docs/01-analisis-v1.md` §1–§3: referencia de ERC, DRC y paridad, versiones del TFG, H8 y H9.
- `docs/03-plan-de-diseno.md`, fase 1.
- `docs/02-especificaciones-v2.md`: KIC-01.
- Origen (solo lectura): `C:\Users\josan\proyectos\TFG\KiCad_PCB\Control_De_Riego\` y `C:\Users\josan\proyectos\TFG\Llibreries_Kicad\`.
- `gestion/checklists/librerias.md`.
- `herramientas/verificar.py` y `herramientas/integridad_tfg.py`.

## Entregables

- `hardware/v1-tfg/`: los 7 archivos del proyecto en formato KiCad 10, `sym-lib-table`, `fp-lib-table` y `referencia/Panel_Control.kicad_sch`.
- `hardware/libraries/`: las librerías de símbolos (`.kicad_sym`) y huellas (`.pretty`) de la v1, la hoja de dibujo y `3d/`.
- `hardware/v1-tfg/README.md` breve: origen, qué se copió y qué no, cambios de rutas, y resultado de la verificación.
- Log `gestion/logs/SPEC-0009/01-jr-conformidad.md` con la salida de `verificar.py` antes (copia sin migrar en el scratchpad) y después, y la comparación de netlists.

## Criterios de aceptación

- [ ] Ningún archivo del TFG ha cambiado: `python herramientas/integridad_tfg.py verificar` da OK, y ni el MCP ni `kicad-cli` han abierto la carpeta del TFG (la referencia «antes» se hace sobre una copia en el scratchpad).
- [ ] `sym-lib-table`, `fp-lib-table`, `.kicad_pro`, esquemas y PCB no contienen rutas absolutas (`G:/`, `C:/`) ni librerías de tipo EasyEDA; los nicknames son los originales.
- [ ] Esquemas y PCB están en el formato de KiCad 10 (cabecera `version` actual).
- [ ] `python herramientas/verificar.py hardware/v1-tfg` da lo mismo que el análisis: ERC 1 (`pin_to_pin`); DRC 1 error `starved_thermal`, 39 `lib_footprint_mismatch` y 0 sin conectar; paridad 77 (61 `LCSC Part#`, 10 conflictos de red, 6 huellas). Cualquier diferencia se explica una a una en el log (por ejemplo, avisos de librería que antes no se resolvían) y no procede de un cambio del diseño.
- [ ] El diseño no ha cambiado: la netlist exportada con `kicad-cli` de la copia sin migrar y la de `hardware/v1-tfg` son equivalentes (mismas 61 referencias, valores, huellas y redes), y la PCB conserva posiciones, pistas y vías (el log da los recuentos antes y después).
- [ ] El proyecto abre sin librerías rotas: ningún símbolo ni huella aparece como no encontrado al resolver contra las tablas nuevas.
- [ ] Sin archivos `.lck` ni `-backups/` en `hardware/`; el MCP queda con `close_project`.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-04 | coordinador | Crea la spec (abierta) | |
| 2026-11-04 | jr-conformidad | Importa la v1: hardware/v1-tfg y hardware/libraries; ERC 1, DRC 39, paridad 77 | `265b5ae` |
| 2026-11-04 | ing-validacion | VAL-0009-01: APROBADO_CON_OBSERVACIONES (M 2 · B 3) | `f1266c9` |
| 2026-11-04 | coordinador | `.gitattributes` con IGES y STEP en mayúsculas (VAL-0009-01-05) | `57b2a6a` |
| 2026-11-04 | coordinador | Cierra la spec. Hallazgos 01–04 a una spec de corrección propuesta; propuestas de checklist y de la v2 al diario | VAL-0009-01 |
