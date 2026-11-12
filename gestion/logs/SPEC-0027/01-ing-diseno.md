---
spec: SPEC-0027
agente: ing-diseno
n: 01
fecha: 2026-11-12
estado: completado
---

# SPEC-0027 · 01 · ing-diseno

## Hecho

- `herramientas/kicad/`: `_comun.py`, `jlc.py`, `campos.py`, `hoja.py`, `sincronizar.py`, `colocar.py`, `vista.py`, `huella.py`, `restricciones.py`, `comprobar.py`, `README.md` y `test_kicad.py` (20 pruebas). Nada cambia en `hardware/`.
- `README.md`: línea y ejemplo por herramienta, formatos, límites, la tabla «punto de checklist → `comprobar.py <punto>`» (21 puntos de esquema, layout y librerías en 19 comprobaciones) y las 5 líneas del enganche en `verificar.py` (secciones «Puntos de checklist…» y «Enganche…»).

## Decisiones y desviaciones

- `vista.py` rasteriza con el `wx` del Python de KiCad (el que trae `pcbnew`): sin PyMuPDF ni otra dependencia.
- `sincronizar.py` no quita «fuera de posiciones» a una huella que ya lo lleva (avisa), y borra con `RemoveNative`: con `BOARD.Remove()` pcbnew devuelve objetos sin tipo y falla.
- `esquema.campos` pide solo `Value`, `Footprint` y `Description` a lo que está fuera del BOM (TP, JP, H). `librerias.3d` no decide «alineado»: propongo partir ese punto de la checklist (README).
- `layout.restricciones` (3 puntos de la checklist) da N/A hasta que exista `docs/diseno/restricciones.csv` o `<proyecto>/restricciones.csv` (fase 4).
- El enganche solo informa: no cambia `limpio` ni el código de salida. `hoja.py` no toca los pines de hoja de la raíz.

## Verificación

- `hardware/v2`, sin tocar: ERC 0, DRC 0 con 172 sin conectar, paridad 0. Batería: 20 pruebas OK en 166 s (Python 3.12, sin red); `py_compile` con 3.12 y 3.11.
- Criterio 1: `--help`, ≤ 30 líneas y md5 antes/después, en la batería (12 órdenes de lectura sobre la copia).
- Criterio 2: copia de `pre-38090d2`: paridad 32 → 0, DRC 0, 172 sin conectar; 168 archivos de origen intactos (`md5sum`); las 80 huellas iguales a las de la PCB del repositorio (huella, valor, ruta, redes, campos, atributos).
- Criterio 3: `extraer` + `generar` de `mcu.kicad_sch`: 0 diferencias de netlist, ERC 0, paridad 0 (UUID conservados). Criterio 4: 10 vías de 0,3 / 0,6 y 11,035 mm² = 65 %. Criterio 5: 23 códigos de §9, tipos iguales a la tabla de SPEC-0024 (consulta del 2026-11-12).
- Criterio 6: `campos.py revisar hardware/v2`: `Fabricante` ausente en alimentación, `Datasheet` distinto en 5 piezas, `Value` «LED»/«Rojo» (y «100n»/«100nF», «1u»/«1uF»). Criterio 7: `verificar.py` con el enganche, sobre una copia: mismos recuentos y código de salida, más 20 líneas.

## Para validación

- `jlc.py` se prueba sin red con una respuesta guardada; el criterio 5 necesita red. `vista.py 3d` y `--3d` están probados a mano, no en la batería. Imágenes miradas: hoja MCU regenerada, hoja nueva desde cero, placa con las 21 huellas sin colocar y huella del BTT6050 en 2D y 3D.

## Pendiente

- Coordinador: enganche, traslado de la batería a `herramientas/pruebas/` y marcas `[auto: comprobar.py <punto>]` con la tabla del README.
- Hoy fallan dos puntos en `hardware/v2` (para SPEC-0028): `librerias.fichas` (C19666, C23162, C23179, C23186, C23345 y C45783, pasivos del MCU, sin ficha) y `librerias.gitattributes` (falta `*.WRL`). También para SPEC-0028: en H1–H4 el símbolo dice `in_pos_files yes` y la huella `exclude_from_pos_files`; la paridad no lo ve.
- **Antes de SPEC-0025:** a la huella `esp-riego:Infineon_PG-TDSO-14_…` le falta `(attr smd)`: `kicad-cli pcb export pos --smd-only` no la saca (comprobado en una placa de prueba), así que U7–U12 no entrarían en el CPL. Al borne WJ500V le falta `(attr through_hole)`. Propongo corregirlas y añadir el punto a la checklist de librerías.