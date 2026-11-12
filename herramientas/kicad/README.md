# Herramientas de KiCad

Operaciones de diseño que se repiten, versionadas y probadas (SPEC-0027, DEC-0009 M1). Antes de escribir un script en la carpeta temporal, se mira aquí; lo que se vaya a repetir se añade aquí, con su prueba en `test_kicad.py`.

Reglas comunes:

- `--help` en todas, en 30 líneas como mucho (lo comprueba la batería). La salida también cabe en 30 líneas; lo que sobra se guarda con `--detalle ARCHIVO` (o `--json`, en una línea).
- No modifican lo que leen. `kicad-cli` y `pcbnew` trabajan sobre una copia temporal del proyecto, con `../libraries` al lado, y solo se escribe en el destino de `-o`.
- Se lanzan con el Python del sistema (`python herramientas/kicad/<herramienta>.py`). Las que necesitan `pcbnew` o `wx` se relanzan solas con el de KiCad (`C:\Program Files\KiCad\10.0\bin\python.exe`; variables `KICAD_DIR`, `KICAD_CLI` y `KICAD_PYTHON` para otra instalación).
- Códigos de salida: 0 bien, 1 hay incidencias, 2 error de uso o de entorno (una línea en stderr).
- Para cambiar `hardware/v2`: copia en la carpeta temporal (`v2` y `libraries` como hermanas), herramienta con `-o` sobre la copia, `verificar.py` y, si está bien, se lleva el archivo al repositorio.

| Herramienta | Qué hace | Ejemplo |
|---|---|---|
| `jlc.py` | Tipo (Basic/Extended), stock y precio de N códigos LCSC en una llamada; tabla con fecha y CSV | `python herramientas/kicad/jlc.py --de docs/diseno/salidas.md --csv stock.csv` |
| `campos.py revisar` | Campos que faltan, misma pieza con campos distintos entre hojas, DNP y diferencias con `hardware/componentes/campos-<hoja>.csv` | `python herramientas/kicad/campos.py revisar hardware/v2` |
| `campos.py aplicar` | Copia los campos y el DNP de la tabla a los símbolos de una hoja | `python herramientas/kicad/campos.py aplicar hardware/componentes/campos-salidas.csv <copia>/v2/salidas.kicad_sch -o <copia>/v2/salidas.kicad_sch` |
| `hoja.py pines` | Pines de un símbolo de librería, con coordenadas y lado | `python herramientas/kicad/hoja.py pines esp-riego:BTT6050-1ERA --proyecto hardware/v2` |
| `hoja.py extraer` | Descripción JSON de una hoja existente (piezas, campos, conexión de cada pin, textos) | `python herramientas/kicad/hoja.py extraer hardware/v2/mcu.kicad_sch -o mcu.json` |
| `hoja.py generar` | Escribe la hoja desde la descripción; conserva los UUID de la hoja que sustituye | `python herramientas/kicad/hoja.py generar mcu.json --proyecto <copia>/v2 -o <copia>/v2/mcu.kicad_sch` |
| `hoja.py netlist` | Compara las netlists de dos proyectos (netlist frente al plan o frente a la hoja anterior) | `python herramientas/kicad/hoja.py netlist hardware/v2 <copia>/v2 --hoja MCU` |
| `sincronizar.py` | Netlist → PCB con `pcbnew`: huellas nuevas sin colocar, redes, campos y atributos; da la paridad | `python herramientas/kicad/sincronizar.py <copia>/v2 -o <copia>/v2/esp-riego.kicad_pcb` |
| `colocar.py` | Aplica una tabla `ref,x,y,giro,cara` a la PCB, o la exporta | `python herramientas/kicad/colocar.py <copia>/v2/esp-riego.kicad_pcb colocacion.csv -o <copia>/v2/esp-riego.kicad_pcb` |
| `vista.py hoja` | PNG de una hoja o de una zona de ella | `python herramientas/kicad/vista.py hoja hardware/v2 --hoja MCU --zona 150,95,280,190 -o u5.png` |
| `vista.py placa` | PNG de la placa por capas, entera, de una zona o con lo que está fuera del contorno | `python herramientas/kicad/vista.py placa hardware/v2 --todo -o placa.png` |
| `vista.py huella` | PNG de una huella sobre una placa de prueba, en 2D o con su modelo 3D (`--3d`) | `python herramientas/kicad/vista.py huella esp-riego:ESP32-S3-WROOM-1 --proyecto hardware/v2 --3d -o u5.png` |
| `vista.py 3d` | Render 3D de la placa | `python herramientas/kicad/vista.py 3d hardware/v2 -o placa3d.png` |
| `huella.py` | Cotas de un `.kicad_mod`: pads, paso, taladros, vías y pasta del pad expuesto, patio, serigrafía (gráficos y textos), atributo frente a los pads, 3D; cruce pin ↔ pad con `--simbolo` | `python herramientas/kicad/huella.py esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm --proyecto hardware/v2 --simbolo esp-riego:BTT6050-1ERA` |
| `restricciones.py` | Anchos, separaciones y vías por red de la PCB frente a la tabla de restricciones (CSV o Markdown) | `python herramientas/kicad/restricciones.py hardware/v2 docs/diseno/restricciones.csv` |
| `comprobar.py` | Los 20 puntos `[auto]` de las checklists de esquema, layout y librerías (`--lista`, qué mira cada uno); `verificar.py` los añade a su informe | `python herramientas/kicad/comprobar.py hardware/v2 --punto librerias.fichas` |

`_comun.py` tiene lo compartido: expresiones S, hojas del proyecto, tablas de librerías, copia de trabajo, `kicad-cli`, netlist y el límite de 30 líneas.

## Formatos

- **Tabla de campos** (`campos.py`, `hoja.py generar --campos`): CSV con `Refs` (`R1`, `R26-R31`, `C45, C46`), una columna por campo (`Value`, `Footprint`, `LCSC Part#`, `MPN`, `Fabricante`, `Datasheet`, `Description`) y `DNP` (sí/no). Celda vacía: no se toca.
- **Descripción de hoja** (`hoja.py`): JSON con
  - `papel` (`A4`…) y `cajetin` (`title`, `date`, `rev`, `company`, `comment: {"1": …}`);
  - `piezas`, cada una con `ref`, `simbolo` (`Lib:Nombre`), `x`, `y` y `giro` (mm y grados), `campos` (`{nombre: valor}`, sin `Reference`), `dnp` (por defecto `false`), `en_bom` (por defecto `true`; con `false` la pieza sale del BOM y de los archivos de posición, y solo se le piden `Value`, `Footprint` y `Description`), `pos` (opcional: `{"Reference" | "Value": [x, y, giro, justify]}`, posición absoluta del campo en la hoja; sin ella, el campo va junto al símbolo y horizontal) y `pines` (`{"nº": conexión}`);
  - `banderas` (`[[x, y]]`, PWR_FLAG) y `textos` (`x`, `y`, `tam`, `negrita`, `texto`).

  Cada pin visible lleva su conexión, dibujada en el extremo del pin y sin cables: `L:RED` (local), `H:RED:forma` (jerárquica), `G:RED:forma` (global), con `forma` `input`, `output`, `bidirectional`, `passive` o `tri_state`, `P:GND` (símbolo de `power`), `NC` o `""`. `extraer` produce `en_bom` y `pos` de la hoja que lee, así que `extraer` + `generar` la reproduce.
- **Fichas de componentes** (`comprobar.py librerias.fichas`): cuenta como ficha de un código LCSC la ficha de pieza (`hardware/componentes/<MPN>.md`) que lo lleva en el campo `lcsc:` de su cabecera, con `tipo_jlcpcb` (basic/extended), `stock_consultado` (con fecha) y algún `datasheet*`; o una ficha de bloque (`bloque-<bloque>.md`) que lo lleva en la columna `LCSC` de una tabla, con el tipo en la misma fila, una fecha en la fila o en el archivo y la palabra «datasheet» en el archivo. Lo que va entre paréntesis (alternativas) y las citas en otro sitio no cuentan.
- **Tabla de colocación** (`colocar.py`): CSV `ref,x,y,giro,cara`, en mm y grados, cara `F` o `B`.
- **Tabla de restricciones** (`restricciones.py`): `Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas`, con `Vía` (taladro/corona) opcional. `comprobar.py` la busca en `<proyecto>/restricciones.csv` o en `docs/diseno/restricciones.csv`.

## Límites conocidos

- `hoja.py` no admite símbolos de varias unidades ni espejados, no dibuja cables y no toca los pines de hoja de la raíz. Se niega a sustituir una hoja con cables (`alimentacion.kicad_sch`) salvo con `--forzar`.
- `restricciones.py` mide la separación entre pistas y vías; la de pads y zonas la mide el DRC con la clase de red o la regla `.kicad_dru`, que es lo que la herramienta comprueba que existe.
- `huella.py` mide los pads `custom` por su ancla y trata las ventanas de pasta como rectángulos. Los textos de serigrafía se miden por una caja aproximada (0,8 × alto de letra por carácter, `${CAMPO}` como 5 caracteres, con `justify` y giro): en la PCB, el DRC mide la forma real.
- Tipo de una huella por sus pads (`huella.py`, `librerias.attr`, `layout.smd_cara`): no cuentan los pads con `pad_prop_heatsink`, `castellated`, `mechanical` o de fiducial, ni las vías térmicas (pasantes con el número de un pad SMD y dentro de él). Solo SMD → `smd`; con pasantes → `through_hole`; las dos cosas (USB-C con patas de la carcasa) → vale cualquiera. Sin atributo solo se acepta con `exclude_from_pos_files` (puntos de prueba, puentes), que tampoco cuenta en `layout.smd_cara`.
- `layout.zonas` comprueba que cada capa de cada zona tenga relleno guardado, no que esté al día: eso lo ve el DRC de `verificar.py` con el relleno previo.
- `comprobar.py` no decide si un modelo 3D está alineado (se mira con `vista.py huella --3d`) ni cubre las checklists de fabricación y requisitos.
- `vista.py` rasteriza con el `wx` del Python de KiCad; los textos del SVG salen como trazos.

## Puntos de checklist que comprueba `comprobar.py`

Línea de cada checklist en su versión actual (`gestion/checklists/`: esquema v8, layout v7, librerías v5). Marca: `[auto: comprobar.py <punto>]`. Cada punto tiene en `test_kicad.py` (clases `Comprobar` y `Mutaciones`) al menos un caso que lo hace fallar.

| Checklist | Línea | Punto de la checklist | `comprobar.py` |
|---|---|---|---|
| esquema | 9 | Hojas jerárquicas por bloque; ninguna hoja huérfana | `esquema.hojas` |
| esquema | 16 | `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet` y `Description` presentes | `esquema.campos` (fuera del BOM solo se piden `Value`, `Footprint` y `Description`) |
| esquema | 17 | La huella asignada existe | `esquema.huellas` |
| esquema | 18 | Huellas con vías según FAB-02 | `esquema.vias` |
| esquema | 19 | No montados marcados como DNP | `esquema.dnp` (hoja = tabla de campos = PCB; texto «DNP / no montar» sin marca) |
| layout | 12 | Zonas rellenadas | `layout.zonas` (relleno guardado en cada capa de cada zona; que esté al día lo ve el DRC con relleno previo) |
| layout | 14 | Sin `embedded_files` | `layout.incrustados` |
| layout | 15 | `outputdirectory` | `layout.salida` (vacío, o relativo y dentro de `<repo>/fabricacion/<versión>`) |
| layout | 30 (y 24, 31) | Anchos según la tabla de restricciones | `layout.restricciones` (`restricciones.py`; N/A mientras no exista la tabla). Compara la PCB con la tabla: que la tabla cumpla la corriente y el ΔT (l. 24 y 31) y los retornos por zonas no los mira (VAL-0027-01-01) |
| layout | 44 | SMD solo en la cara superior | `layout.smd_cara` (por los pads, no por el atributo) |
| layout | 49 | Modelo 3D en todos los componentes | `layout.3d` |
| librerías | 10 | Formato nativo | `librerias.formato` |
| librerías | 14 | Tablas con `${KIPRJMOD}` | `librerias.rutas` |
| librerías | 22 | Campos del símbolo | `librerias.campos` (símbolos de las librerías del `sym-lib-table`) |
| librerías | 28 | Courtyard presente y con margen | `librerias.patio` (≥ 0,1 mm; huellas del `fp-lib-table`) |
| librerías | 29 | Serigrafía fuera de los pads | `librerias.serigrafia` (gráficos y textos; textos por caja aproximada) |
| librerías | 33 | Modelo 3D presente, en `.step`, y existe | `librerias.3d` (alineado, l. 34, es `[juicio]`: `vista.py huella --3d`) |
| librerías | 35 | Atributo `smd` / `through_hole` coherente con los pads | `librerias.attr` (huellas propias y huellas de la PCB) |
| librerías | 37 | Extensiones 3D como `binary` | `librerias.gitattributes` |
| librerías | 45 | Ficha del componente | `librerias.fichas` (campo `lcsc:` de una ficha de pieza o columna `LCSC` de una ficha de bloque; ver «Formatos») |

Sin cubrir: `requisitos.md` (IDs citados) y los ocho puntos de `fabricacion.md`, que van con el paquete de fabricación (fase 5).

## Enganche en `herramientas/verificar.py`

`verificar.py` llama a `comprobar.para_verificar(carpeta)` después de restaurar el proyecto y antes de imprimir: añade las líneas de los puntos a su informe y, con `--json`, la clave `auto`. No cambia `limpio` ni el código de salida.

## Pruebas

`python herramientas/pruebas/test_kicad.py` (sin red, unos minutos; necesita KiCad 10). Las clases que no lanzan KiCad van en segundos: `… test_kicad.py Huella Comprobar Mutaciones Restricciones`. Trabaja sobre una copia temporal de `hardware/v2`, `hardware/libraries` y `hardware/componentes`.
