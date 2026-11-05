# Bloque de alimentación: piezas, campos y *derating* (SPEC-0018)

Consulta de LCSC/JLCPCB: **2026-11-05**, API `selectSmtComponentList` de JLCPCB (stock de montaje, tipo y precio a 1 ud.). Fuente de la lista: `docs/diseno/alimentacion.md` §7. Los campos de los esquemas (`LCSC Part#`, `MPN`, `Datasheet`, `Description`) salen de esta tabla cuando SPEC-0019 coloque las piezas. Datasheets de pasivos: la página de LCSC `https://www.lcsc.com/product-detail/<código>.html` (no hay PDF de fabricante en la API).

## 1. Piezas activas y mecánicas

| Ref. | MPN | Fabricante | LCSC | Tipo · stock | Símbolo / huella (3D) | Ficha |
|---|---|---|---|---|---|---|
| J1 | WJ500V-5.08-2P | Kangnex | C8465 | Extended · 283 190 | `Connector:Screw_Terminal_01x02` / `esp-riego:TerminalBlock_Kangnex_WJ500V-5.08-2P_1x02_P5.08mm_Horizontal` (propio) | `WJ500V-5.08-2P.md` |
| F1 | 0451010.MRL | Littelfuse | C44479 | Extended · 22 770 | `Device:Fuse` / `esp-riego:Fuse_Littelfuse-NANO2-451_453` (3D propio) | `0451010.MRL.md` |
| Q1 | SQD50P06-15L_GE3 | Vishay | C3281500 | Extended · 5 744 | `Transistor_FET:SUD50P06-15` / `Package_TO_SOT_SMD:TO-252-2` (oficial) | `SQD50P06-15L.md` |
| D1 | BZT52C15 | MDD | C173427 | Extended · 148 099 | `Device:D_Zener` / `Diode_SMD:D_SOD-123` | `BZT52C15.md` |
| D2 | SMBJ33A | Littelfuse | C224019 | Extended · 9 670 | `Device:D_TVS` / `Diode_SMD:D_SMB` | `SMBJ33A.md` |
| D3 | SS310 | MDD | C15874 | Extended · 348 658 | `Device:D_Schottky` / `Diode_SMD:D_SMA` | `SS310.md` |
| D4 | KT-0603R | Hubei KENTO | C2286 | **Basic** · 6 683 182 | `Device:LED` / `LED_SMD:LED_0603_1608Metric` | — |
| U1 | TPS26632RGER | TI | C1850278 | Extended · 1 631 | `Power_Management:TPS26632RGE` / `Package_DFN_QFN:Texas_RGE0024H_…_ThermalVias` | `TPS2663.md` |
| U2 | LMR36520FADDAR | TI | C1858395 | Extended · 8 000 | `esp-riego:LMR36520FADDA` (nuevo) / `Package_SO:Texas_HTSOP-8-1EP_…_ThermalVias` | `LMR36520.md` |
| U3 | TPS2116DRLR | TI | C3235557 | Extended · 54 421 | `Power_Management:TPS2116DRL` / `Package_TO_SOT_SMD:SOT-583-8` | `TPS2116.md` |
| U4 | TLV1117LV33DCYR | TI | C15578 | Extended · 1 606 | `Regulator_Linear:TLV1117-33` / `Package_TO_SOT_SMD:SOT-223-3_TabPin2` | `TLV1117LV.md` |
| L1 | FXL0650-100-M | cjiang | C475521 | Extended · 38 857 | `Device:L` / `Inductor_SMD:L_Changjiang_FXL0650` | `FXL0650-100-M.md` |
| JP1 | — (sin pieza) | — | — | fuera de BOM y CPL | `Jumper:SolderJumper_2_Open` / `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` (nueva, sin 3D) | — |
| TP1–TP5 | — (sin pieza) | — | — | fuera de BOM y CPL | `Connector:TestPoint` / `TestPoint:TestPoint_Pad_D2.0mm`; TP4: `TestPoint_THTPad_D2.0mm_Drill1.0mm` (sin 3D) | — |

Alternativas con stock (consulta 2026-11-05): TLC TA10 C2998199 (1 461); UMW SUD50P06-15 C7503186 (51 103); Ruilon SMBJ33A C10219 (11 938); LMR36520ADDAR C2879422 (6 117); JSMSEMI TLV1117LV33DCYR C48937499 (76 870); TPS26633RGER C1850275 (12); XL-1608SURC-06 C965799 (7 479 588); Diodes BZT52C15-7-F C177014 (52 710); UMW SS310A C2988628 (4 731); FXLA0630-100M C5372143 (1 545).

## 2. Pasivos

| Refs. | Valor | MPN | Fabricante | LCSC | Tipo · stock |
|---|---|---|---|---|---|
| R1, R9, R12 | 100 kΩ 1 % | 0603WAF1003T5E | UNI-ROYAL | C25803 | Basic · 16 435 345 |
| R2 | 4,30 kΩ 1 % 100 ppm | 0603WAF4301T5E | UNI-ROYAL | C23159 | Extended (preferente) · 252 613 |
| R3, R4, R5, R6, R10 | 10 kΩ 1 % | 0603WAF1002T5E | UNI-ROYAL | C25804 | Basic · 43 742 372 |
| R7, R14 | 100 kΩ 0,1 % 25 ppm | RT0603BRD07100KL | Yageo | C122538 | Extended · 1 963 953 |
| R8 | 24,9 kΩ 0,1 % 25 ppm | AR03BTCX2492 | Viking | C4156365 | Extended · **774** |
| R11 | 330 kΩ 1 % | 0603WAF3303T5E | UNI-ROYAL | C23137 | Basic · 708 868 |
| R13 | 1 kΩ 1 % | 0603WAF1001T5E | UNI-ROYAL | C21190 | Basic · 27 942 044 |
| R15 | 4,87 kΩ 0,1 % 25 ppm | AT0603BRD074K87L | Yageo | C855888 | Extended · 4 056 |
| C1 | 47 µF 63 V electrolítico | MVK 63V47 M 8*10 | SamYoung | C165628 | Extended · 802 |
| C2, C6, C7 | 4,7 µF 100 V X7R 1210 | FS32X475K101EGG | PSA | C381466 | Extended · 54 967 |
| C3 | 100 nF 100 V X7R 0603 | CL10B104KC8NNNC | Samsung | C15725 | Extended · 363 813 |
| C4 | 22 nF 50 V X7R 0603 | CL10B223KB8NNNC | Samsung | C21122 | **Basic** · 846 818 |
| C5, C9, C13, C14, C20, C21 | 100 nF 50 V X7R 0603 | CL10B104KB8NNNC | Samsung | C1591 | Extended · 3 579 949 |
| C8 | 220 nF 100 V X7R 0805 | CC0805KKX7R0BB224 | Yageo | C513710 | Extended · 72 257 |
| C10, C15 | 1 µF 50 V X5R 0603 | CL10A105KB8NNNC | Samsung | C15849 | **Basic** · 11 489 595 |
| C11, C12, C16, C17 | 22 µF 25 V X5R 1206 | CL31A226KAHNNNE | Samsung | C12891 | **Basic** · 1 613 044 |
| C18, C19 | 10 µF 10 V X5R 0603 | CL10A106KP8NNNC | Samsung | C19702 | **Basic** · 10 377 360 |

Símbolos `Device:R`, `Device:C`, `Device:C_Polarized` y `Device:LED`; huellas `R_0603_1608Metric`, `C_0603_1608Metric`, `C_0805_2012Metric`, `C_1206_3216Metric`, `C_1210_3225Metric` y `CP_Elec_8x10` (todas oficiales, con 3D en la instalación). Cambios en cifras respecto a `alimentacion.md` §7: R8 774 (antes 760); R8 alternativa Yageo C861775 pasa de stock 0 a 21 858 (es de 50 ppm); C2998199 1 461.

**Piezas Extended distintas del bloque: 20** (cada una puede llevar el cargo de pieza extendida de JLCPCB); Basic: 9. Propuestas al coordinador, sin cambiar nada:
- R8: Yageo **RT0603BRD0724K9L** (C136967, 25 ppm, 0,1 %, misma serie que R7; stock 14 308; 0,0393 $) en lugar de Viking C4156365 (774).
- C5, C9, C13, C14, C20, C21: Yageo CC0603KRX7R9BB104 (C14663, 100 nF 50 V X7R, **Basic**, 36 130 321) en lugar de C1591 (Extended): una pieza Extended menos.

## 3. *Derating* DC y térmico de los cerámicos (VAL-0017-01-05)

Fuente: datos simulados por el fabricante en SimSurfing, `https://product.samsungsem.com/mlcc/<MPN sin la última letra>.do` (consulta 2026-11-05): curva de capacitancia frente a tensión DC (25 °C) y frente a temperatura. Son valores típicos, no garantizados. El criterio es la **suma** de la pérdida por tensión y la pérdida por temperatura al 0 V (más severo que el producto). La curva «con polarización» de SimSurfing solo está a una tensión fija (12,5 V en el 22 µF) y es casi plana con la temperatura, así que no sirve para 5 V. Tolerancia: K = ± 10 %.

| Refs. | Pieza (curva usada) | Polarización | ΔC por tensión | ΔC a 60 °C (suma) | ΔC a 85 °C (suma) | C efectiva por condensador (nominal · mín. con −10 %) |
|---|---|---|---|---|---|---|
| C11, C12, C16, C17 | CL31A226KAHNNN (22 µF 25 V X5R 1206) | 5,0 V / 5,107 V | −38,0 % / −38,9 % | −39,0 % | −46,2 % | 13,4 µF · 12,1 µF (25 y 60 °C); 11,8 · 10,6 µF (85 °C) |
| C10, C15 | CL10A105KB8NNN (1 µF 50 V X5R 0603) | 5 V | −34,4 % | −35,8 % | −42,9 % | 0,64 µF a 60 °C; 0,57 µF a 85 °C |
| C18, C19 | CL10A106KP8NNN (10 µF 10 V X5R 0603) | 3,3 V | −55,7 % | −63,4 % | −70,4 % | 3,7 µF · 3,3 µF a 60 °C; 3,0 · 2,7 µF a 85 °C |
| C2, C6, C7 | **Proxy** Samsung CL32B475KCJZ4N (4,7 µF 100 V X7R 1210; el PSA FS32X475K101EGG no publica curva) | 24 V / 30 V | −24,5 % / −33,4 % | −27,6 % / −36,5 % | −31,2 % / −40,1 % | 3,4 µF / 3,0 µF a 60 °C. Con el proxy KCIZNW: 3,2 / 2,7 µF |
| C8 | Proxy CL21B224KCFSFN (220 nF 100 V X7R 0805) | 24 V / 30 V | −22,3 % / −31,1 % | −22,8 % / −31,6 % | −25 % / −33,8 % | 0,17 / 0,15 µF a 60 °C |
| C3 | CL10B104KC8NNN (100 nF 100 V X7R 0603) | 24 V / 30 V | −25,5 % / −35,4 % | −28,4 % / −38,3 % | −31,8 % / −41,7 % | 72 / 62 nF a 60 °C |
| C5, C9, C13, C14, C20, C21 | CL10B104KB8NNN (100 nF 50 V X7R) | ≤ 5 V | + 0,2 % | −2,7 % | −6,1 % | ≈ 97 nF: sin efecto |

Consecuencias, frente a `docs/diseno/alimentacion.md`:

1. **C11/C12 y C16/C17 (prioridad):** 2 × 13,4 = **26,8 µF** efectivos a 5,1 V y 60 °C (24,2 µF con −10 %; 21,3 µF a 85 °C), frente a los ≈ 28 µF de §3.13.4. La caída del +5V durante el *fast-trip* pasa de 0,12 V a 0,14 V con el mínimo (0,75 A × 4,5 µs / 24,2 µF). La conclusión no cambia. La Tabla 8-1 del LMR36520 (p. 18) da 2 × 22 µF de capacitancia **nominal** (4 × 10 µF como mínimo compacto), así que el diseño cumple la tabla; la nota de la p. 17 dice que el resto de valores del datasheet son efectivos.
2. **C16/C17 frente a TPS2116:** 26,8 µF efectivos frente a los ≈ 100 µF que sugiere el datasheet con bloqueo inverso e inductancia (p. 11). Refuerza el punto 6 de §10; sin cambios en el diseño.
3. **C7 como CIN de U2:** el datasheet pide ≥ 4,7 µF cerámicos a la entrada (p. 20) y, según su nota (p. 17), efectivos. **C7 solo da 3,0–3,4 µF a 24–30 V**: no llega. Con C2 (4,7 µF) también junto a VIN–PGND, el total es 6–7 µF y cumple. Propuesta (ing-esquematicos): C2 y C7 pegados a U2, o un segundo 4,7 µF de 100 V, y reflejarlo en §8.
4. **C10 (CVCC):** 0,64 µF efectivos a 5 V y 60 °C frente al «1 µF, 16 V» de la p. 21. Funciona en las EVM de TI con valores nominales equivalentes, pero queda por debajo de lo literal. Opciones: 1 µF X7R de 25 V en 0805, o aceptar. Decisión de ing-esquematicos.
5. **C3 (IN_SYS de U1):** 62–72 nF efectivos a 24–30 V frente a «0,1 µF o más» del datasheet (ficha `TPS2663.md`). Propuesta: 220 nF 100 V X7R (como C8, 150–170 nF efectivos).
6. **C18/C19:** 3,7 µF efectivos a 60 °C frente a > 0,5 µF efectivos que exige el TLV1117LV en la salida (p. 13): cumple con margen 7×.
7. **C2/C6/C7 en §3.13.4:** 2 × 4,7 µF a 24 V dan 6,4–7,1 µF efectivos a 24 V y 60 °C (no 7,9 µF); no cambia la conclusión de §3.13.4, que no depende de esa cota.

## 4. Pendientes de SPEC-0017 resueltos

| Pendiente | Resultado |
|---|---|
| Pines de SUD50P06-15 frente a SQD50P06-15L | Coinciden: 1 G, 2 D, 3 S (+ pestaña a D); datasheet Vishay p. 1, símbolo, huella `TO-252-2` (pad 2 = pestaña) y datasheet UMW p. 1 |
| Pines de TLV1117-33 frente a TLV1117LV | Coinciden: 1 GND, 2 y pestaña OUT, 3 IN; datasheet TI p. 3 |
| Símbolo de LMR36520 | `esp-riego:LMR36520FADDA`, a partir de LMR36510ADDA (pines idénticos a la Tabla 5-1, p. 4) |
| Stock de R8 | 774 (C4156365). La alternativa Yageo C861775 tiene 21 858, pero es de 50 ppm |
| Datasheet del UMW SUD50P06-15 | Revisado (`SQD50P06-15L.md`); válido para Q1 |
| Huella de JP1 | `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` |
