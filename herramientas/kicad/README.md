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
| `jlc.py` | Tipo (Basic/Extended), stock y precio de N códigos LCSC en una llamada; tabla con fecha y CSV. Con `--buscar`, hasta 25 resultados por MPN o texto (código, tipo, stock, precio del tramo de `--cantidad`, encapsulado) | `python herramientas/kicad/jlc.py --de docs/diseno/salidas.md --csv stock.csv` · `python herramientas/kicad/jlc.py --buscar TCA9535 --cantidad 10 --detalle lista.txt` |
| `campos.py revisar` | Campos que faltan, misma pieza con campos distintos entre hojas, DNP y diferencias con `hardware/componentes/campos-<hoja>.csv` | `python herramientas/kicad/campos.py revisar hardware/v2` |
| `campos.py aplicar` | Copia los campos y el DNP de la tabla a los símbolos de una hoja | `python herramientas/kicad/campos.py aplicar hardware/componentes/campos-salidas.csv <copia>/v2/salidas.kicad_sch -o <copia>/v2/salidas.kicad_sch` |
| `hoja.py pines` | Pines de un símbolo de librería, con coordenadas y lado | `python herramientas/kicad/hoja.py pines esp-riego:BTT6050-1ERA --proyecto hardware/v2` |
| `hoja.py extraer` | Descripción JSON de una hoja existente (piezas, campos, conexión de cada pin, cables, uniones, etiquetas fuera de los pines, recuadros, subhojas, textos) | `python herramientas/kicad/hoja.py extraer hardware/v2/mcu.kicad_sch -o mcu.json` |
| `hoja.py generar` | Escribe la hoja desde la descripción, con cables, uniones automáticas, recuadros con título y subhojas (también una subhoja repetida, con las referencias de cada instancia); conserva los UUID de la hoja que sustituye | `python herramientas/kicad/hoja.py generar mcu.json --proyecto <copia>/v2 -o <copia>/v2/mcu.kicad_sch` |
| `hoja.py raiz` | Pines de hoja de la raíz y su etiqueta local, global o NC, desde una descripción; `--extraer` saca la de la raíz actual. Conserva los UUID y no toca las hojas que no están en la descripción | `python herramientas/kicad/hoja.py raiz --proyecto hardware/v2 --extraer -o raiz.json` · `python herramientas/kicad/hoja.py raiz raiz.json --proyecto <copia>/v2 -o <copia>/v2/esp-riego.kicad_sch` |
| `hoja.py netlist` | Compara las netlists de dos proyectos (frente a la hoja anterior; `--grupos`, por grupos de pines y no por nombre de red), o la de un proyecto con las redes de un documento de diseño (`--plan`, «Plan de conexiones») | `python herramientas/kicad/hoja.py netlist hardware/v2 <copia>/v2 --grupos` · `python herramientas/kicad/hoja.py netlist hardware/v2 --plan docs/diseno/conectores.md --seccion "Anexo A"` |
| `sincronizar.py` | Netlist → PCB con `pcbnew`: huellas nuevas sin colocar, redes, campos y atributos; un modelo 3D oficial que falta se enlaza al de `../libraries/3d` con el mismo nombre; da la paridad | `python herramientas/kicad/sincronizar.py <copia>/v2 -o <copia>/v2/esp-riego.kicad_pcb` |
| `colocar.py` | Aplica una tabla `ref,x,y,giro,cara` a la PCB, o la exporta | `python herramientas/kicad/colocar.py <copia>/v2/esp-riego.kicad_pcb colocacion.csv -o <copia>/v2/esp-riego.kicad_pcb` |
| `vista.py hoja` | PNG de una hoja o de una zona de ella | `python herramientas/kicad/vista.py hoja hardware/v2 --hoja MCU --zona 150,95,280,190 -o u5.png` |
| `vista.py placa` | PNG de la placa por capas, entera, de una zona o con lo que está fuera del contorno | `python herramientas/kicad/vista.py placa hardware/v2 --todo -o placa.png` |
| `vista.py huella` | PNG de una huella sobre una placa de prueba, en 2D o con su modelo 3D (`--3d`) | `python herramientas/kicad/vista.py huella esp-riego:ESP32-S3-WROOM-1 --proyecto hardware/v2 --3d -o u5.png` |
| `vista.py 3d` | Render 3D de la placa | `python herramientas/kicad/vista.py 3d hardware/v2 -o placa3d.png` |
| `huella.py` | Cotas de un `.kicad_mod`: pads, paso, taladros, vías y pasta del pad expuesto, patio, serigrafía (gráficos y textos), atributo frente a los pads, 3D; cruce pin ↔ pad con `--simbolo` | `python herramientas/kicad/huella.py esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm --proyecto hardware/v2 --simbolo esp-riego:BTT6050-1ERA` |
| `restricciones.py` | Anchos, separaciones y vías por red de la PCB frente a la tabla de restricciones (CSV o Markdown) | `python herramientas/kicad/restricciones.py hardware/v2 docs/diseno/restricciones.csv` |
| `comprobar.py` | Los 25 puntos `[auto]` de las checklists de esquema, layout y librerías (`--lista`, qué mira cada uno); `verificar.py` los añade a su informe | `python herramientas/kicad/comprobar.py hardware/v2 --punto librerias.fichas` |

`_comun.py` tiene lo compartido: expresiones S, hojas del proyecto, tablas de librerías, copia de trabajo, `kicad-cli`, netlist y el límite de 30 líneas. `_estilo.py`, la geometría aproximada de una hoja (cajas de símbolos y textos, cables, recuadros) para los puntos de estilo de `comprobar.py`.

## Formatos

- **Tabla de campos** (`campos.py`, `hoja.py generar --campos`): CSV con `Refs` (`R1`, `R26-R31`, `C45, C46`), una columna por campo (`Value`, `Footprint`, `LCSC Part#`, `MPN`, `Fabricante`, `Datasheet`, `Description`) y `DNP` (sí/no). Celda vacía: no se toca.
- **Descripción de hoja** (`hoja.py`): JSON con
  - `papel` (`A4`…) y `cajetin` (`title`, `date`, `rev`, `company`, `comment: {"1": …}`);
  - `piezas`, cada una con `ref`, `simbolo` (`Lib:Nombre`), `x`, `y` y `giro` (mm y grados), `campos` (`{nombre: valor}`, sin `Reference`), `dnp` (por defecto `false`), `en_bom` (por defecto `true`; con `false` la pieza sale del BOM y de los archivos de posición, y solo se le piden `Value`, `Footprint` y `Description`), `pos` (opcional: `{"Reference" | "Value": [x, y, giro, justify]}`, posición absoluta del campo en la hoja; sin ella, el campo va junto al símbolo y horizontal), `pines` (`{"nº": conexión}`) y, en una hoja con varias instancias, `refs` (`{"Salidas/Canal1": "U7", …}`, la referencia de cada instancia por su ruta de nombres de hoja, sin `/` al principio ni al final);
  - `banderas` (`[[x, y]]`, PWR_FLAG) y `textos` (`x`, `y`, `tam`, `negrita`, `texto`; `justify`, por defecto `left bottom`);
  - `cables` (polilíneas `[[x, y], [x, y], …]`): se parten donde llega el extremo de otro cable o un pin, y las uniones (`junction`) se ponen solas donde se juntan tres o más extremos; `uniones` (`[[x, y]]`) añade otras;
  - `etiquetas` (`x`, `y`, `con` y `lado` `R`, `U`, `L` o `D`, hacia dónde va el texto): una conexión `L`, `H`, `G` o `P` fuera de un pin, normalmente en el extremo de un cable; avisa si no toca ni un pin ni un cable;
  - `recuadros` (`x`, `y`, `ancho`, `alto`, `titulo`): `text_box` de trazo y punto con el título arriba a la izquierda (DEC-0015);
  - `hojas` (subhojas dentro de esta hoja): `nombre`, `archivo`, `x`, `y`, `ancho`, `alto` y `pines` (`nombre`, `forma`, `lado` `L` o `R`, `y`). Dos subhojas con el mismo `archivo` son instancias de la misma hoja; cada una recibe su página. Se conservan el UUID y la página de la subhoja que ya existía con ese nombre.

  Cada pin visible lleva su conexión, dibujada en el extremo del pin: `L:RED` (local), `H:RED:forma` (jerárquica), `G:RED:forma` (global), con `forma` `input`, `output`, `bidirectional`, `passive` o `tri_state`, `P:GND` (símbolo de `power`; `P:GND:270`, girado 90, 180 o 270°, con el Value horizontal y hacia fuera, para pines seguidos en un lateral), `NC`, `W` (va a un cable: `generar` falla si ningún cable llega al pin) o `""`. `extraer` produce `en_bom`, `pos`, `refs`, cables, etiquetas, recuadros y subhojas de la hoja que lee, así que `extraer` + `generar` la reproduce.
- **Fichas de componentes** (`comprobar.py librerias.fichas`): cuenta como ficha de un código LCSC la ficha de pieza (`hardware/componentes/<MPN>.md`) que lo lleva en el campo `lcsc:` de su cabecera, con `tipo_jlcpcb` (basic/extended), `stock_consultado` (con fecha) y algún `datasheet*`; o una ficha de bloque (`bloque-<bloque>.md`) que lo lleva en la columna `LCSC` de una tabla, con el tipo en la misma fila, una fecha en la fila o en el archivo y la palabra «datasheet» en el archivo. Lo que va entre paréntesis (alternativas) y las citas en otro sitio no cuentan.
- **Descripción de la raíz** (`hoja.py raiz`): JSON con `hojas`, cada una con `nombre` (Sheetname), `archivo` (informativo) y `pines`: `nombre`, `forma` (`input`, `output`, `bidirectional`, `tri_state`, `passive`), `lado` (`L` o `R`), `y` (mm, dentro del borde) y `conexion` (`L:RED`, `G:RED:forma`, `NC` o `""`). Avisa (código 1) de los pines sin etiqueta jerárquica en la hoja hija y de las etiquetas sin pin.
- **Plan de conexiones** (`hoja.py netlist --plan`): en cualquier documento, cada red como `` `RED` = {R1-2, U5-34} `` o `RED {…}` (`REF-PIN` separados por comas); `NC {…}` = pines sin conectar. Sin `/` inicial, la red se busca por su nombre local (`/Conectores/ILIM_5V` vale para `ILIM_5V`). La red tiene que tener exactamente esos pines. Lo que no tiene esa forma (`BTN1…BTN6 {SWn-1}`) se cuenta como «sin interpretar». `--seccion` limita la lectura a la sección cuyo título contiene el texto.
- **Tabla de colocación** (`colocar.py`): CSV `ref,x,y,giro,cara`, en mm y grados, cara `F` o `B`.
- **Tabla de restricciones** (`restricciones.py`): `Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas`, con `Vía` (taladro/corona) opcional. `comprobar.py` la busca en `<proyecto>/restricciones.csv` o en `docs/diseno/restricciones.csv`.

## Límites conocidos

- `hoja.py` no admite símbolos de varias unidades ni espejados, ni buses, polilíneas, rectángulos, imágenes o tablas: se niega a sustituir una hoja que los tenga salvo con `--forzar`. Los cables no se trazan solos (los da la descripción) y los UUID de cables, uniones y recuadros son nuevos en cada `generar` (no afectan a la PCB). `generar` no toca los pines de hoja de la raíz (eso es `hoja.py raiz`). Los símbolos de alimentación de una hoja repetida reciben una `#PWR` nueva en cada instancia salvo la primera.
- Puntos de estilo de `comprobar.py` (`esquema.cruces`, `sueltas`, `recuadros`, `etiquetas`): miden los textos por una caja aproximada (`_estilo.py`: 0,8 × alto por carácter) y los símbolos por su dibujo y sus pines; no miran la raíz ni las hojas que lista `<proyecto>/estilo-pendiente.txt` (transición de SPEC-0035). `esquema.pcb_main` lee la PCB de `main` del repositorio (sin escribir) y busca las referencias en la SPEC de la rama y en sus partes; fuera del repositorio o en `main`, N/A.
- `hoja.py raiz` solo admite pines en los bordes izquierdo y derecho, no mueve ni redimensiona las hojas y solo pone etiquetas en el extremo del pin (sin cables). `netlist --plan` no comprueba los pines de la hoja que el plan no cita.
- `restricciones.py` mide la separación entre pistas y vías; la de pads y zonas la mide el DRC con la clase de red o la regla `.kicad_dru`, que es lo que la herramienta comprueba que existe.
- `huella.py` mide los pads `custom` por su ancla y trata las ventanas de pasta como rectángulos. Los textos de serigrafía se miden por una caja aproximada (0,8 × alto de letra por carácter, `${CAMPO}` como 5 caracteres, con `justify` y giro): en la PCB, el DRC mide la forma real.
- Tipo de una huella por sus pads (`huella.py`, `librerias.attr`, `layout.smd_cara`): no cuentan los pads con `pad_prop_heatsink`, `castellated`, `mechanical` o de fiducial, ni las vías térmicas (pasantes con el número de un pad SMD y dentro de él). Solo SMD → `smd`; con pasantes → `through_hole`; las dos cosas (USB-C con patas de la carcasa) → vale cualquiera. Sin atributo solo se acepta con `exclude_from_pos_files` (puntos de prueba, puentes), que tampoco cuenta en `layout.smd_cara`.
- `layout.zonas` comprueba que cada capa de cada zona tenga relleno guardado, no que esté al día: eso lo ve el DRC de `verificar.py` con el relleno previo.
- `comprobar.py` no decide si un modelo 3D está alineado (se mira con `vista.py huella --3d`) ni cubre las checklists de fabricación y requisitos.
- `vista.py` rasteriza con el `wx` del Python de KiCad; los textos del SVG salen como trazos.

## Puntos de checklist que comprueba `comprobar.py`

Línea de cada checklist en su versión actual (`gestion/checklists/`). Marca: `[auto: comprobar.py <punto>]`. Cada punto tiene en `test_kicad.py` (clases `Comprobar` y `Mutaciones`) al menos un caso que lo hace fallar.

| Checklist | Línea | Punto de la checklist | `comprobar.py` |
|---|---|---|---|
| esquema | 9 | Hojas jerárquicas por bloque; ninguna hoja huérfana | `esquema.hojas` |
| esquema | 16 | `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet` y `Description` presentes | `esquema.campos` (fuera del BOM solo se piden `Value`, `Footprint` y `Description`) |
| esquema | 17 | La huella asignada existe | `esquema.huellas` |
| esquema | 18 | Huellas con vías según FAB-02 | `esquema.vias` |
| esquema | 19 | No montados marcados como DNP | `esquema.dnp` (hoja = tabla de campos = PCB; texto «DNP / no montar» sin marca) |
| esquema | 71 | Ningún cable cruza un símbolo ni un texto; ningún texto se solapa | `esquema.cruces` (cables frente a dibujo y pines de cada símbolo, subhojas y textos; textos entre sí y con los símbolos) |
| esquema | 72 | Ninguna etiqueta suelta | `esquema.sueltas` (etiquetas y símbolos de alimentación en un pin, un pin de subhoja o sobre un cable) |
| esquema | 73 | Toda pieza dentro de un recuadro con título | `esquema.recuadros` (cuerpo y pines dentro de un `text_box` de trazo y punto con título) |
| esquema | 74 | Sin etiquetas que unan piezas del mismo bloque | `esquema.etiquetas` (ninguna etiqueta con el mismo nombre dos veces dentro de un recuadro) |
| esquema | 75 | El diff de la PCB frente a `main` solo toca las referencias de la spec | `esquema.pcb_main` (huella por huella; cada referencia que cambia, citada en la SPEC de la rama o en sus partes, con rangos «U7–U12») |
| layout | 13 | Zonas rellenadas | `layout.zonas` (relleno guardado en cada capa de cada zona; que esté al día lo ve el DRC con relleno previo) |
| layout | 15 | Sin `embedded_files` | `layout.incrustados` |
| layout | 16 | `outputdirectory` | `layout.salida` (vacío, o relativo y dentro de `<repo>/fabricacion/<versión>`) |
| layout | 31 (y 25, 32) | Anchos según la tabla de restricciones | `layout.restricciones` (`restricciones.py`; N/A mientras no exista la tabla). Compara la PCB con la tabla: que la tabla cumpla la corriente y el ΔT (l. 25 y 32) y los retornos por zonas no los mira (VAL-0027-01-01) |
| layout | 45 | SMD solo en la cara superior | `layout.smd_cara` (por los pads, no por el atributo) |
| layout | 50 | Modelo 3D en todos los componentes | `layout.3d` |
| librerías | 10 | Formato nativo | `librerias.formato` |
| librerías | 14 | Tablas con `${KIPRJMOD}` | `librerias.rutas` |
| librerías | 22 | Campos del símbolo | `librerias.campos` (símbolos de las librerías del `sym-lib-table`) |
| librerías | 28 | Courtyard presente y con margen | `librerias.patio` (≥ 0,1 mm; huellas del `fp-lib-table`) |
| librerías | 29 | Serigrafía fuera de los pads | `librerias.serigrafia` (gráficos y textos; textos por caja aproximada) |
| librerías | 33 | Modelo 3D presente, en `.step`, y existe | `librerias.3d` (alineado, l. 34, es `[juicio]`: `vista.py huella --3d`). Un modelo oficial que no existe vale si `libraries/3d` tiene uno con el mismo nombre (respaldo que enlaza `sincronizar.py`; `_comun.modelo_de_respaldo`) |
| librerías | 35 | Atributo `smd` / `through_hole` coherente con los pads | `librerias.attr` (huellas propias y huellas de la PCB) |
| librerías | 37 | Extensiones 3D como `binary` | `librerias.gitattributes` |
| librerías | 47 | Ficha del componente | `librerias.fichas` (campo `lcsc:` de una ficha de pieza o columna `LCSC` de una ficha de bloque; ver «Formatos») |

Sin cubrir: `requisitos.md` (IDs citados) y los ocho puntos de `fabricacion.md`, que van con el paquete de fabricación (fase 5).

## Enganche en `herramientas/verificar.py`

`verificar.py` llama a `comprobar.para_verificar(carpeta)` después de restaurar el proyecto y antes de imprimir: añade las líneas de los puntos a su informe y, con `--json`, la clave `auto`. No cambia `limpio` ni el código de salida.

## Pruebas

`python herramientas/pruebas/test_kicad.py` (sin red, unos minutos; necesita KiCad 10). Clases de SPEC-0035: `Hoja` (cables, uniones, recuadros, subhoja repetida, `--grupos`) y `Mutaciones` (`test_esquema_estilo`, `test_esquema_pcb_main`). Las clases que no lanzan KiCad van en segundos: `… test_kicad.py Huella Jlc Comun Comprobar Mutaciones Restricciones`. Prueba también `verificar.py` (clase `Verificar`: `comprobar.py` roto y zona sin rellenar). Trabaja sobre una copia temporal de `hardware/v2`, `hardware/libraries` y `hardware/componentes`.
