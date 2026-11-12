---
spec: SPEC-0027
agente: ing-diseno
n: 02
fecha: 2026-11-12
estado: completado
---

# SPEC-0027 · 02 · ing-diseno

## Hecho

Correcciones de VAL-0027-01 en `herramientas/kicad/` (`comprobar.py`, `huella.py`, `hoja.py`, `sincronizar.py`, `README.md` y `test_kicad.py` nueva completa, para mover a `herramientas/pruebas/`). Nada cambia en `hardware/`.

| Hallazgo | Punto de `comprobar.py` (o cambio) | Caso que lo hace fallar (`test_kicad.py`) |
|---|---|---|
| -02 | `layout.smd_cara`, por pads: huella en B.Cu con pads SMD, o pad SMD en B.Cu con B.Paste. Punto nuevo **`librerias.attr`**: huellas propias y de la PCB frente a `huella.tipo_por_pads` | `Mutaciones.test_layout_smd_cara` (con y sin `attr`, pads volteados), `.test_librerias_attr`, `Huella.test_tipo_por_pads_y_atributo` |
| -03 | `layout.zonas`: `filled_polygon` en cada capa de la zona (`F&B.Cu` y `*.Cu` expandidos) | `Mutaciones.test_layout_zonas` |
| -04 | `--help`: `hoja.py` 27, `sincronizar.py` 28, `comprobar.py` 27 líneas (la lista de puntos pasa a `--lista`) | `Generales.test_ayuda_y_compilacion` (≤ 30) |
| -05 | `layout.salida`: relativa al proyecto y dentro de `<repo>/fabricacion/<versión>` (raíz por `CLAUDE.md`; si no, `proyecto/../..`); absoluta, FALLA | `Mutaciones.test_layout_salida` (7 rutas, las 3 de `mutar.py`) |
| -06 | `librerias.serigrafia`: también textos visibles de SilkS, por caja aproximada (límite en el README) | `Mutaciones.test_librerias_serigrafia`, `Huella.test_textos_de_serigrafia` |
| -07 | `librerias.fichas`: el código cuenta si está en `lcsc:` de una ficha de pieza (sin lo que va entre paréntesis) o en la columna `LCSC` de una ficha de bloque, con tipo, fecha y datasheet de esa misma fuente | `Mutaciones.test_librerias_fichas` (tipo quitado, cita ajena, fila de bloque sin tipo) |
| -09 | Clase `Mutaciones` (13 pruebas): `esquema.vias`, `.dnp`, `layout.zonas`, `.salida`, `.restricciones`, `.smd_cara`, `.3d`, `librerias.formato`, `.campos`, `.patio`, `.serigrafia`, `.attr`, `.3d`, `.gitattributes`, `.fichas`. El resto (`esquema.hojas`, `.campos`, `.huellas`, `layout.incrustados`, `librerias.rutas`) ya fallaba en `Comprobar.test_detecta_lo_que_se_rompe` | Los 20 puntos tienen un caso |
| -10 | README, «Formatos»: claves `en_bom` y `pos` (y las formas de `H:`/`G:`), y formato de las fichas | — |

## Decisiones y desviaciones

- `librerias.attr` acepta sin atributo una huella con `exclude_from_pos_files` (puntos de prueba, puentes, como las oficiales), y cualquiera de los dos en las mixtas (USB-C con patas de carcasa). No cuentan los pads `heatsink`, `castellated`, `mechanical` ni fiduciales, ni las vías térmicas. `layout.smd_cara` tampoco cuenta lo que está fuera de posiciones.
- `librerias.attr` mira también las huellas de la PCB, que son las que salen en el CPL.

## Verificación

- `comprobar.py hardware/v2`: 20 puntos, OK 15, fallan 3, N/A 2. `librerias.attr` falla en BTT6050, WJ500V y J1 (PCB), como se esperaba. `librerias.fichas` da los mismos seis códigos que antes, y `librerias.gitattributes` sigue con `*.WRL`.
- `mutar.py` de validación con la versión nueva: 23/23 FALLA. Las pruebas nuevas, con las herramientas de `HEAD` sobre una copia: 9 de 16 fallan, así que detectan los defectos.
- Batería, `py_compile` y `verificar.py`: ver el contrato de salida.

## Pendiente

- Coordinador: mover `herramientas/kicad/test_kicad.py` a `herramientas/pruebas/`; en `librerias.md`, la l. 35 pasa a `[auto: comprobar.py librerias.attr]`. Si se quiere, también la l. 12 de `layout.md` (relleno por capa) y la l. 16 de `esquema.md` (VAL-0027-01-10).
- SPEC-0025: añadir `(attr smd)` al BTT6050 y `(attr through_hole)` al WJ500V (librería y J1 en la PCB).
