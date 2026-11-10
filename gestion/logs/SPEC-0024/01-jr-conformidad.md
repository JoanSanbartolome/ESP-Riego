---
spec: SPEC-0024
agente: jr-conformidad
n: 01
fecha: 2026-11-10
estado: completado
---

# SPEC-0024 · 01 · jr-conformidad

## Orden recibida

SPEC-0024 · rama spec/SPEC-0024-piezas-salidas · todo el alcance de la spec (vías del EP en la huella del BTT6050 a 0,3/0,6 mm; confirmación de vías y 3D del resto; render de la placa de prueba; símbolos y mapeo pin ↔ pad; ficha nueva M7.md con su PDF; revisión de BTT6050-1ERA.md, WJ500V-5.08-2P.md, BTT6030-2ERA.md y la fila de D4 de bloque-alimentacion.md; tipo y stock de JLCPCB con fecha de todas las piezas de salidas.md §9, principales y alternativas; tabla de campos de las 87 referencias con DNP en D12–D17; cambios propuestos a salidas.md con el texto exacto).

## Contexto consultado

- `gestion/specs/SPEC-0024-piezas-salidas.md`, `docs/diseno/salidas.md` (§3.2, §4.4, §8, §9, §10, §11, §13, Anexos A y B), `gestion/checklists/librerias.md` v3, `gestion/logs/SPEC-0021/01-jr-conformidad.md` (formato).
- `hardware/libraries/esp-riego.kicad_sym` (BTT6050-1ERA), `esp-riego.pretty/`, fichas de `hardware/componentes/`.
- BTT6050-1ERA Rev. 1.00: Tabla 2 (p. 4), P_7.5.2 (p. 30), §4.3.1 (pp. 9-10), Fig. 53 (p. 49).
- M7: `datasheets/M7.pdf` (MDD «M1 THRU M7», Rev. 2025A5, 3 págs.).
- Oficiales de KiCad 10.0.6: `Package_SO.pretty/HSOP-8-1EP_…_ThermalVias` (patrón de vías, `pad_prop_heatsink`, `zone_connect 2`, capa B.Cu), `Resistor_SMD`, `Capacitor_SMD`, `LED_SMD`, `Diode_SMD`, símbolos `Device` y `Connector`.
- Capacidades de JLCPCB: https://jlcpcb.com/capabilities/Capabilities (consulta 2026-11-10): vía mín. 0,15 / 0,25 mm (0,2 mm preferido), **separación vía-vía (taladro a taladro) 0,2 mm**; vía rellena de máscara: sin apertura en ninguna cara, ≥ 0,35 mm a otras aperturas, Ø ≤ 0,5 mm (la nuestra tiene Ø 0,3 de taladro: se tapa sin relleno).
- `infineon.com/package/PG-TDSO-14-11` (consulta 2026-11-10): la página (WebFetch) no devuelve el patrón de vías (solo navegación); el *land pattern* ya usado (SPEC-0015) no las trae y el datasheet solo dice «una matriz de vías térmicas bajo el pad expuesto» en la simulación 2s2p (nota 2, p. 9; Fig. 4) sin cotas. No hay patrón de vías recomendado: se justifica el elegido.
- API de JLCPCB `selectSmtComponentList` (2026-11-10).

## Acciones

1. **Huella del BTT6050** (`esp-riego.pretty/Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm.kicad_mod`): 10 vías, pasta rediseñada, pad 15 en B.Cu y `descr`. `git diff` confirma que no cambian los pads 1–14, el tamaño del EP, la serigrafía, el patio ni el 3D. Las UUID de los pads nuevos son nuevas; se conservan las del pad 15 F.Cu.
2. **Resto de huellas:** `R_0603`, `R_0805`, `R_1206`, `C_0603`, `C_0805`, `C_1210`, `LED_0603_1608Metric` y `D_SMA` oficiales: 0 pads `thru_hole` en cada una (grep). Borne propio: 2 `thru_hole` (patillas, taladro 1,3 mm), ninguna vía.
3. **Render** (placa de prueba en el *scratchpad*, fuera del repositorio; sin carpeta temporal en el repositorio): `hardware/libraries/3d/fuentes-solidcraft/render_SPEC-0024_top.png` y `_bottom.png` (BTT, borne, R 0603/0805/1206, C 0603/0805/1210, LED y D_SMA), y `render_SPEC-0024_led_m7.png` (LED y D_SMA ampliados).
4. **Fichas:** nueva `M7.md` + `datasheets/M7.pdf`; revisadas `BTT6050-1ERA.md`, `WJ500V-5.08-2P.md`, `BTT6030-2ERA.md`; `KT-0603R.md` (solo stock/fecha); fila de D4 de `bloque-alimentacion.md`.
5. **Stock y tipo:** API de JLCPCB, 2026-11-10, de todas las piezas de §9 (tabla abajo).
6. **MCP:** no usado. `hardware/v2` y `docs/` sin tocar.

## Decisiones y justificación

### Vías y pasta del EP (FAB-02; `salidas.md` §11)

| Cota | Valor | Motivo / fuente |
|---|---|---|
| EP (pad 15) | 2,65 × 6,4 mm (x ∈ ±1,325; y ∈ ±3,2) | sin cambios; Fig. 53, p. 49 |
| Vías | 10 (2 × 5), taladro 0,3 mm, Ø 0,6 mm, numeradas «15» | ≥ 8 (`salidas.md` §11); FAB-02. Anillo 0,15 mm |
| Posición | x = ±0,95; y = −2,4 · −1,2 · 0 · 1,2 · 2,4 | rejilla 1,9 × 1,2 mm |
| Anillo dentro del cobre | borde del anillo a x = ±1,25 (0,075 mm del borde del EP) y a y = ±2,7 (0,5 mm) | «anillo entero dentro del EP» ✔ |
| Taladro a taladro | 0,9 mm (misma columna), 1,6 mm (entre columnas); entre coronas de cobre 0,6 mm | JLCPCB: 0,2 mm (jlcpcb.com/capabilities) ✔ con margen 4,5× |
| Elección de 10 y no 8 | 10 vías a 1,2 mm de paso (recomendación habitual 1–1,2 mm) y el anillo exterior no se acerca a los pads 8–14 (hueco EP–pads 0,735 mm sin cambios) | no hay patrón de Infineon ni del datasheet (R_thJA = 50 K/W con ≥ 300 mm² de cobre, Fig. 7, p. 10) |
| Pasta | 2 ventanas centrales de 1,1 × 2,95 (x = 0, y = ±1,625; 0,15 mm de hueco central, como las 2 ventanas de Infineon) + 8 ventanas de 0,6 × 0,4 en los huecos entre filas de vías (x = ±0,95; y = ±0,6 y ±1,8) | repartida como en las `*_ThermalVias` oficiales (varias aperturas entre vías) |
| Cobertura de pasta | 6,49 + 1,92 = **8,41 mm² = 49,6 % del EP** (16,96 mm²); antes 14,5 mm² (85 %, 2 ventanas de 2,45 × 2,95) | caen del 85 % al 49,6 % por las vías |
| Pasta frente a taladros | ≥ 0,1 mm desde el borde de cualquier anillo (central: borde en x = ±0,55 frente a anillo desde ±0,65; ventanas pequeñas: 0,1 mm en y) | ninguna apertura cubre un taladro ni un anillo |
| Ventana mínima | 0,4 mm (relación de área ≈ 1,0 con stencil de 0,12 mm, > 0,66) | imprimible |
| Máscara | pad 15 de F.Cu con apertura de máscara (como antes); las vías en `*.Cu` **sin capas de máscara**: tapadas en B.Cu (la soldadura no baja por el taladro), y abiertas en F.Cu por la apertura del pad | JLCPCB tapa vías sin apertura; es el criterio de las huellas oficiales |
| Cobre inferior | pad 15 también en B.Cu (2,65 × 6,4 mm, sin máscara) con `zone_connect 2` (sólido) en el pad y en las vías | como la oficial `HSOP-8-1EP…_ThermalVias`. El polígono BUS_24V (≥ 300 mm²) lo pone el layout: el pad B.Cu y las vías ya cuelgan de la red VS. **Con alivio térmico por defecto de la zona, las vías quedarían casi aisladas: de ahí `zone_connect 2`** |
| Red | todo «15» = VS = BUS_24V, no GND | `salidas.md` §11 |

Sin pad `custom` (no aplica la comprobación de envolvente).

### Compra (DEC-0007)

- **Ninguna principal sin stock para 10 placas.** Margen mínimo: BTT6050 60 de 1 628 (3,7 %); el resto > 99,9 % libre.
- **Sin equivalente Basic** con mismo valor, tensión, tolerancia y encapsulado para las Extended de §9: C513710 (220 nF 100 V X7R 0805: ninguna Basic en la API; 5 candidatas Extended, ninguna más barata con stock > 30 k), C381466 (4,7 µF 100 V X7R 1210: igual), C8465 (borne THT), C534868 (BTT). **No se aplica ningún cambio de compra.**
- Código de la alternativa de R57–R62 (Yageo RC0805FR-0747KL): **C126351** (Extended, 247 491).

### Observaciones para el coordinador

- **Stock del BTT6050 en descenso:** 1 698 (2026-11-05) → 1 658 (`salidas.md`) → 1 628 (2026-11-10). Sigue cubriendo 10 placas; recomprobar antes de pedir.
- **M7:** el PDF es del fabricante (microdiode.com, Rev. 2025A5); no se ha localizado una URL estable, por eso la ficha enlaza la copia de LCSC. La huella oficial `D_SMA` tiene un hueco de 1,5 mm entre pads frente a los 2,41 mm del patrón del fabricante (p. 3): irrelevante a ≤ 36,7 V y sin montar.
- **Atributos para dejar D12–D17 fuera de BOM y CPL manteniendo la huella (DEC-0008):** símbolo: `dnp yes` («Do not populate») + `in_bom no` («Exclude from bill of materials»), `on_board yes`; huella: `dnp`, `exclude_from_bom`, `exclude_from_pos_files`. Exportar con `kicad-cli sch export bom --exclude-dnp` y `kicad-cli pcb export pos --exclude-dnp` (ambas opciones existen en 10.0.x).
- **Render y máscara:** el trazador 3D de KiCad no modela el tapado de las vías (en `_bottom.png` los taladros se ven abiertos); la máscara solo se comprueba en los Gerber de la fase 5.
- **LED:** el 3D oficial del LED 0603 no lleva marca de polaridad; la polaridad la dan el símbolo/huella (pad 1 = K a la izquierda) y la serigrafía de la huella. Revisar el giro del CPL de JLCPCB (`KT-0603R.md`).
- **Hallazgo previo:** `salidas.md` §8 dice que la ficha del borne cita `conectores.kicad_sch`: corregida en `WJ500V-5.08-2P.md`.

## Verificación

- `verificar.py`: **no aplica** (ningún proyecto KiCad tocado; `hardware/v2` sin cambios; MCP no usado).
- `git diff` de la huella: solo `descr`, el pad 15 (F.Cu con `property pad_prop_heatsink` + `zone_connect 2`), el pad 15 de B.Cu, las 10 vías y las 10 ventanas de pasta; los pads 1–14, el contorno Fab, la serigrafía, el patio y el modelo 3D, idénticos.
- `kicad-cli pcb render` sobre una placa de prueba con las 10 huellas: carga sin errores (top y bottom).
- Pines del símbolo frente a la Tabla 2, p. 4 (script sobre el `.kicad_sym`): ver «Mapeo».

### Tipo y stock (JLCPCB, consulta 2026-11-10)

`componentLibraryType`: `base` = Basic, `expand` = Extended.

| Ref. | LCSC | MPN | Tipo | Stock | Precio 1.er tramo (USD) | Stock 10 placas |
|---|---|---|---|---|---|---|
| U7–U12 | C534868 | BTT6050-1ERA | Extended | **1 628** | 1,2763 (1–9) · 1,0947 (30–99) | 60 ✔ |
| U7–U12 alt. | C534865 | BTT6030-2ERA | Extended | 10 571 | 2,978 (1–9) · 2,204 (30–99) | 30 ✔ (otro pinout) |
| J4–J9 (y J1) | C8465 | WJ500V-5.08-2P | Extended | 312 788 | 0,1345 (1–49) · 0,1084 (50–149) | 70 ✔ |
| R26–R31, R38–R43 | C25804 | 0603WAF1002T5E | **Basic** | 45 615 021 | 0,0022 (1–999) | ✔ |
| R26–R31, R38–R43 alt. | C98220 | RC0603FR-0710KL | Extended | 11 662 729 | 0,0023 | ✔ |
| R32–R37, R44 | C25803 | 0603WAF1003T5E | **Basic** | 15 637 396 | 0,0029 | ✔ |
| R32–R37, R44 alt. | C14675 | RC0603FR-07100KL | Extended | 11 198 225 | 0,0021 | ✔ |
| R45–R50 | C17902 | 1206W4F1002T5E | **Basic** | 2 010 882 | 0,0078 | ✔ |
| R45–R50 alt. | C132649 | RC1206FR-0710KL | Extended | 3 354 720 | 0,0088 (1–499) | ✔ |
| R51–R56 | C23253 | 0603WAF8200T5E | **Basic** | 828 486 | 0,0015 | ✔ |
| R51–R56 alt. | C114638 | RC0603FR-07820RL | Extended | 149 349 | 0,0054 | ✔ |
| R57–R62 | C17713 | 0805W8F4702T5E | **Basic** | 1 147 110 | 0,0068 | ✔ |
| R57–R62 alt. | **C126351** | RC0805FR-0747KL | Extended | 247 491 | 0,0044 | ✔ |
| R63–R68 | C21190 | 0603WAF1001T5E | **Basic** | 25 467 971 | 0,0017 | ✔ |
| R63–R68 alt. | C22548 | RC0603FR-071KL | Extended | 13 847 347 | 0,0036 | ✔ |
| C27–C38 | C513710 | CC0805KKX7R0BB224 | Extended | **30 059** | 0,0226 (1–199) · 0,018 (200–599) | 140 (con C3 y C8) ✔ |
| C27–C38 alt. | C307542 | CL21B224KCFSFNE | Extended | 29 963 | 0,0709 (1–99) | ✔ |
| C39–C44 | C14663 | CC0603KRX7R9BB104 | **Basic** | 36 614 980 | 0,0069 | ✔ |
| C39–C44 alt. | C1591 | CL10B104KB8NNNC | Extended | 2 626 578 | 0,0073 | ✔ |
| C45, C46 | C381466 | FS32X475K101EGG | Extended | 39 784 | 0,2344 (1–49) · 0,1864 (50–149) | 60 (con alimentación) ✔ |
| C45, C46 alt. | C7471274 | 1210B475K101CT (Walsin) | Extended | 2 804 | 0,4091 (1–49) | ✔ (sin PDF en la API) |
| D6–D11 (y D4) | C2286 | KT-0603R | **Basic** | 6 273 838 | 0,0077 (1–999) | ✔ |
| D6–D11 alt. | C2289 | KT-0603YG | Extended | 35 932 | 0,0106 (1–499) | ✔ |
| D12–D17 (DNP) | C95872 | M7 | **Basic** | 5 407 651 | 0,0103 (1–999) | 0 (DNP; 60 si se montan) ✔ |

Extended en el bloque: C534868, C8465 (ya en alimentación), C513710 y C381466 (ya existentes). Línea Extended nueva: solo C534868. Basic nuevas: C17902, C17713, C23253 (+ C25803, C25804, C21190, C14663, C2286 ya existentes).

### Mapeo pin ↔ pad

| Pieza | Símbolo ↔ huella | Resultado |
|---|---|---|
| U7–U12 | `esp-riego:BTT6050-1ERA` ↔ `Infineon_PG-TDSO-14_…_EP2.65x6.4mm` | Pines: 3 GND (power_in), 4 IN (input), 5 DEN (input), 6 IS (output), 10–12 OUT (power_out, apilados en (15,24; 0), 11 y 12 ocultos), 15 VS (power_in), 1, 2, 7, 8, 9, 13, 14 NC (no_connect, apilados). **15/15 coinciden con la Tabla 2, p. 4** (nombre, número y función); 15 números ↔ pads 1–14 + 15 (el EP y las vías llevan «15»). Los ocultos son power_out/no_connect, no power_in: KiCad no los conecta por nombre a una red global |
| J1, J4–J9 | `Connector:Screw_Terminal_01x02` ↔ `esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P…` | Pin_1 → pad 1 (cuadrado, OUT_n), Pin_2 → pad 2 (GND). Render inferior: pad 1 cuadrado a la derecha (vista espejo) con la patilla del 3D en su taladro |
| R26–R68 | `Device:R` ↔ `R_0603`/`R_0805`/`R_1206` | pines 1, 2 ↔ pads 1, 2 (sin polaridad) |
| C27–C46 | `Device:C` ↔ `C_0603`/`C_0805`/`C_1210` | pines 1, 2 ↔ pads 1, 2 |
| D6–D11 | `Device:LED` ↔ `LED_0603_1608Metric` | pin 1 = K ↔ pad 1 (x = −0,7875), pin 2 = A ↔ pad 2. **KT-0603R: ② del datasheet = cátodo = pad 1** (`KT-0603R.md`, p. 2) |
| D12–D17 | `Device:D` ↔ `D_SMA` | pin 1 = K ↔ pad 1 (x = −2,0), pin 2 = A ↔ pad 2. **Cátodo (banda) del M7 = pad 1**: la banda del 3D oficial queda en el lado del pad 1 (`render_SPEC-0024_led_m7.png`) |

### Confirmación de 3D (FAB-11)

| Huella | Modelo | Existe |
|---|---|---|
| BTT6050 (propia) | `${KIPRJMOD}/../libraries/3d/Infineon_PG-TDSO-14.step` | ✔ (hardware/libraries/3d/) |
| Borne (propia) | `${KIPRJMOD}/../libraries/3d/TerminalBlock_Kangnex_WJ500V-5.08-2P.step` | ✔ |
| R_0603 / R_0805 / R_1206 | `${KICAD10_3DMODEL_DIR}/Resistor_SMD.3dshapes/R_…Metric.step` | ✔ (listados en `…/3dmodels`) |
| C_0603 / C_0805 / C_1210 | `…/Capacitor_SMD.3dshapes/C_…Metric.step` | ✔ |
| LED_0603_1608Metric | `…/LED_SMD.3dshapes/LED_0603_1608Metric.step` | ✔ |
| D_SMA | `…/Diode_SMD.3dshapes/D_SMA.step` | ✔ |

El render muestra los 10 modelos sobre sus pads. Pin 1 del BTT: marca del 3D (hendidura) y triángulo de serigrafía junto al pad 1 (arriba a la izquierda), vías del EP visibles desde abajo (2 × 5). Pin 1 del borne: pad cuadrado con su patilla. Cátodo del D_SMA: banda en el lado del pad 1. Cátodo del LED: sin marca en el 3D (ver arriba).

### Tabla de campos por referencia (para SPEC-0025)

`Value` con la notación de `alimentacion.kicad_sch` para las piezas compartidas con ella (`220n 100V`, `4.7u 100V`, `100n`, `10k`, `100k`, `1k`, `Rojo` como D4) y la de `mcu.kicad_sch` para el resto (valores sin unidad: `820`, `47k`). `Fabricante` y `MPN` según la API de JLCPCB. `Datasheet`: URL del fabricante o, si no la hay, `dataManualUrl` de LCSC (API, 2026-11-10). 87 referencias: 6 + 6 + 43 + 20 + 12.

| Refs. | Value | Footprint | LCSC Part# | MPN | Fabricante | Datasheet | Description | DNP |
|---|---|---|---|---|---|---|---|---|
| U7–U12 (6) | BTT6050-1ERA | esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm | C534868 | BTT6050-1ERA | Infineon Technologies | https://www.infineon.com/assets/row/public/documents/10/49/infineon-btt6050-1era-datasheet-en.pdf | High-side 24 V 50 mΩ con medida de corriente: canal n | no |
| J4–J9 (6) | WJ500V-5.08-2P | esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal | C8465 | WJ500V-5.08-2P | Ningbo Kangnex Elec | https://www.lcsc.com/datasheet/lcsc_datasheet_1912251636_Ningbo-Kangnex-Elec-WJ500V-5-08-2P_C8465.pdf | Borne de tornillo 2P 5,08 mm 15 A: salida n (polo 1 = OUT_n, polo 2 = GND) | no |
| R26–R31 (6) | 10k | Resistor_SMD:R_0603_1608Metric | C25804 | 0603WAF1002T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010045_UNI-ROYAL-Uniroyal-Elec-0603WAF1002T5E_C25804.pdf | Resistencia 10 kΩ 1 % 0603: R_IN de IN_n | no |
| R32–R37 (6) | 100k | Resistor_SMD:R_0603_1608Metric | C25803 | 0603WAF1003T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010045_UNI-ROYAL-Uniroyal-Elec-0603WAF1003T5E_C25803.pdf | Resistencia 100 kΩ 1 % 0603: pull-down de IN_n | no |
| R38–R43 (6) | 10k | Resistor_SMD:R_0603_1608Metric | C25804 | 0603WAF1002T5E | UNI-ROYAL | (igual que R26) | Resistencia 10 kΩ 1 % 0603: R_DEN del canal n | no |
| R44 (1) | 100k | Resistor_SMD:R_0603_1608Metric | C25803 | 0603WAF1003T5E | UNI-ROYAL | (igual que R32) | Resistencia 100 kΩ 1 % 0603: pull-down de OUT_DEN | no |
| R45–R50 (6) | 10k | Resistor_SMD:R_1206_3216Metric | C17902 | 1206W4F1002T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010145_UNI-ROYAL-Uniroyal-Elec-1206W4F1002T5E_C17902.pdf | Resistencia 10 kΩ 1 % 0,25 W 200 V 1206: R_SENSE de IS_HS n | no |
| R51–R56 (6) | 820 | Resistor_SMD:R_0603_1608Metric | C23253 | 0603WAF8200T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010100_UNI-ROYAL-Uniroyal-Elec-0603WAF8200T5E_C23253.pdf | Resistencia 820 Ω 1 % 0603: R_IS del canal n | no |
| R57–R62 (6) | 47k | Resistor_SMD:R_0805_2012Metric | C17713 | 0805W8F4702T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010200_UNI-ROYAL-Uniroyal-Elec-0805W8F4702T5E_C17713.pdf | Resistencia 47 kΩ 1 % 0,125 W 150 V 0805: R_OL del canal n | no |
| R63–R68 (6) | 1k | Resistor_SMD:R_0603_1608Metric | C21190 | 0603WAF1001T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010130_UNI-ROYAL-Uniroyal-Elec-0603WAF1001T5E_C21190.pdf | Resistencia 1 kΩ 1 % 0603: R_LED del canal n (≈ 1,5 mA) | no |
| C27–C32 (6) | 220n 100V | Capacitor_SMD:C_0805_2012Metric | C513710 | CC0805KKX7R0BB224 | YAGEO | https://www.lcsc.com/datasheet/lcsc_datasheet_2004231434_YAGEO-CC0805KKX7R0BB224_C513710.pdf | MLCC 220 nF 100 V X7R 0805: C_VS del canal n | no |
| C33–C38 (6) | 220n 100V | Capacitor_SMD:C_0805_2012Metric | C513710 | CC0805KKX7R0BB224 | YAGEO | (igual que C27) | MLCC 220 nF 100 V X7R 0805: C_OUT del canal n | no |
| C39–C44 (6) | 100n | Capacitor_SMD:C_0603_1608Metric | C14663 | CC0603KRX7R9BB104 | YAGEO | https://www.lcsc.com/datasheet/lcsc_datasheet_2211101700_YAGEO-CC0603KRX7R9BB104_C14663.pdf | MLCC 100 nF 50 V X7R 0603: C_IS del canal n | no |
| C45, C46 (2) | 4.7u 100V | Capacitor_SMD:C_1210_3225Metric | C381466 | FS32X475K101EGG | PSA (Prosperity Dielectrics) | https://wmsc.lcsc.com/wmsc/upload/file/pdf/v2/lcsc/2304140030_PSA-Prosperity-Dielectrics-FS32X475K101EGG_C381466.pdf | MLCC 4,7 µF 100 V X7R 1210: BUS_24V a granel (C45 arriba, C46 abajo) | no |
| D6–D11 (6) | Rojo | LED_SMD:LED_0603_1608Metric | C2286 | KT-0603R | Hubei KENTO Elec | https://www.lcsc.com/datasheet/lcsc_datasheet_1810231112_Hubei-KENTO-Elec-KT-0603R_C2286.pdf | LED rojo 0603: canal n (en IN_n) | no |
| D12–D17 (6) | M7 | Diode_SMD:D_SMA | C95872 | M7 | MDD (Microdiode Semiconductor) | https://www.lcsc.com/datasheet/lcsc_datasheet_2407101107_MDD-Microdiode-Semiconductor-M7_C95872.pdf | Rectificador 1 kV 1 A SMA: rueda libre del canal n (K = OUT_n, A = GND), DNP (DEC-0008) | **sí** (fuera de BOM y CPL; huella en la placa) |

Símbolos: `esp-riego:BTT6050-1ERA`, `Connector:Screw_Terminal_01x02`, `Device:R`, `Device:C`, `Device:LED`, `Device:D`. Las huellas oficiales las resuelve la tabla global de KiCad (la de la v2 solo lista `esp-riego`). La numeración de canal sigue el orden de §9: Uk ↔ Jk ↔ canal (U7 = canal 1 … U12 = canal 6); la correspondencia R26 = canal 1, … la fija SPEC-0025. En D4 de alimentación, `Value` = `Rojo`; si SPEC-0025 prefiere `LED`, es una elección de ing-esquematicos.

### Cambios propuestos a `docs/diseno/salidas.md` (para SPEC-0025; texto exacto)

1. **l. 434 (Anexo A, fila KT-0603R)**, sustituir por:
   `| KT-0603R | D4 y D6–D11. Ficha propia `KT-0603R.md` (SPEC-0024). Polaridad: ② del datasheet = cátodo = pad 1 (K) de `LED_0603_1608Metric` | C2286 | `datasheets/KT-0603R.pdf` (PDF de LCSC, C2286) | Cátodo = pad 1 (K), ánodo = pad 2 (A) | `Device:LED` / `LED_0603_1608Metric` |`
2. **l. 435 (Anexo A, fila M7)**, sustituir por:
   `| M7 (DNP) | D12–D17, DNP por DEC-0008 (solo se montan si se aprueba, §5). Ficha `M7.md` (SPEC-0024) | C95872 | `datasheets/M7.pdf` (MDD, Rev. 2025A5) | K (banda) = pad 1, A = pad 2 | `Device:D` / `Diode_SMD:D_SMA` |`
3. **l. 432 (Anexo A, BTT6050)**, añadir al final de la 2.ª columna: « Ficha revisada en SPEC-0024 (errata de P_7.5.2, vías del EP, stock del 2026-11-10).» y en la **l. 433 (WJ500V)**: « Ficha corregida en SPEC-0024.»
4. **l. 298 (§8, último punto)**, sustituir la frase «**La ficha dice «Uso: `conectores.kicad_sch`»: los bornes de salida van en `salidas.kicad_sch`** (propuesta de cambio en el log).» por «La ficha `WJ500V-5.08-2P.md` (corregida en SPEC-0024) da el uso: J1 en `alimentacion.kicad_sch` y J4–J9 en `salidas.kicad_sch`.»
5. **§9 (l. 306–321), stock y tipo con fecha 2026-11-10** (cambiar en la columna «LCSC · tipo · stock JLCPCB»; añadir «(2026-11-10)» a la cabecera):
   - U7–U12: `C534868 · Extended · 1 628`; alternativa: `BTT6030-2ERA (C534865 · 10 571; otro *routing*, §10)`.
   - J4–J9: `C8465 · Extended (THT) · 312 788`.
   - R26–R31 y R38–R43: `C25804 · Basic · 45,6 M`; R32–R37 y R44: `C25803 · Basic · 15,6 M`; R45–R50: `C17902 · Basic · 2,01 M`; R51–R56: `C23253 · Basic · 828 486`; R57–R62: `C17713 · Basic · 1,15 M`; R63–R68: `C21190 · Basic · 25,5 M`.
   - **R57–R62, alternativa:** `Yageo RC0805FR-0747KL (C126351 · Extended · 247 491)` (sustituye a «(jr-conformidad)»).
   - C27–C38: `C513710 · Extended · 30 059`; C39–C44: `C14663 · Basic · 36,6 M`; C45, C46: `C381466 · Extended · 39 784`; D6–D11: `C2286 · Basic · 6,27 M`; D12–D17: `C95872 · Basic · 5,41 M`.
   - Alternativas (stock del 2026-11-10): C98220 11,7 M; C14675 11,2 M; C132649 3,35 M; C114638 149 349; C22548 13,8 M; C307542 29 963; C1591 2,63 M; C7471274 2 804; C2289 35 932.
6. **l. 325 (§9, «Stock para 10 placas»)**, sustituir por: «**Stock para 10 placas (2026-11-10):** BTT6050 60 de 1 628 ✔ (margen limitado; segunda fuente en §10). C513710: 14 por placa (con C3 y C8), 140 de 30 059 ✔. C381466: 6 por placa (con alimentación), 60 de 39 784 ✔. C8465: 7 por placa, 70 de 312 788 ✔.»
7. **l. 30 y l. 405 (§0 y §13.5)**: `1 658` → `1 628` (las dos veces).
8. **l. 326 (§9, «Piezas nuevas»)**, sustituir por: «**Piezas nuevas:** ningún símbolo ni huella nuevos; la huella `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` pasa a llevar 10 vías de 0,3 / 0,6 mm en el EP (SPEC-0024, FAB-02). Fichas en Anexo A.»
9. **l. 321 (§9, fila D12–D17)**, sustituir « (campo DNP; fuera de BOM y CPL mientras no haya DEC)» por « (DNP: `dnp yes` + `in_bom no` en el símbolo, `dnp` + `exclude_from_bom` + `exclude_from_pos_files` en la huella; se exporta con `--exclude-dnp`; huella en la placa)».
10. **§11, l. 347 (fila «BUS_24V en cada BTT»)**, sustituir « Vías térmicas en el EP de **0,3 / 0,6 mm** (FAB-02) a un polígono BUS_24V en la cara inferior (≥ 8 por *tab*)» por « Vías térmicas en el EP de **0,3 / 0,6 mm** (FAB-02), **ya en la huella** (10 por *tab*, pad 15, con pad en B.Cu y conexión sólida), a un polígono BUS_24V en la cara inferior que pone el layout». Añadir al final de la columna Notas: « Pasta del EP al 49,6 % (vías en la huella; ver `BTT6050-1ERA.md`).»

## Requiere verificación de validación

| Pieza | Qué | Datasheet y página |
|---|---|---|
| `esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm` | **Modificada:** 10 vías 0,3 / 0,6 mm numeradas 15 (x = ±0,95; y = −2,4…2,4 cada 1,2), pad 15 en B.Cu, `zone_connect 2`, 10 ventanas de pasta (49,6 %), `descr`. Pads 1–14, EP, serigrafía, patio y 3D sin cambios | BTT6050-1ERA Rev. 1.00: Fig. 53, p. 49 (cotas del EP y cuerpo); nota 2 de Tabla 3 y Fig. 4, pp. 9-10 (vías térmicas sin cotas); https://www.infineon.com/package/PG-TDSO-14-11 (land pattern); https://jlcpcb.com/capabilities/Capabilities |
| `Infineon_PG-TDSO-14.step` | Sin cambios; render de comprobación | Fig. 53, p. 49 |
| `esp-riego:BTT6050-1ERA` (símbolo) | Sin cambios; 15 pines comprobados frente a la Tabla 2, p. 4 | BTT6050-1ERA, Tabla 2, p. 4 |
| `M7.md` + `datasheets/M7.pdf` | Ficha nueva: cotas del SMA frente a `D_SMA`, polaridad = pad 1 | M7.pdf pp. 1 y 3 («Suggested Pad Layout») |
| `BTT6050-1ERA.md` | Errata de P_7.5.2 como lectura propia; sin R_GND ni zéner en VS (decisión de `salidas.md` §4.4) | BTT6050-1ERA, p. 30 (P_7.5.2), p. 48 (Tabla 11), pp. 4 y 22 |
| `WJ500V-5.08-2P.md`, `BTT6030-2ERA.md`, `KT-0603R.md` | Uso, stock y fecha; sin cambios en assets | `WJ500V-5.08-2P.pdf` (hoja única); BTT6030-2ERA Tabla 2, p. 4 |

### Repaso de `gestion/checklists/librerias.md` v3

**Origen**
- Orden de preferencia y origen anotado en fichas: cumple (BTT/borne creados, anotado; M7 y pasivos oficiales).
- Formato nativo: cumple. JSON de EasyEDA / `kicad-cli upgrade` / fidelidad por conversión independiente: no aplica.
- Sustitución con `git diff`: cumple (el archivo cambia; diff acotado, ver Verificación).
- Tablas `${KIPRJMOD}`: cumple, sin cambios (no se tocó `hardware/v2`). Tablas sin restos: sin cambios.
- *Land pattern* del fabricante antes de derivar: cumple (el de Infineon ya usado; la página no da vías; se justifica el patrón de vías).

**Símbolo**
- Pines y nombres frente al datasheet: BTT6050 comprobado (15/15, Tabla 2, p. 4); pasivos, LED, D y borne oficiales (pines 1/2, K/A).
- Tipos eléctricos: BTT correctos (IN/DEN input, IS output, GND/VS power_in, OUT power_out apilados, NC no_connect); oficiales sin cambios.
- Campos: tabla preparada para SPEC-0025 (no edito hojas); campos de librería del BTT presentes (Value, Footprint, Datasheet, Description, LCSC Part#, MPN).

**Huella (modificada: BTT)**
- Tabla de cotas: cumple (vías y pasta arriba; pads sin cambios, en «Requiere verificación»).
- Pin 1 en serigrafía y Fab: cumple, sin cambios (triángulo F.SilkS y F.Fab).
- Courtyard con margen: sin cambios. Serigrafía fuera de pads: sin cambios.
- Render con pin 1 del 3D sobre el pad 1: cumple (`render_SPEC-0024_top.png`).
- Conectores THT, patilla desde el corte, cara de entrada del cable en Fab: borne sin cambios; pin 1 y patillas comprobados en `_bottom.png`.
- Taladro frente a diagonal: borne sin cambios (ficha); vías 0,3 mm no llevan patilla.
- 3D presente y en `.step`: cumple (tabla arriba).
- Pads `custom`: no aplica.
- Extensiones 3D en `.gitattributes`: sin cambios (`*.step`, `*.STEP`); PNG de render nuevos.

**Mapeo símbolo ↔ huella**: cumple (tabla arriba).

**Ficha**: cumple (LCSC, tipo, fecha 2026-11-10, datos). Datasheet del fabricante: BTT, M7 (MDD, vía copia de LCSC por falta de URL estable) y borne (solo LCSC: Kangnex no responde). LCSC/JLCPCB encuentra todas las piezas; no hay «solo montaje».

## Pendiente

- **ing-validacion:** revisar la huella del BTT6050 (vías, pasta, B.Cu, `zone_connect 2`), la ficha M7 y las revisiones de fichas.
- **SPEC-0025 (ing-esquematicos):** aplicar los campos de la tabla; DNP en D12–D17 con los atributos indicados; los 10 cambios propuestos a `salidas.md`.
- **Coordinador:** decidir si el stock decreciente del BTT6050 (1 628) exige reservar pedido o segunda fuente antes de la fase 5.
- **Layout:** el polígono BUS_24V de ≥ 300 mm² bajo cada BTT; con el pad B.Cu de 2,65 × 6,4 ya en la huella, el hueco a otras redes en la cara inferior se rige por `Power_In` (≥ 0,6 mm).

## Notas para el siguiente agente

- La huella del BTT es compartida con el BTT6030-2ERA (distinto pinout): las vías son VS en ambos.
- Los PNG de render van a `hardware/libraries/3d/fuentes-solidcraft/`; la placa de prueba estaba en el *scratchpad* (no queda carpeta temporal en el repositorio).
- La API de JLCPCB sirve el stock real (LCSC no): `selectSmtComponentList` con el código en `keyword`.
