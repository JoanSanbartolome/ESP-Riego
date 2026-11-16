---
id: SPEC-0028
titulo: Mantenimiento de las fases 2 y 3
fase: 3
estado: abierta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0028-mantenimiento-fases-2-3
requisitos: [FAB-05, ALI-04, AMB-02, KIC-01]
depende_de: []
creada: 2026-11-11
cerrada:
validacion:
---

# SPEC-0028 · Mantenimiento de las fases 2 y 3

## Objetivo

Corregir las observaciones B y M no bloqueantes acumuladas en las fases 2 y 3 (DEC-0005), para que SPEC-0032 (integración) parta de un proyecto sin incidencias conocidas: `verificar.py hardware/v2` sin ningún `[auto]` en FALLA y `campos.py revisar hardware/v2` sin diferencias.

## Alcance

Cada línea lleva su informe de origen, donde está el detalle. Tres pasos, uno detrás de otro (el MCP admite un solo agente con proyecto cargado).

- Incluye:
  - **Paso 1 · `jr-conformidad`** (`hardware/componentes/`, campos de las hojas):
    - **Campos (VAL-0024-01-07):** misma pieza con `Value`, `Fabricante` o `Datasheet` distintos según la hoja («100n»/«100nF», «1u»/«1uF», LED «Rojo» en D4 y «LED» en D5, `Datasheet` de página de producto de LCSC en alimentación) y `Fabricante` ausente en `alimentacion.kicad_sch`. Tablas nuevas `campos-alimentacion.csv` y `campos-mcu.csv`, aplicadas con `campos.py aplicar`.
    - **Fichas:** `verificado_por` «pendiente» en `BTT6050-1ERA.md` y `WJ500V-5.08-2P.md`, y los cambios a esas dos fichas que propone `gestion/logs/SPEC-0023/01-ing-esquematicos.md` («Cambios propuestos»), si faltan.
    - **`librerias.fichas` (SPEC-0027, SPEC-0031):** sin ficha C23162, C23186, C23345 y C45783 (hoja MCU).
    - **`SHT4x.md` (VAL-0029-01-02):** variante sin fijar y modelo 3D «pendiente» en `verificado_por`.
    - **U13 a SHT40-AD1B-R2 (VAL-0029-01-03):** C2909890, el mismo chip, 1,749 $ frente a 1,854 $ (5 uds., 2026-11-16): abarata, sin consulta.
    - **F1 (VAL-0006-01-04):** C44479 vuelve a tener stock (22 932 el 2026-11-16). Se mantiene 0451010.MRL; se comprueban 0453010.MR (C178995) y TA10 (C2998199) como alternativas frente a `alimentacion.md` §3.2.
  - **Paso 2 · `ing-diseno`** (`docs/diseno/`, hojas, PCB y `herramientas/kicad/`):
    - **Hoja de conectores (VAL-0031-01-05/06):** los 7 cables añadidos por script (EN–IN de U14/U15, GND de J10, A0–A2 de U18) pasan a conexiones de la descripción de `hoja.py`, para regenerarla sin `--forzar`; nota «SLVS841G pp. 16–17».
    - **H1–H4 (SPEC-0027, parte 01):** el símbolo dice `in_pos_files yes` y la huella `exclude_from_pos_files`; la paridad no lo ve.
    - **PCB:** llevar a la PCB los campos del paso 1 y de U13 con `sincronizar.py`.
    - **Herramientas (SPEC-0025):** `hoja.py raiz` (pines de hoja y no conexiones de la raíz, que hoy se editan con Python en línea) y `hoja.py netlist --plan` (netlist frente al plan de conexiones de un documento de diseño).
    - **Batería** de `test_kicad.py`: `verificar.py` con un `comprobar.py` roto y con una zona sin rellenar (VAL-0027-02-02); `_comun.modelo_de_respaldo`, el cambio de modelo de `sincronizar.py` y la rama de respaldo de `librerias.3d` (VAL-0029-01-01, M); `jlc.py --buscar` / `jlc.resultados` (VAL-0006-01-07); las dos órdenes nuevas de `hoja.py`.
    - **Documentos:** `alimentacion.md` §4 (I_GND de los BTT) y §10.7, y `estudio-salidas.md` S7, según el parte 01 de SPEC-0023; cabecera de `salidas.md` (VAL-0025-01-01); `mcu.md` §8.2, calentador del SHT4x (VAL-0029-01-04); menciones de SHT40-AD1B-R3 / C2848306; alternativa de F1 en `alimentacion.md` según el paso 1; `viabilidad-expansion.md` §5, inversor de la arquitectura 3 (VAL-0006-02-01).
  - **Paso 3 · coordinador:**
    - `.gitattributes`: `*.WRL` como `binary` (`librerias.gitattributes`).
    - Checklists: `librerias.md`, pasta y vías en pads expuestos y Grep de todas las menciones del rasgo cambiado (VAL-0024-01), y página del pinout citada (VAL-0021-01-07); `layout.md`, cruce pad ↔ netlist (VAL-0019-02).
    - `.kicad_pro`: se versiona si los pasos 1–2 lo reescriben (DEC-0011).
- Excluye:
  - Las dos líneas de la guarda (VAL-0026-02-01 b y -02): DEC-0009 la congela. Ya figuran en «Límites conocidos» de `gestion/README.md`.
  - «Posible: campo *Basic*/*Extended* en los símbolos»: pasa a `gestion/ESTADO.md`.
  - Lo del layout y la fabricación de `gestion/ESTADO.md`; la revisión de `salidas.md` con el dato de las válvulas (SPEC-0032); los requisitos v0.7 del módulo de expansión.
  - Ningún cambio de requisitos ni de decisiones, ni de cifras de diseño salvo las citadas.

## Entradas

- Informes y partes citados en cada línea; `herramientas/kicad/README.md` (formatos, límites conocidos).
- `docs/diseno/alimentacion.md` §2, §3.2, §4 y §10.7; `docs/diseno/salidas.md` (cabecera, §2.3 y §3); `docs/diseno/estudio-salidas.md` (cabecera, S7); `docs/diseno/mcu.md` §8.2; `docs/diseno/sensores.md` (U13); `docs/diseno/viabilidad-expansion.md` §5 y §10.2; `docs/diseno/conectores.md` (U14/U15, J10, U18).
- `docs/02-especificaciones-v2.md` (cabecera e historial, para la versión vigente).
- Checklists `librerias.md` v6 y `esquema.md` (los puntos `[juicio]` de lo que toque cada paso).

## Entregables

- **Paso 1:** `hardware/componentes/campos-alimentacion.csv`, `campos-mcu.csv` y `campos-sensores.csv`; `alimentacion.kicad_sch`, `mcu.kicad_sch` y `sensores.kicad_sch` (solo campos); fichas `BTT6050-1ERA.md`, `WJ500V-5.08-2P.md`, `SHT4x.md`, `0451010.MRL.md` y la de los cuatro pasivos (p. ej. `bloque-mcu.md`); `stock-sensores.csv`; parte `gestion/logs/SPEC-0028/01-jr-conformidad.md`.
- **Paso 2:** `hardware/v2/conectores.kicad_sch` (la descripción JSON, en la carpeta temporal: `hoja.py extraer` la reproduce), `esp-riego.kicad_pcb`; `herramientas/kicad/hoja.py` y `README.md`; `herramientas/kicad/test_kicad.py` (copia de `herramientas/pruebas/test_kicad.py` con los casos nuevos: `herramientas/pruebas/` queda fuera de la zona, la mueve el coordinador); los documentos de `docs/diseno/` citados; parte `gestion/logs/SPEC-0028/02-ing-diseno.md`.
- **Paso 3:** `.gitattributes`, `gestion/checklists/librerias.md` v7 y `layout.md` v9, `herramientas/pruebas/test_kicad.py`, y `hardware/v2/esp-riego.kicad_pro` si cambió.

## Criterios de aceptación

Paso 1 (`jr-conformidad`):

- [ ] Campos: un mismo código LCSC lleva el mismo `Value`, `Fabricante` y `Datasheet` en las cinco hojas, con la notación de las tablas existentes y `Datasheet` del fabricante o PDF de LCSC (no la página de producto). `campos.py revisar hardware/v2`: 0 que faltan, 0 distintos, 0 diferencias con la tabla.
- [ ] `BTT6050-1ERA.md` y `WJ500V-5.08-2P.md`: `verificado_por` con el informe VAL que las verificó (o `VAL-0028-01` si ninguno lo hizo, para que lo haga esta validación); los cambios propuestos en SPEC-0023 a esas fichas, presentes.
- [ ] `comprobar.py hardware/v2 --punto librerias.fichas`: OK (C23162, C23186, C23345 y C45783 con ficha según «Formatos» de `herramientas/kicad/README.md`).
- [ ] `SHT4x.md`: variante SHT40-AD1B-R2 (C2909890) con tipo, stock y fecha, y la diferencia entre R2 y R3 con la página del datasheet; `verificado_por` del 3D como en el punto anterior.
- [ ] U13 = SHT40-AD1B-R2 (C2909890) en `campos-sensores.csv`, en `sensores.kicad_sch` y en `stock-sensores.csv`; misma huella.
- [ ] `0451010.MRL.md`: stock de C44479 con fecha, y 0453010.MR y TA10 comparados con §3.2 (≥ 5,1 A a 60 °C con el 75 % y la curva de temperatura, ≥ 58,6 V DC, I²t de fusión ≫ 0,25 A²s, huella NANO2 451/453), con página del datasheet; alternativa válida anotada. Si TA10 no cumple, se dice en PENDIENTE.

Paso 2 (`ing-diseno`):

- [ ] `conectores.kicad_sch` sale de `hoja.py generar` sin `--forzar` y sin cables; la nota dice «SLVS841G pp. 16–17»; `hoja.py netlist` frente a `main`: la misma netlist.
- [ ] H1–H4: fuera del BOM y de los archivos de posición en la hoja, como su huella (`en_bom: false`).
- [ ] PCB con los campos de las hojas (`sincronizar.py`); `verificar.py hardware/v2`: ERC 0, DRC 0 errores, paridad 0 y ningún `[auto]` en FALLA salvo `librerias.gitattributes` (paso 3).
- [ ] `hoja.py raiz` escribe pines de hoja y no conexiones de la raíz desde una descripción, y `hoja.py netlist --plan` compara la netlist con una tabla de conexiones de un documento de diseño; `--help` ≤ 30 líneas; README (tabla, formatos y límites conocidos) al día.
- [ ] `test_kicad.py` con un caso que falla si se rompe cada una de estas: `verificar.py` con `comprobar.py` roto (no se cae y lo dice) y con una zona sin rellenar; `_comun.modelo_de_respaldo`; cambio de modelo de `sincronizar.py`; rama de respaldo de `librerias.3d`; `jlc.resultados` (sin red, con datos fijos); `hoja.py raiz`; `hoja.py netlist --plan`. La batería entera pasa.
- [ ] `alimentacion.md` §4 suma la I_GND de los BTT (≤ 6 × 9 mA) a la carga del bus y recalcula el margen con las cifras vigentes; §10.7 remite a `salidas.md` §2.3 como cerrado; la alternativa de F1 de §2 coincide con el resultado del paso 1.
- [ ] `estudio-salidas.md` S7 remite a `salidas.md` §3.
- [ ] `salidas.md`: la cabecera cita la versión de `docs/02` frente a la que se comprobó (v0.5 o posterior); ningún otro cambio en ese documento.
- [ ] `mcu.md` §8.2: calentador del SHT4x a 100 mA máx. (datasheet p. 9) y el total que de él depende, recalculado.
- [ ] Grep de SHT40-AD1B-R3 y C2848306 en `docs/diseno/` y `hardware/`: solo quedan como pieza anterior o alternativa.
- [ ] `viabilidad-expansion.md` §5: el inversor de ejemplo garantiza la conmutación con 2,36 V en la puerta (N-MOS con V_GS(th) máx. ≤ 1,5 V o inversor LVC de una puerta a 3,3 V), con pieza y página; nota de arquitectura descartada (DEC-0012).

Paso 3 (coordinador):

- [ ] `librerias.gitattributes`: OK.
- [ ] `librerias.md` v7 y `layout.md` v9 con los puntos de VAL-0024-01, VAL-0021-01-07 y VAL-0019-02, marcados `[auto]` o `[juicio]`, e historial.
- [ ] `.kicad_pro`: si cambió, se versiona con sus rutas de salida vacías o dentro de `fabricacion/`; si no, se anota en el cierre.
- [ ] Baterías `test_kicad.py`, `test_gestion.py`, `test_guardia.py` y `test_commit_msg.py` sin regresiones.

## Plan de validación

Una validación, al final. Nivel **completo** para `hardware/` y `herramientas/kicad/`; **por muestreo** para textos y campos.

- Se reproduce de forma independiente: la netlist de `conectores` frente a `main` (sin cambios de conexión); H1–H4 en hoja, PCB y CPL (`kicad-cli pcb export pos`); `verificar.py hardware/v2` y `campos.py revisar`; U13-R2 con la misma huella y pinout (datasheet); las cifras de F1 frente a §3.2 y la I_GND de §4; que cada caso nuevo de la batería falle con la mutación que dice cubrir (al menos tres de ellos), y `hoja.py raiz` y `netlist --plan` sobre una copia.
- Por muestreo: cinco códigos LCSC de las tablas nuevas (campos y stock), las fichas nuevas, los textos de `docs/diseno/` y las checklists.
- Los `verificado_por` que digan `VAL-0028-01`: se comprueban aquí (render `vista.py huella --3d` y huella frente al datasheet).

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-11 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-11 | coordinador | Recoge las observaciones de los diarios del 2026-11-07 y del 2026-11-10 | DEC-0009 |  |  |  |
| 2026-11-12 | coordinador | Recoge lo pendiente de SPEC-0027 | VAL-0027-02 |  |  |  |
| 2026-11-16 | coordinador | Abre la spec |  |  |  |  |
