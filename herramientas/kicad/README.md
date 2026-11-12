# Herramientas de KiCad

Operaciones de diseño que se repiten, versionadas y probadas (SPEC-0027, DEC-0009 M1). Antes de escribir un script en la carpeta temporal, se mira aquí; lo que se vaya a repetir se añade aquí, con su prueba en `test_kicad.py`.

Reglas comunes:

- `--help` en todas. La salida cabe en 30 líneas; lo que sobra se guarda con `--detalle ARCHIVO` (o `--json`, en una línea).
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
| `huella.py` | Cotas de un `.kicad_mod`: pads, paso, taladros, vías y pasta del pad expuesto, patio, serigrafía, 3D; cruce pin ↔ pad con `--simbolo` | `python herramientas/kicad/huella.py esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm --proyecto hardware/v2 --simbolo esp-riego:BTT6050-1ERA` |
| `restricciones.py` | Anchos, separaciones y vías por red de la PCB frente a la tabla de restricciones (CSV o Markdown) | `python herramientas/kicad/restricciones.py hardware/v2 docs/diseno/restricciones.csv` |
| `comprobar.py` | Los 19 puntos `[auto]` de las checklists de esquema, layout y librerías; `verificar.py` los añade a su informe | `python herramientas/kicad/comprobar.py hardware/v2 --punto librerias.fichas` |

`_comun.py` tiene lo compartido: expresiones S, hojas del proyecto, tablas de librerías, copia de trabajo, `kicad-cli`, netlist y el límite de 30 líneas.

## Formatos

- **Tabla de campos** (`campos.py`, `hoja.py generar --campos`): CSV con `Refs` (`R1`, `R26-R31`, `C45, C46`), una columna por campo (`Value`, `Footprint`, `LCSC Part#`, `MPN`, `Fabricante`, `Datasheet`, `Description`) y `DNP` (sí/no). Celda vacía: no se toca.
- **Descripción de hoja** (`hoja.py`): JSON con `papel`, `cajetin`, `piezas` (`ref`, `simbolo`, `x`, `y`, `giro`, `campos`, `dnp`, `pines`), `banderas` (PWR_FLAG) y `textos`. Cada pin visible lleva su conexión, dibujada en el extremo del pin y sin cables: `L:RED` (local), `H:RED:forma` (jerárquica), `G:RED:forma` (global), `P:GND` (símbolo de `power`), `NC` o `""`.
- **Tabla de colocación** (`colocar.py`): CSV `ref,x,y,giro,cara`, en mm y grados, cara `F` o `B`.
- **Tabla de restricciones** (`restricciones.py`): `Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas`, con `Vía` (taladro/corona) opcional. `comprobar.py` la busca en `<proyecto>/restricciones.csv` o en `docs/diseno/restricciones.csv`.

## Límites conocidos

- `hoja.py` no admite símbolos de varias unidades ni espejados, no dibuja cables y no toca los pines de hoja de la raíz. Se niega a sustituir una hoja con cables (`alimentacion.kicad_sch`) salvo con `--forzar`.
- `restricciones.py` mide la separación entre pistas y vías; la de pads y zonas la mide el DRC con la clase de red o la regla `.kicad_dru`, que es lo que la herramienta comprueba que existe.
- `huella.py` mide los pads `custom` por su ancla y trata las ventanas de pasta como rectángulos.
- `comprobar.py` no decide si un modelo 3D está alineado (se mira con `vista.py huella --3d`) ni cubre las checklists de fabricación y requisitos.
- `vista.py` rasteriza con el `wx` del Python de KiCad; los textos del SVG salen como trazos.

## Puntos de checklist que comprueba `comprobar.py`

Línea de cada checklist en su versión del 2026-11-11 (`gestion/checklists/`). Marca propuesta: `[auto: comprobar.py <punto>]`.

| Checklist | Línea | Punto de la checklist | `comprobar.py` |
|---|---|---|---|
| esquema | 9 | Hojas jerárquicas por bloque; ninguna hoja huérfana | `esquema.hojas` |
| esquema | 16 | `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet` y `Description` presentes | `esquema.campos` (fuera del BOM solo se piden `Value`, `Footprint` y `Description`) |
| esquema | 17 | La huella asignada existe | `esquema.huellas` |
| esquema | 18 | Huellas con vías según FAB-02 | `esquema.vias` |
| esquema | 19 | No montados marcados como DNP | `esquema.dnp` (hoja = tabla de campos = PCB; texto «DNP / no montar» sin marca) |
| layout | 12 | Zonas rellenadas | `layout.zonas` (que tengan relleno; no detecta un relleno anticuado) |
| layout | 14 | Sin `embedded_files` | `layout.incrustados` |
| layout | 15 | `outputdirectory` | `layout.salida` |
| layout | 24, 30 y 31 | Anchos, separación y corriente por red | `layout.restricciones` (`restricciones.py` con la tabla de restricciones; N/A mientras no exista) |
| layout | 44 | SMD solo en la cara superior | `layout.smd_cara` |
| layout | 49 | Modelo 3D en todos los componentes | `layout.3d` |
| librerías | 10 | Formato nativo | `librerias.formato` |
| librerías | 14 | Tablas con `${KIPRJMOD}` | `librerias.rutas` |
| librerías | 22 | Campos del símbolo | `librerias.campos` (símbolos de las librerías del `sym-lib-table`) |
| librerías | 28 | Courtyard presente y con margen | `librerias.patio` (≥ 0,1 mm; huellas del `fp-lib-table`) |
| librerías | 29 | Serigrafía fuera de los pads | `librerias.serigrafia` |
| librerías | 33 | Modelo 3D presente y alineado, en `.step`, y existe | `librerias.3d` cubre presente, STEP y existe; **alineado sigue siendo `[juicio]`** (`vista.py huella --3d`) |
| librerías | 35 | Extensiones 3D como `binary` | `librerias.gitattributes` |
| librerías | 43 | Ficha del componente | `librerias.fichas` (algún `.md` de `hardware/componentes` cita el código LCSC y tiene tipo, fecha y datasheet) |

Sin cubrir: `requisitos.md` (IDs citados) y los ocho puntos de `fabricacion.md`, que van con el paquete de fabricación (fase 5).

## Enganche en `herramientas/verificar.py`

`verificar.py` llama a `comprobar.para_verificar(carpeta)` después de restaurar el proyecto y antes de imprimir: añade las líneas de los puntos a su informe y, con `--json`, la clave `auto`. No cambia `limpio` ni el código de salida.

## Pruebas

`python herramientas/pruebas/test_kicad.py` (sin red, unos minutos; necesita KiCad 10). Trabaja sobre una copia temporal de `hardware/v2`, `hardware/libraries` y `hardware/componentes`.
