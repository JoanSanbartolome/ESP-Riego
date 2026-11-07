---
spec: SPEC-0022
agente: ing-esquematicos
n: 01
fecha: 2026-11-07
estado: completado
---

# SPEC-0022 · 01 · ing-esquematicos

## Orden recibida

SPEC-0022 · rama spec/SPEC-0022-hoja-mcu (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/specs/SPEC-0022-hoja-mcu.md y todas sus Entradas (docs/diseno/mcu.md, gestion/logs/SPEC-0021/01-jr-conformidad.md «Tabla de campos por referencia», gestion/informes/VAL-0021-01.md, gestion/logs/SPEC-0023/01-ing-esquematicos.md y 03-ing-esquematicos.md, docs/diseno/salidas.md, hardware/v2/alimentacion.kicad_sch, fichas del MCU en hardware/componentes/, DEC-0007, gestion/checklists/esquema.md v6) · Haz: el paso 1 de la spec: sustituye el contenido de hardware/v2/mcu.kicad_sch por el bloque MCU de la v2 según mcu.md (piezas, valores, pines y etiquetas jerárquicas del Anexo C, conectadas con alimentacion.kicad_sch), con los campos de la tabla de SPEC-0021 y las huellas esp-riego:ESP32-S3-WROOM-1, esp-riego:SW_Push_1P1T_XKB_TS-1187A y esp-riego:USB_C_Receptacle_HRO_TYPE-C-31-M-12; ninguna librería de la v1. Actualiza docs/diseno/mcu.md (§11, Anexo A, cambios de compra de DEC-0007 con recálculo: C23→C15849, D5→KT-0603R C2286 con R23, U6 UMW C2687116 solo si la equivalencia con el datasheet se comprueba; y §9.2/Anexo B según el log de SPEC-0023). No toques la PCB (la sincroniza ing-layout en el paso 2): la paridad pendiente se lista en el log y debe deberse solo a piezas de esta hoja. Eres el único usuario de KiCad: save y close_project al terminar. Verifica con python herramientas/verificar.py hardware/v2 (ERC 0). · Entrega: hardware/v2/mcu.kicad_sch + docs/diseno/mcu.md (y el .kicad_pro solo si es imprescindible, justificándolo) + log gestion/logs/SPEC-0022/01-ing-esquematicos.md con el repaso de la checklist y la salida de verificar.py. Brevedad: en tu respuesta solo el contrato de salida; log telegráfico.

- Rama `spec/SPEC-0022-hoja-mcu` ✔. KiCad sin abrir (`check_kicad_ui`: no corre); sin `.lck`.

## Contexto consultado

- Spec; `docs/diseno/mcu.md`; logs 01/03 de SPEC-0021 (tabla de campos, Datasheet corregido); VAL-0021-01; logs 01/03 de SPEC-0023; `salidas.md` §3, §7, §10, §12, Anexo B; DEC-0007; checklist `esquema.md` v6; `hardware/v2/alimentacion.kicad_sch` (etiquetas, formato) y raíz.
- Fichas `USBLC6-2SC6.md`, `bloque-alimentacion.md` (D4); datasheets: ST USBLC6-2SC6 Rev 5 (tabla 2, p. 2, local); UMW USBLC6-2SC6 nov. 2024 (PDF de LCSC C2687116, pp. 1-3); KT-0603R (PDF de LCSC C2286, pp. 3-4).
- API de JLCPCB (2026-11-07): C2286 Basic 6,63 M · C15849 Basic 13,0 M · C2687116 Extended 95 007 · C7519 Extended 22 169; `dataManualUrl` de C2286 y C15849.
- Símbolos de KiCad 10.0.6 (`share/kicad/symbols`): RF_Module, Connector, Connector_Generic, Device, Power_Protection, Switch, power.

## Acciones

1. Hoja generada por script propio del *scratchpad* (`s22/s22_gen.py`; `s22_sx.py` extrae y aplana los símbolos de la librería, `USBLC6-2SC6` es derivado de `USBLC6-2P6`). Probada antes sobre una copia de `hardware/v2` + `libraries`; luego copiada.
   - `hardware/v2/mcu.kicad_sch` (A3): 21 piezas (U5, U6, J2, J3, SW1, SW2, D5, C23–C26, R16–R25), 22 símbolos de alimentación (#PWR056–077), 39 etiquetas locales, 25 jerárquicas (Anexo C), 8 no conexiones (GPIO3, 10, 18, 39, 45, 46; SBU1/2), textos de bloque y notas.
   - Conexiones por etiquetas en los extremos de los pines (sin cables). `lib_symbols` = copias de KiCad 10.0.6 (0 `lib_symbol_mismatch`).
   - Campos de las 21 piezas: `Value`, `Footprint`, `Datasheet`, `Description`, `MPN`, `LCSC Part#` y `Fabricante` de la tabla de SPEC-0021, con C23 → C15849 y D5 → KT-0603R C2286.
2. Raíz `hardware/v2/esp-riego.kicad_sch` (`s22_root.py`): hoja MCU movida a (50,8; 40,64), 38,1 × 53,34 mm, con 25 pines; Salidas y Conectores movidas a x = 190,5 (sitio para etiquetas); etiquetas locales VBUS, VIN_SENSE, LIM_IMON, LIM_FLT y LIM_EN entre MCU y Alimentacion; quitadas sus 5 no conexiones provisionales; no conexión provisional en los 20 pines MCU sin destino (BUS_24V conserva la suya). Justificación de los pines de Alimentacion corregida a la nativa de KiCad (ángulo 0 → `right`, 180 → `left`; antes el nombre salía fuera de la caja). Fecha 2026-11-07.
3. `docs/diseno/mcu.md`: cabecera (Rev. SPEC-0022), §0, §2 (huella `esp-riego:`, stock 2 776), §4 (comparación ST/UMW), §5.1 (C15849 y nueva simulación), §7 (KT-0603R), §8.2 (LED 1,8 mA, total 433 mA), §9.2 (IS: R_IS 820 Ω/C_IS, sin diodo, 6 dB; LED de canal en IN; DSEL común del BTT6030), §11 (tabla con tipo/stock de SPEC-0021, huellas, alternativas, *extended*, coste), §12 (EPAD 12 vías, serigrafía «STATUS»), §13, §14.7, Anexo A (hecho en SPEC-0021), Anexo B (IS), Anexo C (implementación).
4. `hardware/v2/README.md`: fila MCU, nota de no conexiones provisionales y estado de verificación (fuera de la lista de entrega, pero en mi zona: documentaba la hoja como «pendiente»).
5. MCP: no se cargó ningún proyecto (solo `check_kicad_ui` y `find_overlapping_elements` sobre la copia). `close_project` → «nothing to close». `.kicad_pro`, `.kicad_prl` y `.kicad_pcb` sin tocar.

## Decisiones y justificación

- **C23 → C15849 (aplicado, DEC-0007):** τ mín. = 10 k × 0,99 × 1 µ × 0,9 × 0,816 × 0,984 = 7,16 ms; simulación (`s22_en.py`) reproduce las cifras de VAL-0021-01: EN/VDD = 0,159 (buck 6 ms) < 0,25; liberación 9,9–18,5 ms. X5R 50 V vale a 60 °C. `mcu.md` §5.1.
- **D5 → KT-0603R C2286 (aplicado por orden del coordinador):** R23 = 1 kΩ sin cambios; I 1,4 mA típ., ≤ 1,8 mA (≪ 25 mA, p. 3), ≥ 0,24 mA; P_R23 3,2 mW. Pierde la distinción por color con D4 (criterio del autor en §7, VAL-0021-01 lo dejaba al usuario): se distingue con serigrafía «STATUS» (§12). Alternativa KT-0603YG (C2289) con la misma huella.
- **U6 se queda en ST (UMW no aplicado):** el UMW da V_RWM = 5 V (< 5,25 V de VBUS máx.) y no da condiciones de medida ni esquema interno; mejor en capacidad y V_CL. No cumple «sin empeorar ninguna especificación» (DEC-0007). Ahorro perdido: 0,11 $/placa, sin cargo *extended* menos. `mcu.md` §4.
- **Campo extra `Fabricante`:** la tabla de SPEC-0021 lo incluye; `alimentacion.kicad_sch` no lo tiene (incoherencia menor entre hojas). «tipo» (Basic/Extended) del criterio de la spec: no es campo de símbolo; está en `mcu.md` §11.
- **Value genéricos** (`SW_Push`, `LED`, `Conn_01x04`, `USB_C_Receptacle_USB2.0_16P`): los de la tabla de SPEC-0021.
- **Dibujo por script y no con el MCP:** reproducible y sin las copias antiguas de `lib_symbols` del MCP (lección de SPEC-0019). Comprobado con netlist, ERC y PDF.

## Verificación

- `python herramientas/verificar.py hardware/v2`:
  - ERC 0 (errores 0, avisos 0).
  - DRC 0 (errores 0, avisos 0, sin conectar 108: PCB sin rutar, igual que antes).
  - Paridad 32 → «CON INCIDENCIAS»: 21 `missing_footprint` (las 21 piezas de esta hoja) + 11 `net_conflict`, causados por esta hoja: al unir MCU y Alimentacion por la raíz, las redes `/Alimentacion/{VBUS,VIN_SENSE,LIM_IMON,LIM_FLT,LIM_EN}` pasan a `/VBUS`, `/VIN_SENSE`, `/LIM_IMON`, `/LIM_FLT` y `/LIM_EN`. Pads afectados: C5.1, R4.2 (LIM_IMON); C15.1, U3.6 (VBUS); C20.1, R14.2, R15.1 (VIN_SENSE); R5.1, U1.12 (LIM_EN); R6.2, U1.14 (LIM_FLT). Ninguna otra diferencia.
- Netlist `kicadsexpr` frente a `mcu.md` §4–§9.2: todas las redes coinciden (EN, BOOT, USB_DP/DM y _C, CC1/2, TXD0/UART_TX/UART_RX, LED_STATUS/LED_A, I²C con R24/R25, VBUS con J2/U6/C26/U3.6/C15, GPIO por número de pin del módulo). 6 pines del módulo y SBU1/2 sin conectar, como en §9.2.
- PDF exportado de la copia (con `../libraries`): cajetín de la hoja MCU con «Microcontrolador: ESP32-S3, USB-C y UART», ESP-Riego v2, rev. 2.0-dev, 2026-11-07, A3, 3/5. Sin textos solapados (revisado en PNG); `find_overlapping_elements`: solo símbolos de alimentación sobre pines (esperado).

### Repaso de `gestion/checklists/esquema.md` v6

Estructura
- Hojas jerárquicas, ninguna huérfana: cumple (MCU con 25 pines; 20 con no conexión provisional hasta Salidas/Sensores/Conectores).
- Cajetín en el PDF: cumple (ver arriba).
- ERC sin errores ni avisos: cumple (0/0).
- Referencias anotadas, sin duplicados: cumple (U5–U6, J2–J3, SW1–SW2, D5, C23–C26, R16–R25; #PWR056–077 sin chocar con #PWR001–055).

Campos
- `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet`, `Description`: cumple en las 21 (más `Fabricante`). Datasheet: URL del fabricante (U5, U6) o `dataManualUrl` de LCSC.
- Huella existente: cumple (3 `esp-riego:` + oficiales).
- Huellas con vías conforme a FAB-02: cumple (`esp-riego:ESP32-S3-WROOM-1`, 0,3/0,6; VAL-0021-01).
- DNP: no aplica (todo montado).

Cálculos
- Fórmula, fuente y margen: cumple para los valores tocados (§5.1 EN, §7 LED, §8.2, §4 U6).
- Recalculado por el revisor: pendiente (validación).
- Tensiones nominales ≥ peor caso: cumple (C23 50 V, C26 16 V en VBUS ≤ 5,25 V; U6 en VBUS: ST V_RM 5,25 V).
- *Derating* de cerámicos: cumple (C23 −18,4 %/−1,6 %; C24 §8.1).
- E_AS, *hold-up*: no aplica a esta hoja.
- Disipación a 60 °C: cumple (TLV1117LV §8.3 sin cambios; R23 3,2 mW).

Alimentación: no aplica a esta hoja salvo «VBUS unido sin retroalimentación»: cumple (VBUS → U3 VIN2 del TPS2116, `alimentacion.md` §3.8).

Microcontrolador
- Pines de arranque sin cargas: cumple (GPIO3/45/46 NC; GPIO0 solo R17 + SW2).
- Analógicas solo en ADC1 GPIO1–10: cumple (VIN_SENSE 1, LIM_IMON 2, IS1–6 en 4–9).
- GPIO19/20 solo USB: cumple; GPIO35–37 usados (N8 sin PSRAM octal).
- RC en EN, BOOT y RESET: cumple (R16/C23/SW1; R17/SW2).
- Desacoplo según la HDG: cumple (C24 22 µF + C25 100 nF en 3V3; C23 1 µF en EN).
- Pinout coherente con el YAML: pendiente (no existe `firmware/`; la tabla de §9.2 y el Anexo B son la fuente).

Salidas e interfaces de campo
- Salidas apagadas en reset/flasheo: cumple en esta hoja (IN, OUT_DEN y LIM_EN en pines sin WPU ni pulso alto, §9–§10); las R_PD van en Salidas (SPEC-0025) y R5 ya está en Alimentacion.
- IS acotada: cumple por diseño (`salidas.md` §3; R_IS/C_IS van en la hoja de salidas).
- Sensor e I²C: *pull-ups* R24/R25 en esta hoja; SHT4x y expansión en sus specs. Resto: no aplica.

Entregables para layout
- Tabla de restricciones: cumple (`mcu.md` §12, con EPAD y serigrafía «STATUS» añadidas).

## Pendiente

- **ing-layout (paso 2):** sincronizar la PCB: 21 huellas nuevas (fuera del contorno, agrupadas) y renombrar las 5 redes de Alimentacion (11 pads) a `/VBUS`, `/VIN_SENSE`, `/LIM_IMON`, `/LIM_FLT`, `/LIM_EN`. Serigrafía «STATUS» junto a D5 (§12).
- **Coordinador:** D5 rojo cambia el criterio de color de `mcu.md` §7 (VAL-0021-01 lo dejaba al usuario): confirmar que consta la decisión. U6 UMW no aplicado (§4). VAL-0021-01-03 (vías del EPAD abiertas a 0,10 mm de la pasta) anotado en §12 para layout y fabricación.
- **Coordinador / layout:** criterio «Campos (… tipo)»: no hay campo de tipo en los símbolos; si se quiere, decidir nombre y aplicarlo a todas las hojas.
- **Validación:** recalcular §5.1 (EN), §7 (LED) y la comparación de §4.
- **Firmware (FW-02):** el YAML se deriva de `mcu.md` §9.2 cuando se cree `firmware/`.

## Notas para el siguiente agente

- La hoja usa solo etiquetas en los extremos de los pines: para mover una pieza hay que mover también sus etiquetas (o regenerar con `s22_gen.py` del *scratchpad*, que no se versiona).
- Etiqueta local y jerárquica del mismo nombre se unen dentro de la hoja (I2C_SDA/SCL en R24/R25, VBUS en J2/C26).
- Las hojas que añadan Salidas, Sensores o Conectores deben quitar la no conexión provisional del pin correspondiente de la hoja MCU en la raíz y unirlo (etiqueta local en la raíz, como VBUS…LIM_EN).
