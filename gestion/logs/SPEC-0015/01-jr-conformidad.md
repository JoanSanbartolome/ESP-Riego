---
spec: SPEC-0015
agente: jr-conformidad
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0015 · 01 · jr-conformidad

## Orden recibida

SPEC-0015 · rama de la spec `spec/SPEC-0015-recopilacion-componentes` (el directorio de trabajo está en `spec/SPEC-0014-limpieza-v2`: intencionado, el coordinador repartirá los archivos). Haz la spec entera: fichas en `hardware/componentes/`, datasheets oficiales (≤ 5 MB) en `hardware/componentes/datasheets/`, símbolo, huella y 3D según el orden de preferencia (librería oficial de KiCad 10 citada, no copiada; lo demás en `hardware/libraries/esp-riego.kicad_sym`, `esp-riego.pretty` y `3d/`, en `.step`), LCSC, tipo, stock y precio con fecha. Reglas del paralelo: nunca `open_project` ni herramientas del MCP que carguen o guarden proyecto o placa; no tocar `hardware/v2/`, `hardware/v1-tfg/` ni las librerías de la v1.

## Contexto consultado

- `gestion/specs/SPEC-0015-recopilacion-componentes.md`, `gestion/checklists/librerias.md` v2, `gestion/plantillas/componente.md`, `docs/diseno/estudio-salidas.md` (§11 y tabla de costes), `docs/02-especificaciones-v2.md` (ALI-01…05, MCU-01, MCU-03, AMB-01) y mi memoria.
- Librería oficial de KiCad 10.0.6 en `C:\Program Files\KiCad\10.0\share\kicad\` (símbolos, huellas y 3D): lectura.
- Datasheets (con las páginas citadas en cada ficha): ESP32-S3-WROOM-1 v1.8, USBLC6-2 Rev 5, HRO TYPE-C-31-M-12 (hoja única), Infineon BTT6050-1ERA y BTT6030-2ERA Rev 1.00, BSP752R V1.3, serie Littelfuse SMBJ, TI TPS2663 SLVSE94G, TI LM5069 SNVS452G, Sensirion SHT4x v6.2, Kangnex WJ500V-5.08 (hoja única).
- PartReel (`search_parts_registry`): sin resultados para BTT6050, BTT6030, BSP752 e ISP752; para TPS2663 solo TPS26631 (otras variantes); SHT4x con tres piezas de terceros (SparkFun, Antmicro, CERN) que no se han usado.
- JLCPCB/LCSC: la base local de `search_jlcpcb_parts` está vacía (`get_jlcpcb_part` da «Part not found»). Se ha consultado la API web de JLCPCB (`jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList`) y la ficha de LCSC para código, stock, tipo (`base` = Basic, `expand` = Extended) y tramos de precio, el 2026-11-05.

## Acciones

1. Comprobada la rama (`spec/SPEC-0014-limpieza-v2`, avisada en la orden) y que no hay `.lck` que afecten a las librerías. No se ha usado `open_project` ni ninguna herramienta que cargue o guarde proyecto o placa; solo `search_parts_registry` y `get_registry_part`.
2. Códigos LCSC, stock, tipo y precio de las 11 familias (tabla más abajo).
3. Datasheets: descargados de ESP32-S3-WROOM-1 (Espressif) y LM5069 (TI) desde el fabricante, y el resto desde la copia de LCSC (los enlaces `www.lcsc.com/datasheet/...` devuelven HTML sin el PDF desde `curl`; los PDF se obtuvieron por el enlace de archivo que da la API de JLCPCB). TPS2663 pesa 5,7 MB (> 5 MB): solo enlace. ST no responde desde `curl` (código 000): se usa la copia de LCSC, que es el PDF de ST. Descartados los HTML falsos antes de guardar.
4. Símbolos creados en `hardware/libraries/esp-riego.kicad_sym`: BTT6050-1ERA, BTT6030-2ERA y BSP752R.
5. Huellas creadas en `hardware/libraries/esp-riego.pretty/`: `Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` y `TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal`.
6. Modelos 3D en `hardware/libraries/3d/` (formato `.step`): `Infineon_PG-TDSO-14.step` y `TerminalBlock_Kangnex_WJ500V-5.08-2P.step` (generados con un script propio, cajas con color), `Sensirion_DFN-4_1.5x1.5mm_SHT4x_simplificado.step` (propio) y `USB_C_Receptacle_HRO_TYPE-C-31-M-12.step` (copia del modelo oficial que KiCad distribuye en `demos/royalblue54L_feather`, porque la instalación 10.0.6 no trae el de la librería).
7. 11 fichas en `hardware/componentes/`.

## Tabla de componentes (consulta 2026-11-05)

| Componente | Origen de símbolo / huella / 3D | LCSC | Tipo | Stock | Precio unitario (USD) |
|---|---|---|---|---|---|
| ESP32-S3-WROOM-1-N8 | oficial `RF_Module` (los tres) | C2913198 | Extended | 4 641 | 4,9208 (1-9), 4,2437 (10-29) |
| USBLC6-2SC6 (ST) | oficial `Power_Protection` / `Package_TO_SOT_SMD:SOT-23-6` | C7519 | Extended | 46 715 | 0,1795 (1-49) |
| TYPE-C-31-M-12 (HRO) | oficial `Connector:USB_C_Receptacle_USB2.0_16P` / `Connector_USB:…HRO_TYPE-C-31-M-12`; 3D ausente en la instalación: respaldo copiado de los demos de KiCad | C165948 | Extended | 152 447 | 0,1868 (1-49) |
| BTT6050-1ERA | **creados** símbolo, huella y 3D (no hay en KiCad ni en PartReel; la API de EasyEDA no es accesible) | C534868 | Extended | 1 698 | 1,0941 (30-99) |
| BTT6030-2ERA | **creado** símbolo; huella y 3D compartidos con el BTT6050 | C534865 | Extended | 10 626 | 2,5005 (10-29), 2,2028 (30-99) |
| BSP752R | **creado** símbolo; huella y 3D oficiales `Package_SO:Infineon_PG-DSO-8-24_4x5mm` | C112644 | Extended | 288 | 1,1350 (30-99) |
| SMBJ33A (Littelfuse) | oficial `Device:D_TVS` / `Diode_SMD:D_SMB` | C224019 | Extended | 9 752 | 0,1229 (1-49) |
| TPS2663x (TPS26632RGER) | oficial `Power_Management:TPS26632RGE` / `Package_DFN_QFN:Texas_RGE0024H_…` | C1850278 | Extended | 1 631 | 3,5258 (1-9), 2,9993 (10-29) |
| LM5069MM-2/NOPB | oficial `Power_Management:LM5069MM-2` / `Package_SO:MSOP-10_3x3mm_P0.5mm` | C111822 | Extended | 9 471 | 4,9764 (1-9), 4,3827 (10-29) |
| SHT40-AD1B-R3 (familia SHT4x) | oficial `Sensor_Humidity:SHT4x` y huella `…SHT4x_NoCentralPad`; 3D ausente: respaldo simplificado creado | C2848306 | Extended | 15 537 | 1,8529 (1-9), 1,5732 (10-29) |
| WJ500V-5.08-2P (Kangnex) | símbolo oficial `Connector:Screw_Terminal_01x02`; **creados** huella y 3D | C8465 | Extended | 284 732 | 0,1345 (1-49), 0,1083 (50-149) |

Los 11 son Extended; ninguno es Basic ni *Preferred*. Los precios a 5 y 10 placas están en cada ficha.

## Decisiones y justificación

- **Familia TPS2663x:** se cita el símbolo oficial de la variante con más stock (TPS26632RGE, 1 631) y se anota que el 26632 y el 26633 tienen *clamp* fijo de 35 V (p. 2 de TI), con entrada hasta 30 V (ALI-01) y avisos a 31 V (ALI-09). Es dato para el bloque de entrada, no una elección.
- **BSP752R:** huella oficial `Infineon_PG-DSO-8-24_4x5mm`, cuya descripción cita este mismo datasheet (p. 17).
- **PG-TDSO-14:** el datasheet de Infineon solo da el dibujo del encapsulado (p. 49 del BTT6050; p. 51 del BTT6030) y no incluye *land pattern*. Se ha derivado con IPC-7351 (ver «Cotas»). La alternativa de la librería oficial, `Infineon_PG-TSDSO-14-22`, es otro encapsulado (paso 0,65 mm) y no sirve.
- **3D de TYPE-C-31-M-12 y SHT4x:** las huellas oficiales apuntan a `.step` que no están en la instalación de KiCad 10.0.6 (la carpeta `3dmodels` es un subconjunto). No se ha descargado de `kicad-packages3D` en GitLab porque no es una de las fuentes permitidas por la orden. Para el USB-C se ha usado el mismo modelo que KiCad distribuye en sus demos; para el SHT4x, un modelo simplificado propio.
- **EasyEDA:** la API `easyeda.com/api/products/<C>/components` responde 403. No se ha insistido con otros métodos de acceso. No se ha usado el paso 3 (JLCPCB/LCSC convertido) por ello.
- **Stock:** se cita el stock de 2026-11-05. BSP752R (288) y TPS26631 (639) son los de menos margen; BTT6050 (1 698) cubre las 60 unidades de 10 placas.

## Cotas de la huella PG-TDSO-14 (para validación)

Fuente: BTT6050-1ERA Rev. 1.00, §11, Figura 53, p. 49 (igual en BTT6030-2ERA, Figura 54, p. 51).

| Elemento | Datasheet (p. 49) | Huella |
|---|---|---|
| Cuerpo | 8,65 ± 0,1 × 3,9 ± 0,1 mm | silueta Fab ±4,325 × ±1,95 |
| Altura | 1,15 máx.; *standoff* 0,05 | 3D: cuerpo de z = 0,05 a 1,15 |
| Paso | 1,27 mm, 14 patillas | pads a y = ±3,81 … ±0,635 |
| Ancho de patilla | 0,4 ± 0,05 | pad de 0,6 (patilla + 0,2) |
| Extensión de patillas | 6,0 ± 0,2 mm punta a punta; pie de 0,67 ± 0,25 mm | pad de 1,5 × 0,6, centro en x = ±2,6 (borde exterior ±3,35; interior ±1,85) |
| Pad térmico (VS) | 2,65 ± 0,1 × 6,4 ± 0,1 (vista inferior) | pad 15 de 2,65 × 6,4, en F.Cu y F.Mask; pasta en dos ventanas de 2,2 × 2,9 |
| Pin 1 | marca de índice en la esquina de la patilla 1 | pads 1-7 a la izquierda, de arriba abajo; 8-14 a la derecha, de abajo arriba; triángulo en serigrafía y en Fab |
| Courtyard | no dado | ±3,6 × ±4,6 mm |

Pads derivados con IPC-7351 (toe 0,35 mm sobre la punta de 6,0 mm; talón calculado con el pie de 0,67 mm). Distancia mínima de cobre pad–EP: (1,85 − 1,325) = 0,525 mm.

**Huella WJ500V:** taladros de Ø 1,2 mm a 5,08 mm (layout recomendado del dibujo del fabricante, hoja única, ± 0,05); pad de 2,4 mm (anillo de 0,6 mm); cuerpo 10,16 × 10,0 mm. La posición del pin dentro del cuerpo no está acotada con claridad: supuesta centrada.

## Verificación

- `kicad-cli sym upgrade` y `kicad-cli fp upgrade -o <scratchpad>` sobre `esp-riego.kicad_sym` y `esp-riego.pretty`: «was not updated», es decir, ya están en el formato actual. `kicad-cli sym export svg` y `fp export svg`: exportan los 3 símbolos y las 2 huellas sin errores.
- Prueba de modelos 3D con una placa de prueba en el *scratchpad*, fuera del repositorio: `kicad-cli pcb export step` y `pcb render` cargan los modelos de la huella TDSO-14 y del borne (120 caras en el STEP, el mapa de caras esperado) y la imagen muestra el cuerpo con las patillas bien alineadas.
- Correspondencia símbolo ↔ huella: BTT6050 y BTT6030, pines 1-15 (el 15 es el *tab* VS) frente a los pads 1-15; BSP752R, pines 1-8 frente a los 8 pads de `Infineon_PG-DSO-8-24_4x5mm`.
- Rutas: ninguna ruta absoluta en `esp-riego.kicad_sym`, `esp-riego.pretty` ni en las fichas; los modelos 3D usan `${KIPRJMOD}/../libraries/3d/…` (KIC-01).
- `.gitattributes` ya marca `.step`/`.STEP` y `.pdf` como `binary`.
- `python herramientas/verificar.py`: no aplica, no he tocado ningún proyecto KiCad. `hardware/v2/`, `hardware/v1-tfg/`, las librerías de la v1 y el TFG no se han modificado. El MCP no ha cargado ningún proyecto.

## Requiere verificación de validación

Cada pieza creada o convertida, con el datasheet y la página del dibujo recomendado. Ninguna se ha autovalidado.

| Pieza | Archivo | Datasheet y página | Qué comprobar |
|---|---|---|---|
| Símbolo BTT6050-1ERA | `hardware/libraries/esp-riego.kicad_sym` | BTT6050-1ERA Rev 1.00, §3.2 Tabla 2, p. 4 | Números y nombres de pin; NC apilados (1, 2, 7, 8, 9, 13, 14) y OUT apilado (10, 11, 12) como un único pin visible; tipos eléctricos |
| Símbolo BTT6030-2ERA | ídem | BTT6030-2ERA, §3.2 Tabla 2, p. 4 | Igual; OUT0 = 12-14, OUT1 = 8-10, NC 7 y 11 |
| Símbolo BSP752R | ídem | BSP752R V1.3, p. 2 (imagen de la tabla de pines) | Pines 1-8; Vbb (5-8) apilados; ST como drenador abierto |
| Huella PG-TDSO-14 | `hardware/libraries/esp-riego.pretty/Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm.kicad_mod` | BTT6050-1ERA, Figura 53, p. 49; BTT6030-2ERA, Figura 54, p. 51 | Tabla de cotas de arriba. **El datasheet no da *land pattern*:** los pads son derivados (IPC-7351), la validación debe aceptarlos o pedir el *land pattern* de Infineon (Package Information `PG-TDSO-14-1`). Pin 1, courtyard, serigrafía fuera de los pads |
| Modelo 3D `Infineon_PG-TDSO-14.step` | `hardware/libraries/3d/` | BTT6050-1ERA, Figura 53, p. 49 | Cuerpo 8,65 × 3,9 × 1,15, patillas y pad; alineación con la huella. Simplificado, de generación propia |
| Huella WJ500V-5.08-2P | `esp-riego.pretty/TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal.kicad_mod` | Dibujo Kangnex (hoja única, C8465), *layout* recomendado | Taladro Ø 1,2, paso 5,08, pad de 2,4; **posición del pin en el cuerpo y sentido de la entrada de cable supuestos** |
| Modelo 3D `TerminalBlock_Kangnex_WJ500V-5.08-2P.step` | `hardware/libraries/3d/` | ídem | Prisma de 10,16 × 10 × 14 con pines de 0,8 × 4,5 mm bajo la placa |
| Modelo 3D `Sensirion_DFN-4_1.5x1.5mm_SHT4x_simplificado.step` | `hardware/libraries/3d/` | Sensirion SHT4x v6.2, §5.2, Figura 15, p. 14 | **Altura supuesta de 0,5 mm** (el texto del PDF no la da); 4 pads según la huella oficial. Hay que enlazarlo en el PCB porque la huella oficial apunta a otro archivo |
| Modelo 3D `USB_C_Receptacle_HRO_TYPE-C-31-M-12.step` | `hardware/libraries/3d/` | HRO TYPE-C-31-M-12 (hoja única) | No creado por mí: copia del modelo oficial de los demos de KiCad 10.0.6 (`royalblue54L_feather`); comprobar que coincide con la huella oficial |

Las huellas y símbolos oficiales (ESP32-S3-WROOM-1, USBLC6-2SC6, USB-C, SMBJ33A, TPS2663x, LM5069, SHT4x y la huella del BSP752R) no se han creado ni modificado: se citan.

## Addenda (autorización del usuario para descargar de kicad-packages3D)

El coordinador autorizó descargar los dos `.step` oficiales de `gitlab.com/kicad/libraries/kicad-packages3D`. Resultado, el 2026-11-05: `raw/master/...` y `raw/10.0/...` devuelven 404 para los dos archivos (también con extensión `.STEP`). El listado de la API de GitLab confirma que no existen: `Connector_USB.3dshapes` contiene solo otros conectores (ningún HRO) y `Sensor_Humidity.3dshapes` solo `Texas_S-PWSON-N6-HDC2080.step`. Las huellas oficiales referencian modelos que el repositorio oficial no publica. No hay nada que sustituir: se mantienen el `USB_C_Receptacle_HRO_TYPE-C-31-M-12.step` (copia del modelo de los demos de KiCad 10.0.6) y el `Sensirion_DFN-4_1.5x1.5mm_SHT4x_simplificado.step`. No se ha descargado ningún archivo (se descartaron dos páginas HTML de error de 2 699 bytes).

## Pendiente

- **Decisión del coordinador (resuelta en la addenda: no existen en el repositorio oficial; quedan los de respaldo):** los modelos `.step` oficiales de `USB_C_Receptacle_HRO_TYPE-C-31-M-12` y `Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad` no están en la instalación de KiCad 10.0.6. ¿Se autoriza descargarlos del repositorio oficial `kicad-packages3D`, o se quedan los de respaldo?
- **Primer bloque que use cada pieza:** inscribir `esp-riego` en `sym-lib-table` y `fp-lib-table` con `${KIPRJMOD}/../libraries/…` y enlazar el 3D de respaldo en las instancias del USB-C y del SHT4x (esta spec no toca `hardware/v2/`).
- **Si el *land pattern* de Infineon difiere** de la derivación IPC, hay que corregir `esp-riego.pretty/Infineon_PG-TDSO-14_…`.
- **Elección de variante** en el bloque de entrada (TPS26630 frente a TPS26632 por el *clamp* de 35 V) y en el bloque MCU (N8 u otra).
- **Coherencia documental:** el estudio de salidas (§11) da para BSP752R 277 uds de stock y para BTT6050 1 748; el 2026-11-05 son 288 y 1 698. Pide actualizarlos si se cita el stock en un documento definitivo. SMAJ33CA para V2 sigue sin código (`docs/diseno/estudio-salidas.md`, sec. de 60 V): irrelevante si se mantiene DC (SMBJ33A).
- Los demás hallazgos del estudio de salidas (códigos LCSC de AO3400A, 1N4148W, SMAJ48CA…) no estaban en el alcance y no se han confirmado.

## Notas para el siguiente agente

- La API de JLCPCB (`selectSmtComponentList`) funciona con un POST JSON y da stock, tramos de precio, `componentLibraryType` (`base` = Basic, `expand` = Extended) y `preferredComponentFlag`.
- Para leer símbolos de la librería oficial con herencia (`extends`), los pines están en el padre: `LM5069MM-2` extiende `LM5069MM-1` y `USBLC6-2SC6` extiende `USBLC6-2P6`.
- Los scripts que han generado huellas, símbolos y STEP están en el *scratchpad* de la sesión (no versionados). Si hay que regenerar, el STEP necesita `MANIFOLD_SOLID_BREP` con `ADVANCED_FACE`: `FACETED_BREP` con `FACE` simple no lo carga KiCad.

## Corrección (VAL-0015-01)

Fecha: 2026-11-05. Rama `spec/SPEC-0015-recopilacion-componentes`. Sin MCP (ni `open_project`); sin tocar `hardware/v2/`, la v1 ni el TFG. Los modelos 3D no se han integrado (los rehace otro agente). La afirmación de «Decisiones» de que el datasheet no da *land pattern* queda sustituida por esta corrección.

### Hallazgo → cambio → evidencia

| Hallazgo | Cambio | Evidencia |
|---|---|---|
| M01 | `Infineon_PG-TDSO-14_…kicad_mod` rehecha con el *land pattern* oficial de PG-TDSO-14-11: pads de señal 1,34 × 0,65 con centro en x = ±2,73 (filas a 5,46); pad 15 (VS) igual, 2,65 × 6,4; pasta del pad térmico en 2 ventanas de 2,45 × 2,95 en y = ±1,625 (0,3 entre ellas); courtyard ±3,65 × ±4,6. Se conservan nombre, numeración (1-7 izquierda, 8-14 derecha, 15 = VS), triángulo del pin 1, serigrafía y `model`. `descr` y `Datasheet` citan Infineon | Fuente: `https://www.infineon.com/package/PG-TDSO-14-11`, imagen «footprint» (`assets.infineon.com/is/image/infineon/infineon-pg-tdso-14-11-png-footprint-en.png`), descargada y leída el 2026-11-05. Cotas leídas: paso 1,27; pad 0,65 × 1,34; 5,46 entre filas; cobre del pad térmico 2,65 × 6,4; ventanas de pasta 2,95 × 2,45 con 0,3 de separación. Derivados: borde interior ±2,06 (hueco de 0,735 al pad térmico) y exterior ±3,40; courtyard a 0,25 de los pads. Render `fp export svg` sobre copia correcto; `fp upgrade`: «not updated» (formato nativo) |
| M03, B04, B09 | `TerminalBlock_Kangnex_WJ500V-…kicad_mod`: cuerpo de y = −5,5 (cara de entrada del cable) a +4,5 (cara trasera), x de −2,54 a 7,62 en Fab; serigrafía a +0,1; courtyard a +0,25 (y −5,75…4,75). Entrada marcada en Fab (línea gruesa, flecha y texto «ENTRADA CABLE»). Pin 1 con triángulo en F.SilkS y F.Fab. Taladro acabado 1,3 mm y pad de 2,6 mm (antes 1,2 y 2,4). Reference y Value fuera del courtyard | Dibujo de Kangnex, sección A-A: patilla a 4,50 ± 0,20 de la cara trasera (fondo 10,00, luego 5,50 a la entrada). Patilla 0,90 × 0,80 (diagonal 1,27 máx.); referencia Phoenix MKDS-1,5-2-5.08 (1,3 / 2,6). Render sobre copia: entrada, pin 1 y courtyard como se describen; `fp upgrade`: «not updated» |
| B06 | Ficha `WJ500V-5.08-2P.md`: precio a 5 y 10 placas con el supuesto de 7 bornes por placa (6 salidas, REL-06, más la entrada): 35 × 0,1345 = 4,71 $ y 70 × 0,1083 = 7,58 $; con 8 bornes, 5,38 $ y 8,66 $. Frase contradictoria eliminada; quitado el «supuesto» de la posición del pin; taladro de 1,3 justificado | API de JLCPCB, 2026-11-05 (tramos 1-49: 0,1345; 50-149: 0,1083) |
| B07 | Ficha `BSP752R.md`: V_IN(T+) ≤ 2,2 V, V_IN(T−) ≥ 0,8 V, histéresis 0,4 V y V_ST(low) ≤ 0,4 V (p. 6); I_L(SCp) 9 A máx. (−40 °C, 20 V), 6,5 A típ. (25 °C), 4 A mín. (150 °C) (p. 5). Sin «dato del gemelo». Criterio de páginas: número impreso (entre paréntesis, el del PDF) | `datasheets/BSP752R.pdf` V1.3 (2017-06-13), páginas 5 y 6 leídas en imagen |
| B08 | `datasheet:` con URL del fabricante y la de LCSC en `datasheet_espejo:` (BTT6050, BTT6030, BSP752R, SMBJ33A); Sensirion actualizada. Mismo cambio en el campo `Datasheet` de los 3 símbolos y de la huella TDSO-14 | Infineon: los PDF de `infineon.com/assets/row/public/documents/10/49/infineon-<mpn>-datasheet-en.pdf` son idénticos byte a byte (MD5) a las copias locales; igual ESP32-S3-WROOM-1 (Espressif), LM5069 y TPS2663 (TI). **SHT4x:** la copia local era la v6.2 (2023) y la vigente en la página de producto de sensirion.com es la **V7.3 (junio de 2026)**: sustituida (1,0 MB). Páginas de la ficha pasadas a la V7.3 (Figura 15, p. 15; §5.3, p. 16; pinout y θ_JA, p. 17); la URL antigua daba 404. **No comprobado:** `st.com` no responde y `littelfuse.com` da 403 desde este equipo: no he podido confirmar que USBLC6-2 Rev 5 y SMBJ de 07/04/25 sean las vigentes (anotado en las fichas). TYPE-C-31-M-12 y WJ500V: sin sede de fabricante accesible, LCSC es la única fuente (anotado) |
| B10 | Símbolos BTT6050-1ERA y BTT6030-2ERA: Value movido bajo el extremo del pin NC, en (0, −15,24) y (0, −17,78) | `sym export svg` sobre copia: Value por debajo del pin NC sin solaparse. Pines y conexiones sin cambios. No añadí los números del grupo (OUT 10-12), fuera de la orden |

### Requiere verificación de validación (actualizado)

| Pieza | Fuente y página |
|---|---|
| Huella PG-TDSO-14 (corregida) | Land pattern: `https://www.infineon.com/package/PG-TDSO-14-11`; cuerpo: BTT6050-1ERA Rev 1.00, Figura 53, p. 49 |
| Huella WJ500V (corregida) | Dibujo de Kangnex, sección A-A y layout recomendado; taladro 1,3 justificado en la ficha |
| Símbolos BTT6050 y BTT6030 | Solo cambian la posición de Value y el campo Datasheet |
| `datasheets/SHT4x.pdf` | Sustituido por la V7.3 de Sensirion |

### Repaso de la checklist `librerias.md` v2

- Huella (cotas del fabricante, pin 1, courtyard, serigrafía): cumple en las dos huellas modificadas; la TDSO-14 con el land pattern de Infineon; el WJ500V con pin 1 en serigrafía y Fab, entrada marcada y taladro justificado.
- Símbolo: sin cambios de pines; B10 solo cosmético.
- Modelo 3D: resuelto con los modelos nuevos (ver «Integración de los modelos 3D nuevos»: hallazgos 02, 03 y 05).
- Ficha (datasheet del fabricante con revisión, LCSC con fecha, tipo, stock, precios): cumple, con las excepciones de ST, Littelfuse, HRO y Kangnex.
- Rutas absolutas: ninguna; archivos en formato nativo (`upgrade`: «not updated»).
- Autovalidación: no. `verificar.py` no aplica (ningún proyecto KiCad tocado). `revisar_zonas.py jr-conformidad`: todo dentro de su zona.

### Integración de los modelos 3D nuevos (SolidCraft)

- Copiados a `hardware/libraries/3d/`: `Infineon_PG-TDSO-14.step` y `TerminalBlock_Kangnex_WJ500V-5.08-2P.step` (sustituyen a los anteriores) y `Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step` (nuevo). Borrado `Sensirion_DFN-4_1.5x1.5mm_SHT4x_simplificado.step`.
- Fuentes en `hardware/libraries/3d/fuentes-solidcraft/` (`gen.py`, `sht4x.json`, `pgtdso14.json`, `borne.json`, `INFORME.md` y un `README.md` de 3 líneas). Sin rutas absolutas en ellos.
- Las dos huellas propias ya tenían `(model …)` con offset 0, rotación 0 y escala 1 (`${KIPRJMOD}/../libraries/3d/…`): sin cambios.
- Fichas SHT4x, BTT6050-1ERA, BTT6030-2ERA y WJ500V: modelo, origen, cotas con página y supuestos; en la del SHT4x, la ruta de respaldo `${KIPRJMOD}/../libraries/3d/Sensirion_DFN-4_1.5x1.5mm_P0.8mm_SHT4x_NoCentralPad.step` que el bloque enlazará.
- Comprobación: placa de prueba en el scratchpad (`v15b/prueba.kicad_pcb`) con la huella oficial del SHT4x y las dos propias, con los modelos de `hardware/libraries/3d/`. `kicad-cli pcb render --side top` (y vista en perspectiva): los tres modelos cargan con color. TDSO-14: patillas sobre los pads (1–7 izquierda, 8–14 derecha) y la marca del pin 1 junto al pad 1, donde está el triángulo de la serigrafía. SHT4x: cuerpo sobre sus 4 pads y marca en la esquina del pad 1. Borne: el cuerpo coincide con el contorno Fab (y = −5,5…+4,5), los dos pines sobre los pads, y la cara de entrada del cable hacia −Y, donde está la marca «ENTRADA CABLE» (en la vista en perspectiva se ve la cara trasera, con el escalón del perfil, hacia +Y). Observación: las patillas del TDSO-14 llegan a |x| = 3,0 y el pad llega a 3,40, así que quedan 0,4 mm de pad libre en la punta: es soldable y coincide con el pie de 6,0 mm de punta a punta del datasheet.
- Repaso de la checklist `librerias.md` v2, modelo 3D: presente (3 de 3 modelos propios); `.step`; alineado con las huellas (origen, pin 1 y contorno comprobados en el render); sin rutas absolutas. El 3D de respaldo del USB-C no ha cambiado.

### Confirmaciones del usuario (2026-11-05, trasladadas por el coordinador)

- 7 bornes por placa (6 salidas y la entrada): ficha del WJ500V actualizada («confirmado por el usuario»).
- Copias locales del USBLC6-2SC6 (ST, Rev 5) y de la serie SMBJ (Littelfuse, 07/04/25) válidas como vigentes: fichas actualizadas («confirmado por el usuario»). No se han contrastado con la web de cada fabricante (ST no responde y Littelfuse da 403 desde este equipo).

### Pendiente

- Nada de esta corrección. La revisión de ST y de Littelfuse queda como confirmada por el usuario.
