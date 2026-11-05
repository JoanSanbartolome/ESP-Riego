---
spec: SPEC-0014
agente: ing-validacion
n: 03
fecha: 2026-11-05
estado: completado
---

# SPEC-0014 · 03 · ing-validacion

## Orden recibida

> SPEC-0014 · rama spec/SPEC-0014-limpieza-v2 (activa; no cambies de rama ni uses git para escribir; git de lectura sí) · commits revisados 3c8a700 (esquema, ing-esquematicos) y el siguiente (PCB, ing-layout); base 61d58eb · OJO: en el directorio de trabajo hay archivos sin commit de OTRA spec en paralelo (SPEC-0015: hardware/componentes/, hardware/libraries/esp-riego.*, hardware/libraries/3d/*.step nuevos) — no forman parte de esta revisión; compara siempre contra los commits (`git diff 61d58eb HEAD`). · Lee: gestion/specs/SPEC-0014-limpieza-v2.md, CLAUDE.md, docs/02 v0.4 (KIC-02, KIC-03, FAB-02, FAB-08 y los requisitos que justifican lo retirado), DEC-0002/0003/0004, gestion/informes/VAL-0013-02.md, checklists esquema.md v5 y layout.md v5; los entregables hardware/v2/; y al final los logs gestion/logs/SPEC-0014/01-ing-esquematicos.md y 02-ing-layout.md · Haz: valida criterio a criterio con tus comprobaciones: verificar.py hardware/v2 (esperado LIMPIO: ERC 0, DRC 0, paridad 0); que no queda ninguna pieza de la v1 que contradiga v0.4 y que lo conservado (H1–H4) está justificado; inventario de lo retirado frente a la v1 (61 refs) y que no se ha perdido nada que la v2 pida tal cual; 4 hojas con su texto de bloque; contorno 100 × 70 mm, H1–H4 y reglas de FAB-02; sin embedded_files del TFG ni outputdirectory; .kicad_pro sin clases de red de la v1; cajetín en PDF exportado sobre una copia (con hardware/libraries al lado); hardware/v1-tfg y hardware/libraries sin cambios en los commits; sin .lck ni backups. No uses el MCP (jr-conformidad trabaja en paralelo y el MCP debe quedar libre). · Entrega: gestion/informes/VAL-0014-01.md con veredicto + log gestion/logs/SPEC-0014/03-ing-validacion.md. Responde con VEREDICTO, hallazgos, PROPUESTAS y LOG.

## Contexto consultado

- `gestion/specs/SPEC-0014-limpieza-v2.md`, `CLAUDE.md` y `docs/02-especificaciones-v2.md` v0.4 (§2, §4 completo y §9).
- `gestion/decisiones/DEC-0002`, `DEC-0003` y `DEC-0004`.
- `gestion/informes/VAL-0013-02.md`.
- `gestion/checklists/esquema.md` v5 y `layout.md` v5, y la plantilla `gestion/plantillas/informe.md`.
- `hardware/v2/*` en `HEAD` (`9a8c24f`), y la base `61d58eb:hardware/v2/*`, extraída con `git show` a `scratchpad\val14\base\`.
- Los logs `01-ing-esquematicos.md` y `02-ing-layout.md`, leídos al final.

## Acciones

1. Rama `spec/SPEC-0014-limpieza-v2` y `HEAD` `9a8c24f`. Confirmé que `git diff HEAD -- hardware/v2` y `-- hardware/libraries/ESP-Riego.kicad_wks` están vacíos: lo que verifico en el directorio de trabajo es lo de los commits.
2. Inventario de la base y de `HEAD` con un analizador de *s-expressions* propio (`scratchpad\val14\inventario.py`). La base tiene 61 referencias y 38 símbolos de alimentación; `HEAD` tiene H1–H4.
3. Netlist de la base con `kicad-cli sch export netlist`, sobre la copia del *scratchpad* (`base_net.net` y `nets.py`), para ver las redes de los componentes retirados.
4. `verificar.py hardware/v2 --salida scratchpad\val14\ver_v2`, con `md5sum` de `hardware/v2/*` antes y después.
5. Copia de `hardware/v2` y de `ESP-Riego.kicad_wks` en `scratchpad\val14\copia\` (con `cp`: la guardia bloquea `git archive`). Allí exporté `sch.pdf` (5 páginas) y `pcb.pdf` (`--include-border-title`) y los revisé como imagen. Exporté también `fab.pdf` (`--layers F.Fab`).
6. Reguardé con `kicad-cli pcb upgrade --force` y `sch upgrade --force` una copia (`scratchpad\val14\upg\`) y la comparé con la entregada.
7. Comparé H1–H4 entre la base y `HEAD` (`fp_h.py`).
8. Grep de restos de la v1 en `hardware/v2`. `git diff --stat 61d58eb HEAD -- hardware/v1-tfg hardware/libraries`, `find` de `.lck` y de copias de seguridad, e `integridad_tfg.py verificar`.
9. Informe `gestion/informes/VAL-0014-01.md`.

## Decisiones y justificación

- **Sin MCP:** por orden del coordinador.
- **Las capas `F.Fab`/`B.Fab` que no están en `(layers …)` no son un hallazgo:** `kicad-cli` traza `F.Fab` con los textos de H1–H4 (`copia\fab.pdf`), así que no se pierde nada. Lo dejo como nota.
- **La clase `Default` a 0,2 mm (FAB-03 pide 0,25 mm) no es un hallazgo:** la spec deja las clases para el layout, y el log de ing-layout lo anota como pendiente.
- **Las tablas de librerías con solo entradas de la v1 sí son un hallazgo (B):** la spec solo excluye añadir las tablas de las piezas nuevas, y el objetivo es un esqueleto limpio.

## Verificación

```
ERC         0  (errores 0, avisos 0)
DRC         0  (errores 0, avisos 0, sin conectar 0)
Paridad     0
Resultado: LIMPIO
```

Otras comprobaciones:

- **MD5:** `hardware/v2/*` es igual antes y después de verificar.
- **v1-tfg y librerías:** `hardware/v1-tfg` y `hardware/libraries` no cambian en los commits.
- **TFG:** «TFG intacto: 337 archivos».
- **Restos de sesión:** no hay `.lck`, `-backups/`, `.mcp-backups/` ni `.kicad_prl`.
- **Reguardado:** la PCB reguardada es idéntica byte a byte; en los esquemas solo cambia el orden de los textos.

## Pendiente

- **Coordinador:** decidir sobre las observaciones B 01 (dos frases de los textos de bloque) y 02 (tablas de librerías con solo librerías de la v1), y sobre las tres propuestas para las checklists del informe.

## Notas para el siguiente agente

- La guardia bloquea `git archive`. Para copiar el estado de un commit, primero hay que comprobar que el directorio de trabajo coincide con `HEAD` (`git diff HEAD -- <ruta>` vacío) y luego usar `cp`. Para los estados anteriores, `git show <commit>:<ruta> > <scratchpad>`.
- `kicad-cli pcb upgrade --force` sobre una copia sirve para comprobar que una PCB editada con script coincide con lo que guardaría pcbnew.
