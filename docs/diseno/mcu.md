# Bloque MCU: módulo, USB-C, arranque, UART, LED y tabla de GPIO (SPEC-0020)

**Estado:** propuesta para validación. **Autor:** ing-esquematicos · **Fecha:** 2026-11-05. **Rev. VAL-0020-01** (2026-11-06): referencias renumeradas (C23–C26), DEN común fijado por DEC-0007, observaciones 02–07.
**Requisitos:** MCU-01…MCU-07, ALI-07 (comprobación del TLV1117LV), REL-04, REL-10 (pines de IS), AMB-01, EXP-01, EXP-02 (pines).
**Precios y stock:** LCSC, consulta del 2026-11-05 (`wmsc.lcsc.com/.../product/detail?productCode=…`); C2913198 y los cambios de compra de DEC-0007 revisados el 2026-11-06. El tipo Basic/Extended lo confirma jr-conformidad (SPEC-0021).

> Datasheets (las páginas son las impresas en el documento):
> - **WROOM-1:** ESP32-S3-WROOM-1/1U Datasheet v1.8 (`hardware/componentes/datasheets/ESP32-S3-WROOM-1.pdf`).
> - **S3:** ESP32-S3 Series Datasheet v2.2 (espressif.com, descargado el 2026-11-05).
> - **HDG:** ESP32-S3 Hardware Design Guidelines, *release master* (docs.espressif.com, generado el 2026-11-05).
> - **TLV:** TLV1117LV SBVS160C (ene. 2023). **LMR:** LMR36520 SNVSBF0C (nov. 2025). **TPS2116:** SLVSFG1A (may. 2021).
> - **BTT:** BTT6050-1ERA Rev. 1.00 (`hardware/componentes/datasheets/BTT6050-1ERA.pdf`).
> - **USBLC6:** USBLC6-2SC6 Rev 5 (ficha). **TYPE-C:** TYPE-C-31-M-12 (ficha).

## 0. Resumen

| Función | Pieza principal | Alternativa | Requisito |
|---|---|---|---|
| MCU | ESP32-S3-WROOM-1-**N8** (8 MB de flash, sin PSRAM, −40…85 °C), C2913198 | ESP32-S3-WROOM-1-N16 (C2913199) | MCU-01 |
| Antena | Antena del módulo **fuera del borde lateral**, en una esquina; zona libre según HDG Fig. 26 | — | MCU-02 |
| USB-C | HRO TYPE-C-31-M-12 (C165948) + USBLC6-2SC6 (C7519) + CC 2 × 5,1 kΩ + 2 × 22 Ω en serie | TYPE-C-31-M-12A (C5337088) · USBLC6 UMW (C2687116) | MCU-03, ALI-08 |
| RESET / EN | RC de 10 kΩ / 1 µF + pulsador XKB TS-1187A-B-A-B (C318884) | TS-1187A-C-E-B (C318887) | MCU-04 |
| BOOT / GPIO0 | *Pull-up* de 10 kΩ + pulsador igual al de RESET | ídem | MCU-04 |
| UART | Tira de 4 pines a 2,54 mm (3V3 · TX · RX · GND), 470 Ω en TXD0 | tira de 40 pines cortada (C2337) | MCU-06 |
| LED de estado | KT-0603YG (verde-amarillo, V_F 2,0–2,2 V, C2289) + 1 kΩ en GPIO40 | KT-0603Y (C2287) | MCU-07 |
| Desacoplo | 22 µF X5R 0805 (C45783) + 100 nF (C14663, Basic; DEC-0007) en el pin 3V3 | — | ALI-07 |

Resultados clave:

- **GPIO (MCU-05):** caben las 8 entradas analógicas en ADC1 (VIN_SENSE, LIM_IMON e IS1–IS6), sin usar GPIO3. Las salidas van solo en pines sin *pull-up* ni pulso alto en el arranque. Hay **un DEN común** a los 6 canales (§9.2, fijado por DEC-0007) y quedan 3 pines libres. La variante con un DEN por canal (§9.3) queda descartada: ocupa los 28 pines.
- **REL-04:** con el *chip* en reset, en el arranque y en el modo de descarga, los pines de IN, DEN y LIM_EN están en alta impedancia o a nivel bajo. Las resistencias de *pull-down* fijan el nivel bajo (≤ 5 mV frente a V_IN(L) ≤ 0,8 V). El OTA y los reinicios por software se cubren desde el firmware (§10).
- **EN:** con la rampa más lenta del raíl de 3,3 V (*soft-start* del buck de 6 ms y τ mínimo), EN está a ≤ 0,16·VDD cuando VDD llega a 3,0 V: el *chip* sigue en reset hasta que el raíl es estable (§5).
- **3,3 V (ALI-07):** 0,43 A de pico (0,45 A de diseño), con 1 A de capacidad. La caída es ≤ 0,70 V, y el margen es de 0,88 V con el buck y de 0,37 V con USB a 4,40 V. T_J = 109 °C a 60 °C de ambiente. Pico de Wi-Fi: ≈ 40 mV de caída. **El TLV1117LV de `alimentacion.md` vale; no se cambia** (§8).
- **Piezas nuevas:** ningún símbolo ni huella. Falta el **modelo 3D** del pulsador TS-1187A, que no viene en KiCad 10.0 (§11).

## 1. Datos de partida

| Dato | Valor | Origen |
|---|---|---|
| Raíl de 3,3 V | TLV1117LV desde +5V; 4,881–5,107 V por el buck y VBUS por el TPS2116 | `alimentacion.md` §3.8 y §3.9 |
| Precisión de +3V3 | ± 2,7 % a 25 °C → 3,211–3,389 V | `alimentacion.md` §3.9 |
| Ambiente del módulo | 50 °C + 10 °C dentro de la caja = **60 °C** | §5 de `docs/02`, checklist de esquema |
| Pines que pide alimentación | VIN_SENSE, LIM_IMON (ADC1, 6 dB), LIM_EN (salida, R5 de 10 kΩ a GND), LIM_FLT (entrada, R6 de 10 kΩ a +3V3) | `alimentacion.md` §6 |
| Pines de las salidas | 6 × IN, DEN, 6 × IS a ADC1 con R_SENSE de 10 kΩ; R_IN = R_DEN = 10 kΩ | `estudio-salidas.md` S7, §11.5; BTT §6.4, p. 19 |
| Expansión | I²C, ≥ 2 GPIO (uno de interrupción), 3V3 y GND; detalle pendiente de SPEC-0006 | EXP-02 |

## 2. Módulo (MCU-01)

- **ESP32-S3-WROOM-1-N8:** flash de 8 MB *quad*, sin PSRAM (WROOM-1 tabla 1-1, p. 3).
  - Temperatura: −40…85 °C. Las variantes R8/R16V solo llegan a 65 °C (p. 3): margen de 25 °C sobre los 60 °C de la caja, frente a 5 °C con ellas.
  - Sin PSRAM octal, GPIO35–37 quedan libres (tabla 3-1, nota b, p. 12) y se usan (§9). **La placa no admite variantes R8 ni R16V.**
  - 8 MB bastan para ESPHome con OTA (dos particiones de aplicación de ≤ 3 MB cada una).
- Alimentación: 3,0–3,6 V, con una fuente de ≥ 0,5 A (tabla 6-2, p. 27). El TLV1117LV da 1 A (§8).
- LCSC: C2913198, stock 3 277. 4,91 $ (1–9 uds.) y 4,2345 $ (10–29 uds.).
- Alternativa: N16 (C2913199, stock 1 985, 5,00 / 4,48 $), con la misma huella y los mismos pines. N4 (C2913197) no cumple MCU-01.
- Símbolo y huella oficiales: `RF_Module:ESP32-S3-WROOM-1`. La huella trae la zona de *keepout* de la antena en todas las capas de cobre (§3). El modelo 3D oficial existe.
- EPAD (pin 41) a GND, con vías térmicas y poca pasta: el exceso levanta el módulo (WROOM-1 §9, p. 41).

## 3. Antena (MCU-02)

Fuente: HDG §1.4.7 (pp. 28-31, Fig. 24 y 26) y WROOM-1 §11.2 (p. 46).

- **Posición:** módulo en una esquina, con la antena **sobresaliendo del borde lateral** (posiciones 3 o 4 de la Fig. 24, p. 30). Los laterales están reservados para la antena (FAB-07).
  - El punto de alimentación de la antena (*feed point*) mira hacia la esquina de la placa.
  - Según la Fig. 24 («*antenna feed point on the right*»), es el lado derecho del módulo con la antena arriba. El layout lo confirma con el modelo 3D.
- **Si la antena no puede sobresalir:**
  - Zona libre de 6 mm (alto de la antena) × ≥ 15 mm hacia el lado contrario al punto de alimentación, recortando la placa (Fig. 26, p. 31).
  - Las cotas «Max 1» y «Max 2» de la Fig. 26 fijan la alineación del módulo con los bordes.
  - En la placa, nada de cobre, pistas, vías ni componentes dentro del *keepout* de la huella oficial (21 × 48 mm, en todas las capas).
- **Caja:** ≥ 15 mm libres alrededor de la antena en todas direcciones, dentro de la caja (HDG p. 30). Se comprueba con la decisión D5 (caja).
- **Lejos de:**
  - el buck (SW, L1), las salidas (*high-side*), el USB, la UART y el SHT4x: **objetivo del autor de ≥ 15 mm** del área de la antena. No es un requisito de la HDG: la HDG da 15 mm solo como zona libre dentro de la caja (p. 30), y para el USB y la UART pide «*as far away from the antenna as possible*» (§1.4.4, p. 28);
  - en una placa de ≤ 100 × 70 mm puede no ser realizable: el *floorplan* justifica una distancia menor si hace falta.
- **Tamaño:** si la antena sobresale, el módulo asoma ≈ 6 mm del contorno. Si FAB-08 (≤ 100 mm) cuenta lo que sobresale, el ancho de la placa baja a ≤ 94 mm. Lo decide el *floorplan*, con la decisión D5 (caja).
- Hay que poner abundante cobre de GND y vías de cosido junto a la antena, pero fuera de la zona libre (HDG p. 30).

## 4. USB-C (MCU-03, ALI-08)

```
J2 VBUS (A4/A9/B4/B9) ─┬─ U6 pin 5 (VBUS) ─┬─ C26 4,7 µF ── VBUS → U3 VIN2 (alimentación)
J2 CC1 (A5) ─ R18 5,1 kΩ ─ GND           │
J2 CC2 (B5) ─ R19 5,1 kΩ ─ GND           │
J2 D+ (A6+B6) ─ U6 I/O1 (1↔6) ─ R20 22 Ω ─ GPIO20 (USB_D+)
J2 D− (A7+B7) ─ U6 I/O2 (3↔4) ─ R21 22 Ω ─ GPIO19 (USB_D−)
J2 SBU1/SBU2 sin conectar · J2 SHIELD a GND · U6 pin 2 a GND
```

- **CC:** 5,1 kΩ al 1 % a GND en cada CC, como *sink* (MCU-03).
  - Con una fuente Type-C da como mínimo el perfil por defecto de USB.
  - Sin ellas, un cargador C-C no da VBUS.
- **ESD:** USBLC6-2SC6 junto al conector.
  - *Clamping* V_CL de 12 V a 1 A y de 17 V a 5 A (8/20 µs), y 3,5 pF máx. por línea (ficha, tabla 2, p. 2): apto para 12 Mb/s.
  - Las líneas de datos pasan por los pines de I/O, sin derivaciones.
  - El pin VBUS del USBLC6 va a VBUS: protege también la entrada VIN2 del TPS2116.
- **22 Ω en serie** junto al módulo: valor inicial de la HDG §1.3.13 (p. 18). Los condensadores a GND que la HDG deja «sin montar» no se ponen.
- **Condensador de VBUS:** C26 = 4,7 µF 16 V X5R 0603 (C19666). Con el C15 de 1 µF del TPS2116 (`alimentacion.md` §3.8) suman 5,7 µF, por debajo de los 10 µF que admite USB 2.0 en un dispositivo.
- **Corriente con solo USB:**
  - 3,3 V: 0,45 A, por debajo de los 0,5 A de un puerto USB 2.0.
  - El 5 V de la expansión (0,30 A) no cabe en un puerto USB 2.0. Con solo USB se programa sin la expansión o con poca carga en ella (ALI-08 solo exige la lógica).
- Unión al raíl de 5 V por el TPS2116, en modo prioridad del buck (`alimentacion.md` §3.8): VBUS no retroalimenta la entrada ni el PC.
- Con solo USB, VIN_SENSE ≈ 0 V: el firmware sabe que no hay 24 V sin usar el pin ST del TPS2116, que queda sin conectar.

## 5. EN, RESET y BOOT (MCU-04)

### 5.1 EN

- R16 = 10 kΩ de +3V3 a EN y C23 = 1 µF X7R 16 V (C106248) de EN a GND, junto al pin 3. SW1 (RESET) va en paralelo con C23.
  - Es el valor que recomienda Espressif (WROOM-1 §9, p. 41; HDG §1.3.3, p. 8).
- Umbrales: el reset es seguro con EN ≤ V_IL_nRST = 0,25·VDD y la liberación, con EN ≥ V_IH_nRST = 0,75·VDD (S tabla 5-4, p. 65). Además, t_STBL ≥ 50 µs desde que el raíl es estable y t_RST ≥ 50 µs de pulso (WROOM-1 tabla 4-6, p. 16).
- Simulación numérica de la red RC, con τ entre 7,35 ms y 11,1 ms. τ mín. = 10 kΩ × 0,99 × 1 µF × 0,90 (tolerancia ±10 %) × 0,85 (polarización a 3,3 V, −15 % conservador: sin curva del fabricante para C106248) × 0,97 (−3 % a 60 °C) = 7,35 ms; τ máx. = 10 kΩ × 1,01 × 1 µF × 1,10 = 11,1 ms:

| Arranque del raíl de 3,3 V | VDD llega a 3,0 V en | EN/VDD en ese momento (τ mín. 7,35 ms) | EN ≥ 0,75·VDD en (τ 7,35–11,1 ms) |
|---|---|---|---|
| Escalón (USB ya presente, rearme) | 0 | 0 | 10,2–15,4 ms |
| VBUS por el TPS2116 (1,7 ms de subida, TPS2116 §8.2.2, p. 15) | 1,55 ms | ≈ 0,10 (0,083 con 8,8 ms, escalado) | ≈ 11–16 ms |
| Buck con t_SS = 3 / 6 ms (LMR p. 7) y el LDO desde su UVLO de 1,95 V (TLV p. 5) | 1,98 / 3,96 ms | 0,081 / **0,155** | 11,6–18,3 ms |
| Cota pesimista: rampa lineal de 0 a 3,3 V en 6 ms | 5,46 ms | 0,294 | 13,4–18 ms |

- **Cumple:** en los casos reales, EN ≤ 0,155·VDD < 0,25·VDD cuando el raíl llega a 3,0 V (recalculado por validación con τ = 7,35 ms). El *chip* no sale de reset antes de que el raíl sea estable, y lo hace entre 10 y 18 ms después (≫ 50 µs).
  - Con el TPS2116, que solo conecta VIN1 por encima del umbral de PR1 (3,9–4,72 V) y con su *soft-start*, el caso del buck baja a 0,04–0,08: el de la tabla es conservador.
  - La cota pesimista no es física, porque el TLV1117LV no da salida por debajo de su UVLO; con τ mín. supera el umbral (0,294), así que no es caso de diseño.
  - Si el prototipo arranca mal con fuentes lentas, C23 se sube a 2,2 µF (≈ 0,08 en el caso del buck de 6 ms, estimado por escalado).
- **Reset con el pulsador:** cortocircuita C23. El pulso dura ≫ 50 µs. Al soltar, el *chip* arranca a los 10–15 ms.
- **Apagado y vuelta rápida:** si la tensión se corta y vuelve en menos de ≈ τ, EN puede no bajar del umbral. El detector de *brown-out* del ESP32-S3 resetea igualmente al caer VDD. La HDG pide un supervisor solo con arranques lentos, ciclos frecuentes o fuentes inestables (p. 9); la fuente LED no está en esos casos. No se añade supervisor: queda como prueba del prototipo (§14).

### 5.2 BOOT (GPIO0)

- R17 = 10 kΩ de GPIO0 a +3V3 y SW2 de GPIO0 a GND. **Sin condensador** en GPIO0 (HDG §1.3.9, p. 15: *pull-up* recomendado; un condensador grande puede dejar el *chip* en descarga).
- Descarga: mantener BOOT, pulsar y soltar RESET. GPIO0 se muestrea con t_H ≥ 3 ms (WROOM-1 tabla 4-2, p. 14) y GPIO46 está a 0 por su *pull-down* interno: arranque conjunto de descarga (tabla 4-3, p. 14).
- Por USB no hacen falta los pulsadores: el controlador USB-Serial/JTAG reinicia el *chip* en modo de descarga.
- **GPIO3, GPIO45 y GPIO46, sin conectar:**
  - GPIO3 no tiene efecto con los eFuse por defecto (WROOM-1 tabla 4-5, p. 16);
  - GPIO45 a 0 → VDD_SPI = 3,3 V, la tensión de la flash (tabla 4-4, p. 15). Si estuviera alto, la flash de 3,3 V recibiría 1,8 V y no arrancaría;
  - GPIO46 a 0 hace falta para la descarga.

## 6. UART de programación (MCU-06)

- J3, tira de 4 pines macho a 2,54 mm, vertical y THT: 1 = +3V3, 2 = TXD0 (GPIO43), 3 = RXD0 (GPIO44), 4 = GND. La serigrafía indica el sentido (TX del módulo).
- R22 = 470 Ω en serie con TXD0, junto al módulo. La HDG recomienda 499 Ω contra armónicos (§1.3.7, p. 13); se usa el valor más cercano de la serie E12 en la librería básica.
- **El pin de 3V3 es una referencia:** no sirve para alimentar la placa.
  - Si un adaptador lo alimenta, carga el raíl y, por el diodo interno del TLV1117LV, el nodo de +5V (TLV §7.3.1: corriente inversa no limitada; el TPS2116 bloquea hacia VIN1).
  - Serigrafía: «3V3 OUT». Para programar sin fuente se usa el USB-C (ALI-08).
- Adaptador de 3,3 V: el ESP32-S3 no tolera 5 V (V_IH máx. = VDD + 0,3 V, S tabla 5-4, p. 65).
- No hay reinicio automático por DTR/RTS: con la UART se usan BOOT y RESET a mano. MCU-06 no lo pide.

## 7. LED de estado (MCU-07)

- GPIO40 → R23 = 1 kΩ → D5 KT-0603YG → GND, activo alto.
  - I_típ = (3,3 − 2,1)/1 k ≈ 1,2 mA.
  - I_máx = (3,39 − 2,0)/1 k = 1,4 mA.
  - I_mín ≈ (2,64 − 2,2)/1 k = 0,44 mA, con V_OH ≥ 0,8·VDD medida en alta impedancia (S tabla 5-4).
- Excitación directa desde el GPIO: a diferencia del LED de canal, este no indica nada crítico y su brillo no tiene que estar garantizado.
- Verde-amarillo (AlGaInP, V_F 2,0–2,2 V), para distinguirlo del LED rojo de alimentación. Descartado el KT-0603G (verde InGaN, V_F 3,1 V): no tiene margen con 3,3 V.
- Se usa GPIO40 porque en el modo de descarga USB-OTG la ROM lo pone a nivel alto (HDG tabla 12, p. 19). Ahí el LED encendido avisa de que el *chip* está en descarga, sin riesgo. No sirve para ninguna salida ni para el limitador.

## 8. Desacoplo y raíl de 3,3 V (ALI-07)

### 8.1 Desacoplo del módulo

- C24 = 22 µF 25 V X5R 0805 (C45783) y C25 = 100 nF 50 V X7R (Yageo CC0603KRX7R9BB104, C14663, Basic; cambio de compra de DEC-0007 en lugar de C1591), en el pin 2 (3V3), según la Fig. 9-1 de WROOM-1 (p. 41: C1 22 µF y C3 0,1 µF).
  - *Derating* de C24 (SimSurfing CL21A226MAQNNN): −32,3 % a 3,3 V y −3,5 % a 60 °C; tolerancia ±20 % (LCSC C45783). Efectivo: 22 × 0,677 × 0,965 × 0,8 = **11,5 µF** en el peor caso (14,4 µF típicos) ≥ 10 µF, que la HDG pide en VDD3P3 para los picos de transmisión (§1.3.2, p. 8) ✔.
- Con C19 (10 µF) y C21 (100 nF) a la salida del LDO (`alimentacion.md` §3.9): ≈ 25 µF efectivos en +3V3.

### 8.2 Presupuesto de +3V3

| Carga | Corriente | Fuente |
|---|---|---|
| Módulo, pico de TX 802.11b a 20,5 dBm, 100 % de ciclo | 355 mA | WROOM-1 tabla 6-4, p. 28 |
| SHT4x en medida (sin calentador) | 0,5 mA | ficha SHT4x, p. 9 |
| LED de estado y LED de alimentación | 1,4 + 1,4 mA | §7; `alimentacion.md` §3.11 |
| *Pull-ups* de I²C a nivel bajo: placa 2 × 0,7 mA y expansión 2 × 1,5 mA | 4,4 mA | §11 |
| *Pull-ups* y *pull-downs* de control (R6, R5, IN y DEN) | ≈ 1,1 mA | §10.2 |
| LED de los 6 canales, si se alimentan de +3V3 (REL-07, bloque de salidas) | ≤ 18 mA | reserva de 3 mA por canal |
| 3,3 V del conector de expansión | ≤ 50 mA | `alimentacion.md` §4 |
| **Total** | **≈ 432 mA** (diseño: 0,45 A) | |

- El calentador del SHT4x (hasta 200 mW / 3,3 V = 61 mA durante ≤ 1 s, ficha p. 13) no se usa (AMB-02). Si se usara, el total subiría a 0,49 A, todavía dentro de 1 A.

### 8.3 Comprobación del TLV1117LV

| Comprobación | Cálculo | Resultado |
|---|---|---|
| Corriente | 0,45 A ≤ 1 A nominal; I_CL ≥ 1,1 A (TLV p. 5); el módulo pide una fuente de ≥ 0,5 A (WROOM-1 tabla 6-2) | ✔ (2,2×) |
| Caída con el buck | +5V mín. 4,881 V − 3,3 V − V_DO máx. 0,70 V (1 A, TLV p. 5) | Margen **0,88 V** ✔ |
| Caída con USB, puerto de 4,75 V | 4,75 − 0,03 (TPS2116, 60 mΩ × 0,5 A) − 3,3 − 0,70 | Margen 0,72 V ✔ |
| Caída con USB al mínimo de USB 2.0 en el dispositivo (4,40 V) | 4,40 − 0,03 − 3,3 − 0,70 | Margen **0,37 V** ✔ |
| Conmutación del TPS2116 (+5V hasta 3,9 V, `alimentacion.md` §3.8) | V_DO a 0,45 A ≈ 0,7 Ω × 0,45 = 0,32 V (PMOS resistivo, TLV §7.3.2) → regula con ≥ 3,62 V | ✔ (transitorio) |
| Disipación con el buck | (5,107 − 3,3) × 0,45 = 0,81 W; R_θJA ≤ 60 °C/W con ≥ 4 cm² → T_J = 60 + 49 = **109 °C** | ✔ (< 125 °C; TSD 165 °C) |
| Disipación con USB a 5,25 V | (5,25 − 0,03 − 3,3) × 0,45 = 0,86 W → T_J = 112 °C | ✔ |
| Pico de Wi-Fi (95 → 355 mA) | TLV Fig. 6-16 (1 → 500 mA con 10 µF): caída ≈ 40 mV (lectura de la figura, típica); aquí hay ≈ 25 µF | VDD ≥ 3,211 − 0,04 = **3,17 V ≥ 3,0 V** ✔ (margen 0,17 V) |

**Conclusión:** el TLV1117LV de `alimentacion.md` cumple ALI-07 con este bloque y no se cambia. La caída transitoria del pico de Wi-Fi no cuenta en el ± 3 % de §6, que es la regulación en continua.

## 9. Tabla de GPIO de la placa (MCU-05)

### 9.1 Criterios

Datos: S tabla 2-1 (pp. 16-17), tabla 2-2 (pp. 18-19) y §4.2.2.1 (p. 59); HDG tablas 9-12 (pp. 15-19).

1. **Analógicas solo en ADC1, GPIO1–10.** ADC2 no funciona con el Wi-Fi activo (S §4.2.2.1, p. 59).
2. **Salidas (IN, DEN, LIM_EN):** solo en pines que, desde el reset hasta que arranca el firmware, estén en alta impedancia sin *pull-up* o en nivel bajo. Se excluyen:
   - los pines de arranque 0, 3, 45 y 46 (MCU-05);
   - **GPIO18**, con un pulso alto de 60 µs al arrancar (S tabla 2-2, p. 19);
   - **GPIO39** (MTCK), con *pull-up* débil tras el reset (S tabla 2-1, nota 7);
   - **GPIO40** (MTDO), que la ROM pone a nivel alto en el modo de descarga USB-OTG (HDG tabla 12, p. 19);
   - **GPIO43** (TXD0), activo en el arranque, y **GPIO44** (RXD0), con *pull-up*.
3. **GPIO1–17:** solo tienen pulsos **bajos** de 60 µs (S tabla 2-2), que no activan nada con lógica activa a nivel alto.
4. **GPIO19/20:** reservados al USB (MCU-03). GPIO35–37 se usan porque no hay PSRAM octal (§2).
5. **Pines restringidos (18, 39, 40):** solo como entradas, señales de drenador abierto con *pull-up* o el LED (§7).

Pines disponibles: hay 36 GPIO (0–21 y 35–48). Sin los 8 reservados (0, 3, 19, 20, 43, 44, 45 y 46) quedan **28**. Se usan **25**.

### 9.2 Asignación (variante A: DEN común, fijada por DEC-0007)

Estado: **Z** = alta impedancia, sin *pull* interno · **WPU/WPD** = *pull-up* o *pull-down* interno de ≈ 45 kΩ · **L↓** = pulso bajo de 60 µs al arrancar · **H↑** = pulso alto. «Flasheo» es el modo de descarga de la ROM, por USB-Serial/JTAG o por UART.

| GPIO | Pin del módulo | Señal | Bloque | Dir. | ADC1 | Reset (EN bajo) y arranque | Flasheo | Elemento externo |
|---|---|---|---|---|---|---|---|---|
| 0 | 27 | BOOT | MCU | E | — | WPU (arranque) | Bajo con BOOT pulsado | R17 10 kΩ a +3V3, SW2 a GND |
| 1 | 39 | VIN_SENSE | Alimentación | A | CH0 | Z, L↓ | Z | R14/R15, C20 (`alimentacion.md` §3.10) |
| 2 | 38 | LIM_IMON | Alimentación | A | CH1 | Z, L↓ | Z | R4 10 kΩ, C5 100 nF |
| 3 | 15 | — (arranque, sin conectar) | — | — | (CH2) | Z | Z | Ninguno |
| 4 | 4 | IS1 | Salidas | A | CH3 | Z, L↓ | Z | R_SENSE 10 kΩ y *clamp* (REL-10) |
| 5 | 5 | IS2 | Salidas | A | CH4 | Z, L↓ | Z | ídem |
| 6 | 6 | IS3 | Salidas | A | CH5 | Z, L↓ | Z | ídem |
| 7 | 7 | IS4 | Salidas | A | CH6 | Z, L↓ | Z | ídem |
| 8 | 12 | IS5 | Salidas | A | CH7 | Z, L↓ | Z | ídem |
| 9 | 17 | IS6 | Salidas | A | CH8 | Z, L↓ | Z | ídem |
| 10 | 18 | — (libre; ADC1 de reserva) | — | — | CH9 | Z, L↓ | Z | — |
| 11 | 19 | IN1 | Salidas | S, activa alta | — | Z, L↓ | Z | R_IN 10 kΩ + **R_PD 100 kΩ** a GND |
| 12 | 20 | IN2 | Salidas | S | — | Z, L↓ | Z | ídem |
| 13 | 21 | IN3 | Salidas | S | — | Z, L↓ | Z | ídem |
| 14 | 22 | LIM_FLT | Alimentación | E, activa baja (drenador abierto) | — | Z, L↓ | Z | R6 10 kΩ a +3V3 |
| 15 | 8 | IN4 | Salidas | S | — | Z, L↓ | Z | R_IN + R_PD |
| 16 | 9 | IN5 | Salidas | S | — | Z, L↓ | Z | ídem |
| 17 | 10 | IN6 | Salidas | S | — | Z, L↓ | Z | ídem |
| 18 | 11 | — (libre; solo entrada) | — | — | — | Z, L↓ y **H↑** | Z | — |
| 19 | 13 | USB_D− | MCU | E/S | — | Z, pulsos | USB activo | R21 22 Ω, U6 |
| 20 | 14 | USB_D+ | MCU | E/S | — | *pull-up* del USB, pulsos | USB activo | R20 22 Ω, U6 |
| 21 | 23 | LIM_EN | Alimentación | S, activa alta | — | Z | Entrada (RCV) | **R5 10 kΩ** a GND |
| 35 | 28 | EXP_INT | Conectores | E (interrupción) | — | Z | Z | Según SPEC-0006 |
| 36 | 29 | EXP_IO2 | Conectores | E/S | — | Z | Z | Según SPEC-0006 |
| 37 | 30 | PULSE_IN | Conectores (EXP-01) | E (contador PCNT) | — | Z | Z | Acondicionamiento de EXP-01 (salida de 3,3 V) |
| 38 | 31 | OUT_DEN (común a los 6 canales) | Salidas | S, activa alta | — | Z | **Bajo** (VMO) | 6 × R_DEN 10 kΩ + **R_PD 100 kΩ** a GND |
| 39 | 32 | — (libre; solo entrada o drenador abierto) | — | — | — | Z → WPU | Bajo (VPO) | — |
| 40 | 33 | LED_STATUS | MCU | S | — | Z | **Alto** (OEN): LED encendido | R23 1 kΩ, D5 |
| 41 | 34 | I2C_SDA (placa: SHT4x) | Sensores | E/S (drenador abierto) | — | Z | Entrada | R24 4,7 kΩ a +3V3 |
| 42 | 35 | I2C_SCL (placa) | Sensores | S (drenador abierto) | — | Z | Entrada | R25 4,7 kΩ a +3V3 |
| 43 | 37 | UART_TX (TXD0) | MCU | S | — | WPU; mensajes de la ROM | TX activo | R22 470 Ω → J3-2 |
| 44 | 36 | UART_RX (RXD0) | MCU | E | — | WPU | RX activo | J3-3 |
| 45 | 26 | — (arranque VDD_SPI, sin conectar) | — | — | — | WPD | WPD | Ninguno; sin pistas |
| 46 | 16 | — (arranque, sin conectar) | — | — | — | WPD | WPD | Ninguno |
| 47 | 24 | I2C_EXP_SDA | Conectores | E/S (drenador abierto) | — | Z | Z | *Pull-up* y ESD según SPEC-0006 (2,2 kΩ provisional) |
| 48 | 25 | I2C_EXP_SCL | Conectores | S (drenador abierto) | — | Z | Z | ídem |

- Analógicas: 8 de los 9 canales de ADC1 sin GPIO3. Queda de reserva GPIO10 (ADC1_CH9).
- Libres: GPIO10 (cualquier uso), GPIO18 (solo entrada) y GPIO39 (entrada o drenador abierto).
- Atenuación del ADC: VIN_SENSE y LIM_IMON a 6 dB (`alimentacion.md`). La de IS la fija el bloque de salidas, con V_IS ≤ 3,1 V también en fallo (REL-10). Máximo del pin: VDD + 0,3 V (S tabla 5-4).
- **Dos buses I²C** (el ESP32-S3 tiene dos controladores):
  - un fallo, un corto o la capacidad del cable de expansión no bloquea el SHT4x (AMB-01);
  - cada bus lleva sus propias resistencias de *pull-up*.
- **Los números de GPIO de esta tabla son fijos para SPEC-0022 y para el YAML.** Si el layout pide permutarlos, se cambia antes este documento.

**Por qué un DEN común (DEC-0007 cambia el «IN, DEN e IS por canal» de la spec por «IN e IS por canal, DEN común»):**

- Con un IS por canal en su propio ADC1, el DEN por canal no aporta diagnóstico. El BTT6050 deja IS en alta impedancia con DEN bajo y da la corriente del canal o I_IS(FAULT) con DEN alto (BTT §7.2, tabla 8, p. 24). Con todos los DEN altos, cada ADC lee su canal sin interferencias.
- La carga abierta en OFF (con R_OL y el bus habilitado) se lee igual canal a canal.
- El reinicio tras un enclavamiento térmico lo hace IN, no DEN (BTT §6.5.2, p. 21: «*Only the IN pin signal toggling can re-activate the power stage*»).
- Ahorra 5 GPIO y deja 3 libres para EXP-02, que SPEC-0006 todavía no ha cerrado. Con un DEN por canal no queda ninguno (§9.3).
- Carga del GPIO38: 6 × I_DEN(H) ≤ 25 µA (BTT tabla 10, p. 34) + 33 µA de R_PD = 183 µA. La caída de V_OH es despreciable (I_OH típ. 40 mA con V_OH ≥ 2,64 V). V_DEN ≥ 2,64 − 25 µA × 10 kΩ = 2,39 V ≥ V_DEN(H) mín. 2,0 V ✔.
- Con la segunda fuente BTT6030-2ERA (DEN por *chip*, DSEL e IS compartidos por pareja; `estudio-salidas.md` §11.4), el DEN común sigue valiendo. Habría que cambiar 3 IS por 3 DSEL, y eso es otro *routing* (otra spec).

### 9.3 Variante B (un DEN por canal; descartada por DEC-0007)

Cumple REL-04 (ningún pin tiene WPU ni pulso alto) y cabe, pero ocupa 28 de 28 pines y limita la expansión:

| Cambio respecto a la variante A | GPIO |
|---|---|
| DEN1–DEN6 | 38, 10, 35, 36, 47 y 48 |
| Un solo bus I²C para el SHT4x y la expansión | 41 y 42 |
| EXP_INT (drenador abierto) | 39 |
| EXP_IO2, **solo entrada** (pulso alto al arrancar) | 18 |
| Libres | Ninguno (GPIO3, solo como entrada, sin usar) |

Coste: 5 × R_PD y 5 × R_DEN más, el bus I²C de la placa expuesto al cable de expansión y ningún pin para lo que pida SPEC-0006. **Descartada.**

## 10. Estado seguro durante el arranque, el reset y el flasheo (REL-04)

### 10.1 Pines de control

| Fase | Estado de IN1–6, OUT_DEN y LIM_EN | Fuente |
|---|---|---|
| Sin 3,3 V, o 3,3 V subiendo con EN bajo | *Chip* apagado; pines sin excitar. Los fija la R_PD | §5.1 |
| Reset (EN bajo, pulsador o RC) | Z sin *pull* (columna «*At Reset*») | S tabla 2-1, pp. 16-17 |
| Encendido | GPIO11–17: pulso **bajo** de 60 µs; GPIO21 y 38: sin pulsos | S tabla 2-2, pp. 18-19 |
| ROM y muestreo de los pines de arranque (t_H 3 ms) | Z («*After Reset*»: solo IE) | S tabla 2-1 |
| Flasheo (descarga por USB o UART) | La ROM no configura estos pines. Con USB-OTG: GPIO38 **bajo**, GPIO21 entrada | HDG tabla 12, p. 19 |
| *Bootloader* y arranque de ESPHome | Z hasta que ESPHome los configura con `restore_mode: ALWAYS_OFF` | Anexo B |
| *Brown-out*, *watchdog* de sistema, reset por USB | Reset del sistema → como «Reset» | — |
| OTA y `esp_restart()` (reset de CPU) | **Los registros de GPIO pueden conservar el nivel hasta que la aplicación los reconfigura.** Lo cubre el firmware: todo a bajo en `ota: on_begin` y en `on_shutdown` (Anexo B) | Interpretación del autor; se comprueba en el prototipo |

Hay dos barreras independientes. Con LIM_EN bajo, el bus de las salidas está apagado aunque un IN subiera. Con JP1 cerrado (sin limitador, DEC-0006) solo queda la R_PD de cada IN (`alimentacion.md` §3.13.9).

### 10.2 *Pull-downs* que exige REL-04

Van en el bloque que corresponde. Aquí se fijan el valor y la condición.

| Red | Resistencia | Bloque | Cálculo |
|---|---|---|---|
| IN1…IN6 | R_PD = 100 kΩ 1 % (C25803) del GPIO a GND, en el lado del GPIO de R_IN (10 kΩ) | Salidas | Pin en Z: fuga del GPIO ≤ 50 nA (S tabla 5-4) × 100 kΩ = **5 mV** ≪ V_IN(L) 0,8 V (BTT tabla 10, p. 34). El BTT añade una corriente interna a GND de ≥ 1 µA. Con el GPIO alto: V_IN ≥ 2,64 − 25 µA × 10 kΩ = **2,39 V** ≥ V_IN(H) 2,0 V (margen 0,39 V; con VDD = 3,211 V: 2,32 V) |
| OUT_DEN | R_PD = 100 kΩ, una sola | Salidas | ídem; 2,39 V con 6 entradas DEN (§9.2) |
| LIM_EN | R5 = 10 kΩ (existente) | Alimentación | 0,1 V con los 10 µA de SHDN < 0,8 V (`alimentacion.md` §3.13.5) |

- Ninguna de estas redes va a un pin con *pull-up* interno ni con pulso alto (§9.1). Con el WPU de 45 kΩ de GPIO39 y 100 kΩ a GND quedarían 2,28 V > 2,0 V: por eso se excluye GPIO39.

## 11. Lista de piezas

Referencias provisionales: siguen a las de `alimentacion.md` sin chocar con ellas (allí las mayores son C22, R15, D4, J1, U4, JP1, TP5, L1, Q1 y F1) y las fija la anotación de SPEC-0022. En este documento «D5» es el LED de estado; la decisión de la caja se escribe «decisión D5». Símbolos y huellas oficiales de KiCad 10.

| Ref. | Valor / función | Encapsulado | MPN principal | LCSC · stock | Alternativa (LCSC) | Símbolo / huella |
|---|---|---|---|---|---|---|
| U5 | Módulo ESP32-S3, 8 MB | SMD 18 × 25,5 | Espressif ESP32-S3-WROOM-1-N8 | C2913198 · 3 277 | ESP32-S3-WROOM-1-N16 (C2913199 · 1 985) | `RF_Module:ESP32-S3-WROOM-1` / `RF_Module:ESP32-S3-WROOM-1` (con el *keepout*) |
| C24 | 22 µF 25 V X5R | 0805 | Samsung CL21A226MAQNNNE | C45783 · 125 600 | — | `Device:C` / `Capacitor_SMD:C_0805_2012Metric` |
| C25 | 100 nF 50 V X7R | 0603 | Yageo CC0603KRX7R9BB104 | C14663 · **Basic** (36,1 M según SPEC-0018; stock LCSC 0 el 2026-11-06, lo confirma jr-conformidad en JLCPCB) | Samsung CL10B104KB8NNNC (C1591 · Extended) | `Device:C` / `C_0603_1608Metric` |
| R16 | EN, 10 kΩ 1 % | 0603 | UNI-ROYAL 0603WAF1002T5E | C25804 · 4,59 M | Yageo RC0603FR-0710KL (C98220) | `Device:R` / `R_0603_1608Metric` |
| C23 | EN, 1 µF 16 V X7R | 0603 | Yageo CC0603KRX7R7BB105 | C106248 · 538 550 | — | `Device:C` / `C_0603` |
| SW1, SW2 | RESET y BOOT, pulsador SPST 5,1 × 5,1 | SMD-4P | XKB TS-1187A-B-A-B | C318884 · 726 320 | XKB TS-1187A-C-E-B (C318887 · 82 760, misma huella) | `Switch:SW_Push` / `Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A` (**sin modelo 3D en KiCad 10.0**) |
| R17 | *Pull-up* de GPIO0, 10 kΩ | 0603 | 0603WAF1002T5E | C25804 | — | `R_0603` |
| J2 | USB-C 2.0, 16 pines | SMD | HRO TYPE-C-31-M-12 | C165948 · 136 905 | TYPE-C-31-M-12A (C5337088 · 2 405; confirmar la huella) | `Connector:USB_C_Receptacle_USB2.0_16P` / `Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12` (3D de respaldo, ficha) |
| U6 | ESD del USB | SOT-23-6 | ST USBLC6-2SC6 | C7519 · 26 240 | UMW USBLC6-2SC6 (C2687116 · 97 240) | `Power_Protection:USBLC6-2SC6` / `Package_TO_SOT_SMD:SOT-23-6` |
| R18, R19 | CC, 5,1 kΩ 1 % | 0603 | 0603WAF5101T5E | C23186 · 15,4 M | — | `R_0603` |
| R20, R21 | Serie en D+/D−, 22 Ω 1 % | 0603 | 0603WAF220JT5E | C23345 · 2,62 M | — | `R_0603` |
| C26 | VBUS, 4,7 µF 16 V X5R | 0603 | Samsung CL10A475KO8NNNC | C19666 · 1,23 M | — | `C_0603` |
| J3 | UART, tira 1 × 4 a 2,54 mm (THT) | THT | Ckmtw B-2100S04P-A110 | C124378 · 97 840 | BOOMELE 2.54-1*40P cortada (C2337) | `Connector_Generic:Conn_01x04` / `Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical` |
| R22 | Serie en TXD0, 470 Ω 1 % | 0603 | 0603WAF4700T5E | C23179 · 1,59 M | — | `R_0603` |
| D5 | LED de estado, verde-amarillo | 0603 | Hubei KENTO KT-0603YG | C2289 · 38 650 | KT-0603Y amarillo (C2287 · 92 500) | `Device:LED` / `LED_SMD:LED_0603_1608Metric` |
| R23 | LED, 1 kΩ 1 % | 0603 | 0603WAF1001T5E | C21190 · 2,59 M | — | `R_0603` |
| R24, R25 | *Pull-ups* del I²C de la placa, 4,7 kΩ 1 % | 0603 | 0603WAF4701T5E | C23162 · 4,11 M | — | `R_0603` |

- **Fuera de esta hoja, pero fijadas aquí:**
  - R_PD de 100 kΩ (C25803) en IN1…6 y OUT_DEN: bloque de salidas (§10.2);
  - *pull-ups* del I²C de expansión (2,2 kΩ, C4190, provisional), ESD y *pull-up* de EXP_INT: bloque de conectores, tras SPEC-0006.
- **Cálculo de los *pull-ups* del I²C de la placa:**
  - R ≥ (3,3 − 0,4 V)/3 mA = 0,97 kΩ;
  - con C_bus ≤ 50 pF (pista hasta el borde del SHT4x), t_r = 0,8473 × 4,7 k × 50 pF = 0,20 µs ≤ 0,3 µs (I²C rápido, 400 kHz) ✔.
- **Expansión (provisional):** 2,2 kΩ admiten hasta C ≤ 1 µs/(0,8473 × 2,2 k) = 536 pF a 100 kHz, con I_OL = 1,5 mA ≤ 3 mA ✔.
- **Piezas nuevas:**
  - ningún símbolo ni huella;
  - **modelo 3D del TS-1187A**: la huella oficial existe, pero falta su `.step` en `3dmodels/Button_Switch_SMD.3dshapes` de KiCad 10.0 (FAB-11);
  - el 3D del USB-C ya tiene respaldo (ficha).
- **Fichas:** existen las de ESP32-S3-WROOM-1 (hay que fijar la variante N8 y la nota de la antena), USBLC6-2SC6 y TYPE-C-31-M-12. Faltan las del TS-1187A-B-A-B, el KT-0603YG y la tira B-2100S04P-A110 (Anexo A).
- **Coste orientativo** (tramo de la cantidad real, sin los cargos de montaje de piezas *extended*):
  - **5,61 $ por placa con 5 placas** (módulo 4,91 $);
  - **4,93 $ con 10 placas** (módulo 4,23 $).
  - El mínimo de compra de los pasivos lo ajusta jr-conformidad.

## 12. Restricciones de layout

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| Antena de U5 | — | — | Zona libre en **todas las capas** (*keepout* de la huella oficial, 21 × 48 mm, o placa recortada) | U5 en una esquina, con la antena sobresaliendo del borde **lateral** y el punto de alimentación hacia la esquina (HDG Fig. 24/26, pp. 30-31). Objetivo del autor (no es requisito de la HDG): ≥ 15 mm entre el área de la antena y el buck (SW, L1), los *high-side* y sus pistas, el USB, la UART y el SHT4x; el *floorplan* puede justificar menos | MCU-02. Cosido de GND junto a la antena, fuera de la zona. ≥ 15 mm libres en la caja (HDG p. 30; decisión D5). Si sobresale ≈ 6 mm, se revisa FAB-08 en el *floorplan* |
| +3V3 → U5 pin 2 | 0,45 A (pico 0,5 A) | 0,5 mm | 0,2 mm | C24 y C25 a ≤ 3 mm del pin 2, con la vía de GND junto a ellos | — |
| GND de U5 (pines 1, 40 y EPAD 41) | 0,45 A | Plano | — | EPAD con ≥ 9 vías al plano (pad de la huella oficial) | Poca pasta en el EPAD (WROOM-1 p. 41) |
| EN (U5-3, R16, C23, SW1) | µA | 0,25 mm | 0,2 mm | C23 y R16 junto al pin 3; pista de EN lo más corta posible (HDG p. 8) | Lejos de SW del buck y de la antena |
| GPIO0 (R17, SW2) | µA | 0,25 mm | 0,2 mm | R17 junto al módulo | Sin condensadores en GPIO0 |
| USB_D+ / USB_D− (J2 → U6 → R20/R21 → GPIO20/19) | mA | Par diferencial de 90 Ω ± 10 % si es viable en 2 capas; si no, 0,25–0,3 mm, en paralelo y con la misma longitud (± 1 mm) | 0,2 mm dentro del par; ≥ 0,5 mm a otras señales | U6 a ≤ 5 mm de J2; R20/R21 junto a U5; recorrido corto (≤ 40 mm), sin vías y con plano de GND continuo debajo (HDG §1.4.8, p. 30) | 12 Mb/s: la impedancia no es crítica con ese recorrido. Lejos de la antena |
| VBUS (J2 → U6-5 → C26 → U3 VIN2) | 0,75 A (0,5 A solo con la lógica; 0,75 A con la expansión) | 0,6 mm (`Power`) | 0,2 mm | C26 junto a J2; VBUS hasta el TPS2116 (hoja de alimentación) | Misma restricción en `alimentacion.md` §8 |
| CC1, CC2 (R18, R19) | µA | 0,25 mm | 0,2 mm | Junto a J2 | — |
| SHIELD de J2 | ESD | Pestañas a GND con vías | — | J2 en el borde lateral, accesible desde fuera (FAB-07) | Lejos de la antena |
| UART (TXD0/RXD0 → J3) | mA | 0,25 mm | 0,2 mm | R22 junto al módulo; J3 lejos de la antena (HDG p. 28) | Rodeadas de GND con vías (HDG §1.4.6) |
| VIN_SENSE, LIM_IMON, IS1–IS6 | µA | 0,25 mm | 0,2 mm (≥ 0,6 mm en el lado de 24 V de los divisores) | Condensadores del ADC junto al pin del módulo | Lejos de SW, L1 y las salidas; sin cortes del plano debajo (FAB-04) |
| IN1–IN6, OUT_DEN, LIM_EN | µA | 0,25 mm | 0,2 mm | R_PD en el lado del GPIO; R_IN y R_DEN junto al *high-side* (BTT §6.4, p. 19) | Sin restricciones de impedancia |
| I2C_SDA/SCL (placa) | mA | 0,25 mm | 0,2 mm | R24/R25 junto al módulo; pista hasta el SHT4x por el puente entre las ranuras de AMB-02 | Pistas estrechas por el puente térmico (AMB-02) |
| I2C_EXP, EXP_INT, EXP_IO2, PULSE_IN | mA | 0,25 mm | 0,2 mm | Hasta el borde inferior (FAB-07); ESD junto al conector (bloque de conectores) | — |
| LED_STATUS (R23, D5) | 1,4 mA | 0,25 mm | 0,2 mm | D5 visible desde la cara superior | — |
| GPIO3, 45 y 46 | — | — | — | Sin pistas ni piezas | Pines de arranque sin conectar (§5.2) |

## 13. Trazabilidad

| Requisito | Pieza o cálculo | Sección |
|---|---|---|
| MCU-01 | U5 ESP32-S3-WROOM-1-N8, −40…85 °C, sin PSRAM (WROOM-1 tabla 1-1, p. 3) | §2 |
| MCU-02 | Antena fuera del borde lateral, en una esquina; zona libre de la HDG Fig. 26; objetivo de ≥ 15 mm del buck y de las salidas (no es requisito de la HDG) | §3, §12 |
| MCU-03 | J2 + U6 USBLC6-2SC6 + R18/R19 5,1 kΩ; GPIO19/20 | §4 |
| MCU-04 | SW1 + R16/C23 (10 kΩ / 1 µF; EN ≤ 0,16·VDD con el raíl a 3,0 V); SW2 + R17 en GPIO0 | §5 |
| MCU-05 | Tabla de GPIO: 8 analógicas en ADC1 sin GPIO3; ninguna salida en los pines de arranque, en GPIO18/39/40/43/44 ni en GPIO19/20; GPIO35–37 en uso porque no hay PSRAM octal | §9 |
| MCU-06 | J3 (3V3, TX, RX, GND) + R22 | §6 |
| MCU-07 | D5 + R23 en GPIO40 | §7 |
| ALI-07 | TLV1117LV: 0,45 A / 1 A; margen de caída ≥ 0,37 V; T_J 109 °C; caída del pico de Wi-Fi ≈ 40 mV | §8 |
| REL-04 | Pines de control en Z o a nivel bajo en todas las fases; R_PD de 100 kΩ (≤ 5 mV); OTA y reinicios por firmware | §10 |
| REL-10 (pines) | IS1–IS6 en ADC1_CH3–CH8 con DEN común | §9.2 |
| AMB-01, EXP-01, EXP-02 (pines) | I²C de la placa (41/42); I²C de expansión (47/48), EXP_INT (35), EXP_IO2 (36); PULSE_IN (37) | §9.2 |

## 14. Riesgos y puntos abiertos

1. **DEN común:** cerrado por DEC-0007 (§9.2). La variante B (§9.3) queda descartada.
2. **EXP-02:** la tabla reserva I²C, EXP_INT y EXP_IO2, más 3 pines libres. SPEC-0006 puede pedir otros. Los *pull-ups* y la ESD de la expansión son provisionales.
3. **GPIO tras `esp_restart()` y OTA:** pueden conservar su nivel hasta que la aplicación los reconfigura. Se cubre en el firmware (Anexo B) y se prueba en §6 («Salidas… desactivados durante el reset y el flasheo»), haciendo también un OTA con un canal activo.
4. **Arranque con alimentación lenta o con cortes rápidos (§5.1):** sin supervisor. Prueba en el prototipo: cortar y reponer la fuente en < 50 ms, 20 veces; la placa tiene que arrancar siempre. Si falla, C23 = 2,2 µF o un supervisor de 2,9–3,0 V.
5. **Antena:** el lado del punto de alimentación y las cotas «Max 1/Max 2» se confirman con el modelo 3D y la Fig. 26. El módulo puede asomar ≈ 6 mm frente a FAB-08 (decisión D5, caja).
6. **Solo USB:** el 5 V de la expansión (0,30 A) supera lo que da un puerto USB 2.0 (§4).
7. Cerrado: SPEC-0018 pasó C10 a C28323 (Basic) y C15849 tiene hoy 211 050 en stock en LCSC (2026-11-06); C23 (EN) usa C106248 y no depende de él.

## Anexo A. Datos para las fichas nuevas (`hardware/componentes/`, fuera de la zona de ing-esquematicos)

| Ficha | MPN · fabricante | LCSC | Datasheet | Pinout | Símbolo / huella / 3D |
|---|---|---|---|---|---|
| TS-1187A-B-A-B | TS-1187A-B-A-B · XKB Connection | C318884 (alt. C318887) | PDF de LCSC (C318884) | 4 pines: 1-2 y 3-4 unidos de dos en dos; SPST, 12 V, 50 mA, 160 gf, altura 1,5 mm | `Switch:SW_Push` / `Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A` / **3D que falta** |
| KT-0603YG | KT-0603YG · Hubei KENTO | C2289 (alt. C2287) | PDF de LCSC (C2289) | Ánodo / cátodo según la marca del PDF; V_F 2,0–2,2 V | `Device:LED` / `LED_0603_1608Metric` / oficial |
| B-2100S04P-A110 | B-2100S04P-A110 · Ckmtw | C124378 (alt. C2337) | PDF de LCSC (C124378) | 4 pines a 2,54 mm | `Conn_01x04` / `PinHeader_1x04_P2.54mm_Vertical` / oficial |
| ESP32-S3-WROOM-1 (actualizar) | Variante **N8** fija (C2913198); stock 3 277 a 2026-11-05 | — | WROOM-1 v1.8 | — | Añadir: antena según §3; GPIO35–37 en uso (no admite R8/R16V) |

## Anexo B. Notas para el firmware (FW-01…FW-04)

- Pines: tabla de §9.2. Cuando la hoja exista, el YAML se deriva del esquema (FW-02).
- **REL-04:**
  - IN1–6, OUT_DEN y LIM_EN como `output` con `restore_mode: ALWAYS_OFF`;
  - `on_boot` con prioridad alta que los fije a bajo;
  - `ota: on_begin` y `on_shutdown`: apagar IN1–6, OUT_DEN y LIM_EN.
- **ADC:**
  - VIN_SENSE y LIM_IMON a 6 dB (`alimentacion.md` Anexo B);
  - IS1–IS6, según el bloque de salidas;
  - todos en ADC1, válidos con el Wi-Fi activo.
- **I²C:** `i2c` con dos buses: `bus_placa` (SDA 41, SCL 42, 400 kHz) para el SHT4x y `bus_exp` (SDA 47, SCL 48, 100 kHz). Calentador del SHT4x apagado.
- **Contadores:** `pulse_counter` en GPIO37 (EXP-01). EXP_INT en GPIO35, como `binary_sensor` o como interrupción del expansor.
- `status_led` en GPIO40.
- Con VIN_SENSE < 5 V, la placa está alimentada solo por USB: avisar y no accionar salidas (ALI-08).

## Anexo C. Etiquetas jerárquicas de la hoja MCU (para SPEC-0022)

| Etiqueta | Dirección (vista desde la hoja MCU) | Hoja de destino |
|---|---|---|
| VBUS | Salida | Alimentación (U3 VIN2) |
| VIN_SENSE, LIM_IMON, LIM_FLT | Entrada | Alimentación |
| LIM_EN | Salida | Alimentación |
| IN1…IN6, OUT_DEN | Salida | Salidas |
| IS1…IS6 | Entrada | Salidas |
| I2C_SDA, I2C_SCL | Bidireccional | Sensores |
| I2C_EXP_SDA, I2C_EXP_SCL, EXP_INT, EXP_IO2, PULSE_IN | Bidireccional / entrada | Conectores |
| +3V3, GND | Símbolos de alimentación | Global |
