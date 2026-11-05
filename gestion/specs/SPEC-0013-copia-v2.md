---
id: SPEC-0013
titulo: Copia de trabajo de la v2
fase: 3
estado: abierta
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0013-copia-v2
requisitos: [KIC-01, KIC-02]
depende_de: [SPEC-0010, SPEC-0011]
creada: 2026-11-05
cerrada:
validacion:
---

# SPEC-0013 · Copia de trabajo de la v2

> Primer paso de la v2: una copia de trabajo de la v1 (etiqueta `v1.1-tfg`) sobre la que cada bloque se sustituye después con su propia spec. El usuario lo pidió así: copiar la placa del TFG y aplicar las especificaciones poco a poco. Esta spec **no cambia el diseño**: solo copia, renombra y prepara el proyecto.

## Objetivo

`hardware/v2/` contiene un proyecto KiCad 10 llamado `esp-riego`, copia exacta en diseño de `hardware/v1-tfg/`. Sus hojas tienen los nombres de los bloques de la v2 (KIC-02) y su cajetín identifica la v2. La verificación da las mismas incidencias que la v1.

## Alcance

- Incluye:
  - Copiar los 7 archivos del proyecto de `hardware/v1-tfg/` (sin `referencia/` ni `README.md`) a `hardware/v2/`, junto con `sym-lib-table` y `fp-lib-table`. Las rutas `${KIPRJMOD}/../libraries/...` siguen valiendo, porque `hardware/v2` está al lado de `hardware/v1-tfg`.
  - Renombrar el proyecto: `Control_De_Riego.kicad_pro|kicad_sch|kicad_pcb` pasan a `esp-riego.kicad_pro|kicad_sch|kicad_pcb`.
  - Renombrar las hojas con los bloques de KIC-02, cambiando el archivo y el `Sheetname` en la raíz:

    | Hoja v1 (`Sheetname` · archivo) | Hoja v2 (`Sheetname` · archivo) |
    |---|---|
    | `Alimentacion` · `allimentacion.kicad_sch` | `Alimentacion` · `alimentacion.kicad_sch` |
    | `ESP32_S2` · `wemos_s2mini.kicad_sch` | `MCU` · `mcu.kicad_sch` |
    | `Modulo_reles` · `modulo_reles.kicad_sch` | `Salidas` · `salidas.kicad_sch` |
    | `Conectores y agujeros PCB` · `conectores.kicad_sch` | `Conectores` · `conectores.kicad_sch` |

    La hoja `Sensores` no se crea aquí: llega con el bloque de temperatura y humedad.
  - Cajetín de todas las hojas del esquema y de la PCB:
    - título «ESP-Riego v2»;
    - revisión «2.0-dev»;
    - fecha 2026-11-05;
    - autor y empresa «Joan San Bartolomé Ferri».
    
    Se quitan los comentarios del TFG («Plano General PCB», «001», «SE», «1:1», «Universitat Politecnica de Valencia»). Se mantiene la hoja de dibujo `Cajetin_Kicad.kicad_wks`.
  - `hardware/v2/README.md` breve:
    - origen (`v1.1-tfg`, commit `ec3527c`);
    - correspondencia de las hojas;
    - que cada bloque se sustituye con su propia spec y el layout se rehace cuando el esquema esté estable.
- Excluye:
  - Cualquier cambio de circuito, de componentes, de huellas o de la PCB que no sea renombrar o cambiar el cajetín. Los bloques de la v2 son otras specs.
  - Tocar `hardware/v1-tfg/` o `hardware/libraries/`.
  - `docs/03-plan-de-diseno.md` (lo actualiza el coordinador en esta rama).

## Entradas

- Esta spec y `CLAUDE.md`.
- `hardware/v1-tfg/` y su `README.md`.
- `docs/02-especificaciones-v2.md`: KIC-01 y KIC-02.
- `gestion/checklists/librerias.md` (rutas y tablas).
- `herramientas/verificar.py`.

## Entregables

- `hardware/v2/`: los 7 archivos del proyecto renombrados, `sym-lib-table`, `fp-lib-table` y `README.md`.
- Log `gestion/logs/SPEC-0013/01-jr-conformidad.md`, con los cambios y la verificación antes y después.

## Criterios de aceptación

- [ ] `python herramientas/verificar.py hardware/v2` da lo mismo que la v1: ERC 1 (`pin_to_pin`), DRC 40 (1 `starved_thermal` y 39 `lib_footprint_mismatch`, 0 sin conectar) y paridad 77 (61, 10 y 6).
- [ ] El diseño es el de la v1. La netlist de `hardware/v2` y la de `hardware/v1-tfg` (exportadas con `kicad-cli`) tienen las mismas 61 referencias, valores, huellas y conexiones. Solo cambia el prefijo de hoja en los nombres de red. La PCB conserva posiciones, pistas, vías y zonas.
- [ ] La jerarquía tiene las 4 hojas con los nombres de la tabla y no queda ninguna referencia a los archivos antiguos.
- [ ] El cajetín del esquema y de la PCB tiene los datos de la v2 y ningún resto del TFG.
- [ ] No hay rutas absolutas; `hardware/v1-tfg/` y `hardware/libraries/` no cambian; no quedan `.lck` ni `-backups/`, y el MCP queda con `close_project` si se usó.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (abierta) | |
