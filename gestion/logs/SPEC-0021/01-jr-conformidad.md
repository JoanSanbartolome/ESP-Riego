---
spec: SPEC-0021
agente: jr-conformidad
n: 01
fecha: 2026-11-06
estado: completado
---

# SPEC-0021 · 01 · jr-conformidad

## Orden recibida

SPEC-0021 · rama spec/SPEC-0021-piezas-mcu · todo el alcance de la spec (3D del TS-1187A con render del pin 1; huella `esp-riego:ESP32-S3-WROOM-1` con las 12 vías a 0,3/0,6 mm; fichas TS-1187A-B-A-B, KT-0603YG, B-2100S04P-A110 y ESP32-S3-WROOM-1 con N8; tipo y stock con fecha de todas las piezas de §11, incluida C14663; tabla de campos para SPEC-0022).

## Contexto consultado

- `gestion/specs/SPEC-0021-piezas-mcu.md`, `docs/diseno/mcu.md` (§0, §2, §3, §5.1, §11, §12, Anexo A), `gestion/checklists/librerias.md` v3 y `esquema.md` v6 (punto FAB-02), DEC-0007, `docs/02` (FAB-02, FAB-11, KIC-01).
- Oficiales de KiCad 10.0.6: `RF_Module.pretty/ESP32-S3-WROOM-1`, `Button_Switch_SMD.pretty/SW_Push_1P1T_XKB_TS-1187A`, `Connector_USB.pretty/USB_C_Receptacle_HRO_TYPE-C-31-M-12`, símbolos `RF_Module`, `Switch`, `Connector`, `Power_Protection`, `Connector_Generic`, `Device`.
- PDF de LCSC/JLCPCB descargados a `hardware/componentes/datasheets/`: `TS-1187A-B-A-B.pdf`, `KT-0603YG.pdf`, `B-2100S04P-A110.pdf`. WROOM-1 v1.8 ya estaba.
- API de JLCPCB `selectSmtComponentList` (2026-11-06) para stock y tipo. Samsung SimSurfing `CL10A105KB8NNN` (curvas).

## Acciones

1. **3D del TS-1187A:** `hardware/libraries/3d/SW_Push_1P1T_XKB_TS-1187A.step` (SolidCraft; fuente `fuentes-solidcraft/gen_ts1187a.py` y `ts1187a.json`). 6 cuerpos, 55 caras `ADVANCED_FACE`, Y hacia arriba, offset 0.
2. **Huella del pulsador:** `esp-riego.pretty/SW_Push_1P1T_XKB_TS-1187A.kicad_mod` = oficial + ruta `${KIPRJMOD}/../libraries/3d/…` (`diff` frente a la oficial: solo `generator`, `descr` y la línea del modelo).
3. **Huella del módulo:** `esp-riego.pretty/ESP32-S3-WROOM-1.kicad_mod` = oficial con `drill 0.2 → 0.3` en las 12 vías del EPAD (`diff`: solo `generator`, `descr` y esas 12 líneas). Se conservan las 12 vías, el *keepout* (zona de 21 × 48 mm, todas las capas Cu, sin pistas/vías/pads/relleno/huellas), los pads y el 3D oficial `${KICAD10_3DMODEL_DIR}/RF_Module.3dshapes/ESP32-S3-WROOM-1.step` (existe).
4. **Huella del USB-C (extra, para FAB-11):** `esp-riego.pretty/USB_C_Receptacle_HRO_TYPE-C-31-M-12.kicad_mod` = oficial con el 3D de respaldo `${KIPRJMOD}/../libraries/3d/USB_C_Receptacle_HRO_TYPE-C-31-M-12.step` (la oficial apunta a un `.step` que KiCad 10.0.6 no instala).
5. **Render** en placa de prueba del scratchpad (fuera de `hardware/v2`): `kicad-cli pcb render --side top` → `hardware/libraries/3d/fuentes-solidcraft/render_SPEC-0021_top.png`. Los tres modelos cargan y quedan sobre sus pads; en los pulsadores, terminales sobre los 4 pads y marca roja del pin 1 en la esquina superior izquierda (pad 1 = (−3; −1,875) de la huella).
6. **Fichas:** nuevas `TS-1187A-B-A-B.md`, `KT-0603YG.md`, `B-2100S04P-A110.md`; actualizadas `ESP32-S3-WROOM-1.md` (N8, antena, R8/R16V, huella propia, stock) y `TYPE-C-31-M-12.md` (huella y 3D).
7. **Stock/tipo:** API de JLCPCB, 2026-11-06 (tabla más abajo).
8. **Pines símbolo ↔ pads** (script sobre los `.kicad_sym` y `.kicad_mod`): WROOM 41/41, SW_Push 2 pines ↔ pads 1,1,2,2, USB-C 17/17, USBLC6 6/6, Conn_01x04 4/4, LED 2/2, sin faltas ni sobras.

## Decisiones y justificación

- **Vías del EPAD: 0,3/0,6, no «sin vías».** Mantiene las 12 vías térmicas del fabricante (§12 pide ≥ 9) y el *keepout*; anillo 0,15 mm. Cumple FAB-02. Máscara tal como la oficial (`F.Mask` abierta, trasera tapada).
- **TS-1187A-B-A-B ya es Basic** (mcu.md no lo decía): sin cargo por pieza Extended.
- **C14663 confirmado en JLCPCB:** Basic, stock 34 715 136 (LCSC 0 no aplica a JLCPCB). Se mantiene.
- **Ninguna principal sin stock:** no se aplica DEC-0007 de oficio.
- **Propuestas DEC-0007 (las decide el coordinador; la tabla de campos usa las principales de `mcu.md`):**
  1. **C23 (EN, 1 µF): C106248 (Extended) → C15849 Samsung CL10A105KB8NNNC (Basic, 13,07 M, 0,0108 $).** Curvas Samsung: −18,4 % a 3,3 V DC, −1,6 % a 60 °C (`mcu.md` §5.1 supone −15 % y −3 %). τ mín. 7,35 → ≈ 7,16 ms; EN/VDD del caso peor 0,155 → ≈ 0,159 < 0,25: sigue cumpliendo. Ahorra una referencia Extended. Requiere que validación acepte el recálculo.
  2. **U6: ST C7519 (28 729 · 0,1624 $) → UMW C2687116 (95 519 · 0,0479 $)**, ambas Extended, misma huella SOT-23-6; abarata, pero la equivalencia eléctrica del clon (capacidad, V_BR) no está comprobada: solo con datasheet del UMW revisado.
  3. **D5 a Basic:** solo existe en rojo (KT-0603R, C2286, Basic, 6,66 M) o blanco; cambia el color, no se aplica sin decisión.
  - Las demás Extended (módulo, J2, J3) no tienen alternativa Basic: J3 y C2337/C492403 son todas Extended.
- **C318887 (alternativa del pulsador) mide H = 2,5 mm y 260 gf**, no «misma altura»: 1 mm más alto que la principal (revisar con la caja, FAB-11).
- **Datasheet del KT-0603YG:** el PDF de LCSC está rotulado XL-0603QYGC (otro fabricante). No se ha localizado el de KENTO; se enlaza como referencia, mismos rangos V_F/λ.

## Verificación

- `verificar.py`: no aplica (no se ha tocado ningún proyecto KiCad; `hardware/v2` sin cambios, `.kicad_pro` no reescrito). MCP no usado.
- `git status`: solo archivos nuevos de `hardware/` y la modificación de las fichas, más `auditoria/*.jsonl` (hook).
- `diff` de las 3 huellas frente a las oficiales (CRLF normalizado): ver Acciones 2-4.
- Render del banco: `render_SPEC-0021_top.png`.

### Stock y tipo (JLCPCB, consulta 2026-11-06)

| Ref. | LCSC | MPN | Tipo | Stock | Precio 1.er tramo (USD) |
|---|---|---|---|---|---|
| U5 | C2913198 | ESP32-S3-WROOM-1-N8 | Extended | 2 776 | 4,9259 (1–9) · 4,2482 (10–29) |
| U5 alt. | C2913199 | …-N16 | Extended | 2 297 | 4,9603 · 4,4447 |
| (no válida) | C2913197 | …-N4 | Extended | 4 154 | 4,2629 · 3,8062 |
| C24 | C45783 | CL21A226MAQNNNE | Basic | 3 443 575 | 0,1836 (1–199) |
| C25 y 100 nF | C14663 | CC0603KRX7R9BB104 | **Basic** | 34 715 136 | 0,0101 (1–499) |
| C25 alt. | C1591 | CL10B104KB8NNNC | Extended | 3 371 230 | 0,0071 |
| R16, R17 | C25804 | 0603WAF1002T5E | Basic | 42 706 895 | 0,0024 |
| R16 alt. | C98220 | RC0603FR-0710KL | Extended | 12 303 144 | 0,0027 |
| C23 | C106248 | CC0603KRX7R7BB105 | Extended | 581 082 | 0,0115 |
| C23 (propuesta) | C15849 | CL10A105KB8NNNC | Basic | 13 070 681 | 0,0108 |
| SW1, SW2 | C318884 | TS-1187A-B-A-B | **Basic** | 969 468 | 0,0207 (1–199) |
| SW alt. | C318887 | TS-1187A-C-E-B | Extended | 81 180 | 0,0392 |
| J2 | C165948 | TYPE-C-31-M-12 | Extended | 324 114 | 0,1870 (1–49) |
| J2 alt. | C5337088 | TYPE-C-31-M-12A | Extended | 2 393 | 0,2399 |
| U6 | C7519 | USBLC6-2SC6 (ST) | Extended | 28 729 | 0,1624 (1–49) |
| U6 alt. | C2687116 | USBLC6-2SC6 (UMW) | Extended | 95 519 | 0,0479 (1–99) |
| R18, R19 | C23186 | 0603WAF5101T5E | Basic | 20 424 093 | 0,0015 |
| R20, R21 | C23345 | 0603WAF220JT5E | Basic | 6 050 898 | 0,0017 |
| C26 | C19666 | CL10A475KO8NNNC | Basic | 3 885 262 | 0,0150 (1–99) |
| J3 | C124378 | B-2100S04P-A110 | Extended | 105 049 | 0,0524 (1–99) |
| J3 alt. | C2337 | 2.54-1*40P (BOOMELE) | Extended | 55 818 | 0,1593 |
| R22 | C23179 | 0603WAF4700T5E | Basic | 4 148 312 | 0,0023 |
| D5 | C2289 | KT-0603YG | Extended | 39 870 | 0,0106 (1–499) |
| D5 alt. | C2287 | KT-0603Y | Extended | 92 914 | 0,0106 |
| R23 | C21190 | 0603WAF1001T5E | Basic | 27 504 990 | 0,0017 |
| R24, R25 | C23162 | 0603WAF4701T5E | Basic | 16 074 128 | 0,0028 |
| R_PD (fuera de hoja) | C25803 | 0603WAF1003T5E | Basic | 16 268 275 | 0,0029 |
| Pull-ups EXP (provisional) | C4190 | 0603WAF2201T5E | Basic | 5 130 643 | 0,0018 |

Extended en el bloque: U5, C23, J2, U6, J3, D5 (6 referencias distintas; con la propuesta 1, 5). El cargo de JLCPCB por referencia Extended distinta se confirma en su presupuesto.

### Tabla de campos por referencia (para SPEC-0022)

`Fabricante` y `MPN` según la API de JLCPCB. `Datasheet`: URL del fabricante o, si no la hay, `dataManualUrl` de LCSC (API de JLCPCB, 2026-11-07); corregida por VAL-0021-01-02 (ver log 03). `Footprint` con las propias `esp-riego:`; las oficiales las resuelve la tabla global de KiCad (la tabla de la v2 solo lista `esp-riego`).

| Ref. | Value | Footprint | LCSC Part# | MPN | Fabricante | Datasheet | Description |
|---|---|---|---|---|---|---|---|
| U5 | ESP32-S3-WROOM-1-N8 | esp-riego:ESP32-S3-WROOM-1 | C2913198 | ESP32-S3-WROOM-1-N8 | Espressif Systems | https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf | Módulo Wi-Fi/BLE ESP32-S3, 8 MB flash, antena PCB |
| C24 | 22uF | Capacitor_SMD:C_0805_2012Metric | C45783 | CL21A226MAQNNNE | Samsung Electro-Mechanics | https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Samsung-Electro-Mechanics-CL21A226MAQNNNE_C45783.pdf | 22 µF 25 V X5R 0805 |
| C25 | 100nF | Capacitor_SMD:C_0603_1608Metric | C14663 | CC0603KRX7R9BB104 | YAGEO | https://www.lcsc.com/datasheet/lcsc_datasheet_2211101700_YAGEO-CC0603KRX7R9BB104_C14663.pdf | 100 nF 50 V X7R 0603 |
| R16, R17 | 10k | Resistor_SMD:R_0603_1608Metric | C25804 | 0603WAF1002T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010045_UNI-ROYAL-Uniroyal-Elec-0603WAF1002T5E_C25804.pdf | 10 kΩ 1 % 0603 |
| C23 | 1uF | Capacitor_SMD:C_0603_1608Metric | C106248 (o C15849 si se aprueba) | CC0603KRX7R7BB105 (o CL10A105KB8NNNC) | YAGEO (o Samsung) | https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_YAGEO-CC0603KRX7R7BB105_C106248.pdf (C106248) · https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Samsung-Electro-Mechanics-CL10A105KB8NNNC_C15849.pdf (C15849) | 1 µF 16 V X7R 0603 (o 50 V X5R) |
| SW1, SW2 | SW_Push | esp-riego:SW_Push_1P1T_XKB_TS-1187A | C318884 | TS-1187A-B-A-B | XKB Connection | https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_XKB-Connection-TS-1187A-B-A-B_C318884.pdf | Pulsador SMD 5,1 × 5,1, 160 gf, H 1,5 mm |
| J2 | USB_C_Receptacle_USB2.0_16P | esp-riego:USB_C_Receptacle_HRO_TYPE-C-31-M-12 | C165948 | TYPE-C-31-M-12 | Korean Hroparts Elec (HRO) | https://www.lcsc.com/datasheet/lcsc_datasheet_2205251630_Korean-Hroparts-Elec-TYPE-C-31-M-12_C165948.pdf | Conector USB-C 2.0 16 pines SMT |
| U6 | USBLC6-2SC6 | Package_TO_SOT_SMD:SOT-23-6 | C7519 | USBLC6-2SC6 | STMicroelectronics | https://www.st.com/resource/en/datasheet/usblc6-2.pdf | ESD de 2 líneas USB, SOT-23-6 |
| R18, R19 | 5k1 | Resistor_SMD:R_0603_1608Metric | C23186 | 0603WAF5101T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010116_UNI-ROYAL-Uniroyal-Elec-0603WAF5101T5E_C23186.pdf | 5,1 kΩ 1 % 0603 |
| R20, R21 | 22 | Resistor_SMD:R_0603_1608Metric | C23345 | 0603WAF220JT5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010100_UNI-ROYAL-Uniroyal-Elec-0603WAF220JT5E_C23345.pdf | 22 Ω 1 % 0603 |
| C26 | 4.7uF | Capacitor_SMD:C_0603_1608Metric | C19666 | CL10A475KO8NNNC | Samsung Electro-Mechanics | https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Samsung-Electro-Mechanics-CL10A475KO8NNNC_C19666.pdf | 4,7 µF 16 V X5R 0603 |
| J3 | Conn_01x04 | Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical | C124378 | B-2100S04P-A110 | Ckmtw | https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Ckmtw-Shenzhen-Cankemeng-B-2100S04P-A110_C124378.pdf | Tira 1 × 4 a 2,54 mm, recta THT |
| R22 | 470 | Resistor_SMD:R_0603_1608Metric | C23179 | 0603WAF4700T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010116_UNI-ROYAL-Uniroyal-Elec-0603WAF4700T5E_C23179.pdf | 470 Ω 1 % 0603 |
| D5 | LED | LED_SMD:LED_0603_1608Metric | C2289 | KT-0603YG | Hubei KENTO Elec | https://www.lcsc.com/datasheet/lcsc_datasheet_1806151835_Hubei-KENTO-Elec-KT-0603YG_C2289.pdf | LED verde-amarillo 0603 |
| R23 | 1k | Resistor_SMD:R_0603_1608Metric | C21190 | 0603WAF1001T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010130_UNI-ROYAL-Uniroyal-Elec-0603WAF1001T5E_C21190.pdf | 1 kΩ 1 % 0603 |
| R24, R25 | 4k7 | Resistor_SMD:R_0603_1608Metric | C23162 | 0603WAF4701T5E | UNI-ROYAL | https://www.lcsc.com/datasheet/lcsc_datasheet_2206010116_UNI-ROYAL-Uniroyal-Elec-0603WAF4701T5E_C23162.pdf | 4,7 kΩ 1 % 0603 |

## Requiere verificación de validación

| Pieza | Qué | Datasheet y página |
|---|---|---|
| `hardware/libraries/3d/SW_Push_1P1T_XKB_TS-1187A.step` (+ `fuentes-solidcraft/gen_ts1187a.py`) | 3D creado: cuerpo 5,1, terminales hasta ±3,25, tecla Ø 2,0, H 1,5 (supuestos: tapa a 0,9, grosor de terminal 0,3) | `hardware/componentes/datasheets/TS-1187A-B-A-B.pdf`, hoja única (vista superior y alzado) |
| `esp-riego:SW_Push_1P1T_XKB_TS-1187A` | copia con ruta 3D propia; pads 1,0 × 0,75 a ±3 / ±1,875 = «P.C.B LAYOUT» (7,0/5,0 × 4,5/3,0) | ídem |
| `esp-riego:ESP32-S3-WROOM-1` | 12 vías EPAD 0,2 → 0,3 mm; resto igual a la oficial | WROOM-1 v1.8 §9 p. 41 y land pattern Fig. 11-1 p. 45 (`hardware/componentes/datasheets/ESP32-S3-WROOM-1.pdf`) |
| `esp-riego:USB_C_Receptacle_HRO_TYPE-C-31-M-12` | copia con 3D de respaldo (ya existente) | `hardware/componentes/datasheets/TYPE-C-31-M-12.pdf`, hoja única |
| Huellas oficiales sin cambios del bloque (no modificadas; solo para el mapeo) | LED_0603 vs pads recomendados 0,7 × 0,7 a 1,4 (p. 2 de KT-0603YG.pdf); PinHeader taladro 1,0 vs diagonal 0,93 (holgura 0,07 < 0,1 de la checklist) | `KT-0603YG.pdf` p. 2; `B-2100S04P-A110.pdf` hoja única |

### Repaso de `gestion/checklists/librerias.md` v3

**Origen**
- Orden de preferencia y origen anotado en fichas: cumple (oficial; 3D propio creado, anotado).
- Formato nativo: cumple (`.kicad_mod`, `.step`; nada de EasyEDA).
- JSON de EasyEDA / `kicad-cli upgrade`: no aplica.
- Fidelidad por conversión independiente: no aplica (copias de oficiales con `diff`).
- Sustitución de pieza con `git diff`: no aplica (archivos nuevos).
- Tablas `${KIPRJMOD}`: cumple, sin cambios (`hardware/v2/fp-lib-table` y `sym-lib-table` con `${KIPRJMOD}/../libraries/…`).
- Tablas sin restos: cumple (solo `esp-riego`).
- *Land pattern* del fabricante antes de derivar por IPC: no aplica (no se derivó ninguna huella).

**Símbolo**
- Pines y nombres frente al datasheet: WROOM-1 comprobado por script contra la ficha (Tabla 3-1, pp. 11-12); el resto, solo existencia de pines ↔ pads. Tipos eléctricos: los oficiales, sin cambios.
- Campos: tabla preparada; se aplican en SPEC-0022 (no edito hojas).

**Huella (creadas o modificadas)**
- Tabla de cotas: pulsador y WROOM en «Requiere verificación»; sin pads cambiados.
- Pin 1 en serigrafía y Fab: heredado de las oficiales; el pulsador es simétrico y no lo lleva (el 3D marca el pad 1).
- Courtyard y serigrafía fuera de pads: heredados de las oficiales, sin cambios.
- Render con pin 1 del 3D sobre el pad 1: cumple (pulsador, marca roja arriba izquierda; WROOM y HRO alineados).
- Conectores THT, patilla desde el corte: no aplica (no se creó). Taladro frente a diagonal: pendiente, ver observación del J3 (1,0 frente a 0,93 + 0,1).
- 3D presente y en `.step`: cumple (WROOM y LED/PinHeader/pasivos oficiales existen; pulsador y HRO propios en `${KIPRJMOD}`).
- Pads `custom`: no aplica.
- Extensiones 3D en `.gitattributes`: cumple (`*.step`, `*.STEP`).

**Mapeo símbolo ↔ huella**: cumple (script, sin faltas ni sobras).

**Ficha**: cumple (LCSC, tipo, fecha 2026-11-06, datasheet, datos). Datasheet del fabricante: pendiente para TS-1187A (URL oficial sin respuesta; dibujo de LCSC), KT-0603YG (el de LCSC es XL-0603QYGC) y B-2100S04P (LCSC). LCSC encuentra todas las piezas; no hay «solo montaje».

## Pendiente

- Coordinador: decidir las propuestas DEC-0007 (C23 → C15849 recomendada; U6 UMW; D5) y llevar a `mcu.md`: TS-1187A-B-A-B es Basic; C14663 confirmado Basic (34,7 M); stocks de la tabla; C318887 mide 2,5 mm de alto y 260 gf; huellas `esp-riego:` para U5, SW1/SW2 y J2 (§11 y Anexo A, que citan `RF_Module:` y `Button_Switch_SMD:`).
- SPEC-0022: usar `esp-riego:` en Footprint de U5, SW1, SW2 y J2, y la tabla de campos.
- Validación: revisar las piezas de «Requiere verificación».
- Datasheets del fabricante para TS-1187A, KT-0603YG y la tira (no localizados).

## Notas para el siguiente agente

- Las huellas propias `esp-riego:` llevan 3D con `${KIPRJMOD}/../libraries/3d/`, salvo el módulo (`${KICAD10_3DMODEL_DIR}`, existe en 10.0.6).
- Los pulsadores tienen pads duplicados 1,1,2,2: usar `Switch:SW_Push` con pines 1 y 2.
- La guardia no admite variables de shell en rutas de salida: escribir rutas literales.
