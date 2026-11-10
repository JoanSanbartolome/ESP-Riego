---
id: SPEC-0024
titulo: Piezas del bloque de salidas
fase: 2
estado: cerrada
responsable: jr-conformidad
revisor: ing-validacion
rama: spec/SPEC-0024-piezas-salidas
requisitos: [REL-01, REL-03, REL-05, REL-07, REL-10, FAB-02, FAB-05, FAB-11, KIC-01]
depende_de: [SPEC-0023, SPEC-0022]
creada: 2026-11-06
cerrada: 2026-11-10
validacion: VAL-0024-01
---

# SPEC-0024 · Piezas del bloque de salidas

## Objetivo

Todas las piezas de la lista de `docs/diseno/salidas.md` §9 tienen símbolo, huella y 3D resolubles desde `hardware/v2`, con sus campos completos, su tipo de JLCPCB (Basic/Extended) y su stock confirmados con fecha, y sus fichas en `hardware/componentes/`. El log deja la tabla de campos por referencia lista para SPEC-0025.

## Alcance

- Incluye:
  - **Huella del BTT6050 y FAB-02.** `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` no lleva vías (comprobado por el coordinador el 2026-11-10: ningún pad `thru_hole`; EP = pad 15 de 2,65 × 6,4 mm; pasta en dos aperturas de 2,45 × 2,95 mm, 85 % del EP). Se le añaden las vías térmicas del EP en el mismo archivo y con el mismo nombre (lo citan `salidas.md` §9 y las fichas BTT6050-1ERA y BTT6030-2ERA):
    - ≥ 8 vías (`salidas.md` §11) de taladro 0,3 mm y diámetro 0,6 mm (FAB-02), numeradas «15» (el *tab* es VS = BUS_24V, no GND), con el anillo entero dentro del cobre del EP;
    - distancia entre taladros según las capacidades de JLCPCB estándar (se cita el parámetro);
    - pasta sin cubrir los taladros, repartida como en las huellas oficiales `*_ThermalVias` de KiCad; se anota la cobertura de pasta resultante y la elección de máscara y de cobre en la cara inferior, con su motivo (el polígono BUS_24V lo pone el layout);
    - se consulta si el *land pattern* de Infineon (`infineon.com/package/PG-TDSO-14-11`) o el datasheet recomiendan un patrón de vías; si no, se justifica el elegido;
    - los pads 1–14, el tamaño del EP, la serigrafía, el patio y el 3D no cambian: `git diff` solo muestra las vías, la pasta y `descr`.
  - **Resto de huellas.** Se confirma que ninguna otra huella de §9 lleva vías (`Resistor_SMD`, `Capacitor_SMD`, `LED_SMD:LED_0603_1608Metric` y `Diode_SMD:D_SMA` oficiales; en el borne propio, los `thru_hole` son las patillas).
  - **3D de todo (FAB-11).** Cada huella de §9 enlaza un `.step` que existe: las propias en `${KIPRJMOD}/../libraries/3d/` (BTT6050, borne) y las oficiales en `${KICAD10_3DMODEL_DIR}` (comprobado por el coordinador el 2026-11-10: existen los de `R_0603`, `R_0805`, `R_1206`, `C_0603`, `C_0805`, `C_1210`, `LED_0603_1608Metric` y `D_SMA`). Render con `kicad-cli pcb render` (caras superior e inferior) de una placa de prueba creada fuera de `hardware/v2` (en el *scratchpad* o en una carpeta temporal que se borra al terminar), con una huella de cada tipo: 3D sobre sus pads, pin 1 del BTT y del borne, cátodo del LED y del M7 sobre el pad 1, y vías del EP. Las imágenes van a `hardware/libraries/3d/fuentes-solidcraft/render_SPEC-0024_*.png`.
  - **Símbolos y mapeo pin ↔ pad** de todas las piezas de §9: `esp-riego:BTT6050-1ERA` (número, nombre y tipo eléctrico de los pines 1–15 frente a la Tabla 2, p. 4, y campos del símbolo de librería), `Connector:Screw_Terminal_01x02`, `Device:R`, `Device:C`, `Device:LED` y `Device:D`. En particular: cátodo del KT-0603R = pad 1 (ficha `KT-0603R.md`), cátodo (banda) del M7 = pad 1 de `D_SMA`, y pin 1 del borne.
  - **Fichas:**
    - nueva `M7.md` (MDD, C95872; D12–D17, DNP por DEC-0008) con el PDF en `datasheets/M7.pdf` (el del fabricante si se localiza; LCSC como espejo): V_RRM, I_F, V_F, I_R, polaridad y cotas del SMA frente a `Diode_SMD:D_SMA` (tabla de cotas con página);
    - `BTT6050-1ERA.md`, revisada entera: errata del datasheet en P_7.5.2 (p. 30: «I_IS(OL) = 8 mA» se lee 8 µA; razonamiento en `salidas.md` §3.2); uso en U7–U12 de `salidas.kicad_sch`; sin R_GND ni zéner en VS (`salidas.md` §4.4; hoy la ficha los cita como recomendados); vías del EP a BUS_24V, ya incluidas en la huella; BTT6030-2ERA con la misma huella pero **distinto pinout** (no intercambiable); stock, tipo y precio con fecha; `verificado_por`;
    - `WJ500V-5.08-2P.md`, revisada entera: uso en J1 (alimentación) y J4–J9 de `salidas.kicad_sch` (no `conectores.kicad_sch`), 7 por placa; pin 1 = OUT_n y pin 2 = GND en las salidas; stock con fecha; `verificado_por`;
    - `BTT6030-2ERA.md`: coherente con lo anterior (misma huella, ahora con vías; distinto pinout);
    - `bloque-alimentacion.md`, fila de D4: columna «Ficha» → `KT-0603R.md` y stock con su fecha de consulta (hoy 6 683 182 del 2026-11-05 y sin ficha);
    - D6–D11 usan `KT-0603R.md` (SPEC-0022), que solo cambia si cambia el stock;
    - las resistencias y condensadores genéricos no llevan ficha propia (como en SPEC-0021): los cubren las tablas del log.
  - **Tipo Basic/Extended y stock** en la API de JLCPCB, con fecha, de **todas** las piezas de §9, principales y alternativas, incluido el código LCSC que falta en la alternativa de R57–R62 (Yageo RC0805FR-0747KL). Stock del BTT6050 frente a las 60 unidades de 10 placas.
  - **Cambios de compra (DEC-0007).** Si una principal no tiene stock para 10 placas, o hay una equivalente Basic para una Extended con el mismo valor, tensión, tolerancia y encapsulado, se aplica: la tabla de campos lleva la pieza nueva y el log lo marca para `salidas.md`. Si la equivalencia exige recalcular, no se aplica: se propone en el log.
  - **Tabla de campos por referencia** en el log, para SPEC-0025: las 87 referencias de §9 (U7–U12, J4–J9, R26–R68, C27–C46, D6–D17), agrupadas por pieza, con `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Fabricante`, `Datasheet`, `Description` y `DNP`. Mismos nombres de campo y notación de valores que `mcu.kicad_sch` y `alimentacion.kicad_sch` (se consultan con Grep o Read, sin abrir el proyecto). `Datasheet`: URL del fabricante o, si no la hay, `dataManualUrl` de la API de JLCPCB (VAL-0021-01-02). D12–D17: `DNP` = sí, con el resto de campos completos y la lista de atributos de KiCad que los dejan fuera de BOM y CPL manteniendo la huella en la placa (DEC-0008).
  - **Cambios propuestos a `docs/diseno/salidas.md`** (fuera de la zona de jr-conformidad), en el log y con el texto exacto, para que los aplique ing-esquematicos en SPEC-0025: l. 434 (Anexo A, fila KT-0603R: «ficha propia si jr-conformidad la pide» → ficha `KT-0603R.md`, polaridad ② = cátodo = pad 1), §9 (stock, tipo y código de la alternativa de R57–R62), §11 (vías del EP ya en la huella) y Anexo A (ficha M7).
- Excluye:
  - editar o abrir con el MCP o `kicad-cli` cualquier archivo de `hardware/v2` (las tablas de librerías no cambian);
  - editar `docs/` (los cambios se proponen en el log);
  - cambiar valores o piezas elegidos en `salidas.md`, salvo los cambios de compra de DEC-0007 descritos arriba;
  - las vías del EP del TPS26632 y las del EPAD de U5 (layout y mantenimiento).

## Entradas

- `docs/diseno/salidas.md` (§0, §8, §9, §11 y Anexos A y B) y `gestion/logs/SPEC-0023/01-ing-esquematicos.md` y `03-ing-esquematicos.md`.
- DEC-0007 y DEC-0008; `docs/02-especificaciones-v2.md` v0.5 (FAB-02, FAB-05, FAB-11, KIC-01).
- `hardware/libraries/` (`esp-riego.kicad_sym`, `esp-riego.pretty/`, `3d/`) y `hardware/componentes/` (fichas BTT6050-1ERA, BTT6030-2ERA, WJ500V-5.08-2P, KT-0603R y bloque-alimentacion; `datasheets/BTT6050-1ERA.pdf`: Tabla 2, p. 4; P_7.5.2, p. 30; Fig. 53, p. 49).
- Checklists `gestion/checklists/librerias.md` (v3) y `gestion/checklists/esquema.md` (v6, punto de FAB-02).
- `gestion/logs/SPEC-0021/01-jr-conformidad.md` (formato de las tablas de stock y de campos).

## Entregables

- `hardware/libraries/esp-riego.pretty/Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm.kicad_mod` con las vías del EP.
- `hardware/componentes/M7.md` y `datasheets/M7.pdf`; fichas actualizadas `BTT6050-1ERA.md`, `WJ500V-5.08-2P.md` y `bloque-alimentacion.md`, y `BTT6030-2ERA.md` y `KT-0603R.md` si cambian.
- Renders en `hardware/libraries/3d/fuentes-solidcraft/`.
- Log `gestion/logs/SPEC-0024/01-jr-conformidad.md` con: repaso de `librerias.md` v3 punto por punto, tabla de stock y tipo con fecha, tabla de campos por referencia, tabla de cotas de las vías y la pasta del EP, mapeo pin ↔ pad, sección «Requiere verificación de validación» y cambios propuestos a `salidas.md`.

## Criterios de aceptación

- [ ] Cada pieza de §9 tiene símbolo, huella y 3D en `.step` resolubles desde `hardware/v2` (rutas `${KIPRJMOD}` o `${KICAD10_3DMODEL_DIR}`, archivos existentes); pines y pads comprobados contra el datasheet (página citada); render con el pin 1 y los cátodos.
- [ ] La huella del BTT6050 lleva ≥ 8 vías de 0,3 / 0,6 mm en el EP, numeradas 15 y sin pasta sobre los taladros; `git diff` no muestra cambios en los pads 1–14, el tamaño del EP, el patio ni la serigrafía. Ninguna otra huella del bloque lleva vías.
- [ ] Tipo Basic/Extended y stock de JLCPCB de todas las piezas de §9 (principales y alternativas) con fecha; los cambios de compra, justificados con DEC-0007.
- [ ] Ficha `M7.md` creada; `BTT6050-1ERA.md` con la errata de P_7.5.2 y los cambios del Anexo A de `salidas.md`; `WJ500V-5.08-2P.md` con el uso corregido; D4 de `bloque-alimentacion.md` con su ficha y el stock al día.
- [ ] La tabla de campos cubre las 87 referencias de §9, con D12–D17 marcados DNP.
- [ ] Los cambios a `salidas.md` (l. 434 y los que resulten) están propuestos en el log con el texto exacto.
- [ ] Checklist de librerías v3 pasada punto por punto.
- [ ] Ningún archivo de `hardware/v2` ni de `docs/` modificado.

## Validación

Nivel **completo** (pieza modificada y fichas; DEC-0005).

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-06 | coordinador | Crea la spec (propuesta) | |
| 2026-11-08 | coordinador | Recoge DEC-0008: D12–D17 DNP con su huella | DEC-0008 |
| 2026-11-10 | coordinador | Abre la spec (encargo del usuario): vías del EP del BTT6050, 3D, fichas, tipo y stock, y tabla de campos | |
| 2026-11-10 | jr-conformidad | Entrega: huella con 10 vías en el EP, ficha del M7, fichas revisadas, stock y tabla de campos | `c2401d6`, log 01 |
| 2026-11-10 | ing-validacion | Validación completa: 3 M y 4 B | VAL-0024-01 (APROBADO_CON_OBSERVACIONES) |
| 2026-11-10 | jr-conformidad | Corrige las observaciones 01–06: pasta del EP al 65 %, texto del tapado de las vías y cambios a `salidas.md` | `8efa234`, log 03 |
| 2026-11-10 | coordinador | Cierra la spec; correcciones comprobadas con un script sobre la huella (pasta igual al patrón de VAL-0024-01-01) y con Grep. La observación 07 pasa a mantenimiento | VAL-0024-01 |
