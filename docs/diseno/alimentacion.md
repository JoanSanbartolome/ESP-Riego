# Bloque de alimentación: entrada, limitador y raíles (SPEC-0017)

**Estado:** propuesta para validación. **Autor:** ing-esquematicos · **Fecha:** 2026-11-05.
**Requisitos:** ALI-01…ALI-13, REL-04, REL-08 (parte del limitador), §6 de `docs/02` v0.4; DEC-0003, DEC-0004, DEC-0006 (UVLO a 13,5 V, coste del limitador y puente JP1); estudio de salidas S2–S4.
**Precios y stock:** LCSC, consulta del 2026-11-05 (`wmsc.lcsc.com/.../product/detail?productCode=…`). El tipo Basic/Extended y el stock de montaje los confirma jr-conformidad (SPEC-0018).

> Datasheets usados (revisión, descargados de ti.com, vishay.com vía LCSC, littelfuse.com vía LCSC y espressif.com; las páginas citadas son las del PDF):
> TPS2663 SLVSE94G (jun. 2024) · LMR36520 SNVSBF0C (nov. 2025) · TPS2116 SLVSFG1A (may. 2021) · TLV1117LV SBVS160C (ene. 2023) · SQD50P06-15L doc. 69098 rev. E (ago. 2012) · Littelfuse 451/453 (rev. 15/06/2017) · SMBJ (`hardware/componentes/datasheets/SMBJ33A.pdf`, 07/04/25) · ESP32-S3 Series Datasheet v2.2 · ESP32-S3-WROOM-1 v1.8 (`hardware/componentes/datasheets/`).

## 0. Resumen

```
J1 ─ F1 ─ Q1 (P-MOS, D→S) ─┬─ VIN_PROT ─┬─ U1 TPS26632 (limitador 4,19 A) ─ BUS_24V → salidas
borne 10 A    polaridad    D2 SMBJ33A   ├─ U2 LMR36520 (buck 5,0 V) ─ U3 TPS2116 VIN1 ┐
                           C1, C2       ├─ R14/R15 → VIN_SENSE (ADC1)   VBUS ─ VIN2 ─┴─ +5V ─ U4 TLV1117LV ─ +3V3
                                        └─ R9/R10 → EN de U2 (UVLO)
```

| Función | Pieza principal | Alternativa | Requisito |
|---|---|---|---|
| Borne de entrada | WJ500V-5.08-2P (C8465) | — (ficha existente) | ALI-02 |
| Fusible | Littelfuse 0451010.MRL, 10 A muy rápido, 125 V, 2410 (C44479) | TLC TA10 (C2998199) | ALI-04, ALI-12 |
| Polaridad | P-MOS SQD50P06-15L, 60 V, 15,5 mΩ, TO-252 (C3281500), con zéner de puerta BZT52C15 | UMW SUD50P06-15 (C7503186) | ALI-03 |
| TVS | SMBJ33A (C224019), tras Q1 | Ruilon SMBJ33A (C10219) | ALI-04 |
| Buck 5 V | LMR36520FADDAR, 65 V / 2 A síncrono (C1858395) | LMR36520ADDAR (C2879422) | ALI-05, ALI-06 |
| Unión USB / 5 V | Multiplexor TPS2116DRLR, prioridad al buck (C3235557) | — (ver §3.8) | ALI-08 |
| 3,3 V | LDO TLV1117LV33DCYR, 1 A (C15578) | JSMSEMI TLV1117LV33DCYR (C48937499) | ALI-07 |
| Limitador común | eFuse TPS26632RGER, 60 V, I_OL = 4,19 A ± 8,5 % (C1850278) | TPS26633RGER (C1850275, stock bajo) | ALI-12, ALI-13, REL-04 |
| Medida de VIN | Divisor 100 kΩ / 4,87 kΩ al 0,1 % → ADC1 a 6 dB | Viking ARG03BTC1003 para 100 kΩ | ALI-09 |
| LED | KT-0603R rojo + 1 kΩ en +3V3 (C2286) | XL-1608SURC-06 (C965799) | ALI-10 |
| Test points | Pads `TestPoint` (sin pieza) | Keystone 5000/5001 THT | ALI-11 |
| Puente de U1 | JP1, puente de soldadura de `VIN_PROT` a `BUS_24V` (sin pieza), abierto por defecto | — | DEC-0006 |

Resultados clave:

- **Banda del limitador:** 3,86–4,57 A (4,21 A −8,3 / +8,6 %; VAL-0017-01-02). Dentro de 3,5–4,9 A; con la lógica, 4,77 A < 5,14 A.
- **UVLO del buck:** arranque 12,50–14,56 V (nominal 13,54 V, **decidido en DEC-0006**); bajada ≤ 14,56 V. Con la caída de las protecciones: arranque ≤ 14,57 V ≤ 17 V y bajada ≤ 14,72 V ≤ 15,5 V.
- **Puente JP1 (DEC-0006):** cortocircuita U1 con estaño si U1 no se monta o falla. Pads de 3,0 mm de ancho para 4,9 A; abierto por defecto (§3.13.9).
- **Medida de VIN:** error ≤ ± 1,62 % a 17 V y ≤ ± 1,05 % a 31 V (≤ ± 3 %).
- **Nodo de entrada:** todas las piezas ≥ 60 V (Vc = 53,3 V; +10 % = 58,6 V).
- **Lógica:** 4,32 W en la entrada (≤ 4,8 W), con 0,45 A en 3,3 V y 0,30 A para el 5 V de la expansión.
- **Piezas nuevas:** el símbolo del LMR36520 (hay uno compatible pin a pin) y la huella del puente JP1 con pads de 3,0 mm (§3.13.9). Las demás huellas existen en las librerías oficiales de KiCad 10 (§7).

## 1. Datos de partida

| Dato | Valor | Origen |
|---|---|---|
| Fuente | LED de tensión constante, 24 V ± 2 % (ajuste de fábrica), 5 A, sobrecarga desde 126 W (≥ 5,14 A a 24,5 V), OVP 28,8–33,6 V (supuestos) | ALI-01, ALI-12, DEC-0004 |
| Rango en el borne | 18–30 V en funcionamiento | ALI-01 |
| Carga de salidas | 3,5 A instalados máx. (24,5 V, bobinas a −10 °C) | ALI-12 |
| Lógica | ≤ 4,8 W en la entrada | ALI-12 |
| Ambiente | −10…+50 °C; +10 °C dentro de la caja → **60 °C** para la térmica | §5, checklist de esquema |
| TVS | SMBJ33A: V_RWM 33 V; V_BR 36,7–40,6 V; Vc 53,3 V a 11,3 A | SMBJ33A.pdf, tabla p. 2 |
| Tensión mínima del nodo | Vc × 1,1 = **58,6 V** | ALI-05 |

## 2. Arquitectura y orden de las protecciones

1. **J1 → F1 → Q1 → nodo `VIN_PROT`**. El fusible va primero (protege también a Q1). Con polaridad invertida Q1 no conduce y F1 no actúa (§6, «Polaridad invertida a 30 V»).
2. **D2 (TVS unidireccional) en `VIN_PROT`, después de Q1** (ALI-04).
3. Del nodo `VIN_PROT` salen, en paralelo:
   - **U2 (buck)**, antes del limitador (ALI-13, DEC-0004, S2);
   - **U1 (limitador)** → `BUS_24V` → *high-side* (hoja de salidas);
   - el divisor de medida (ALI-09) y el divisor de UVLO de U2 (ALI-06).
4. **+5V** = salida de U3 (TPS2116): VIN1 = buck (prioritario), VIN2 = VBUS del USB-C.
5. **+3V3** = U4 desde +5V.

Descartado: usar el bloqueo inverso del TPS2663 (B_GATE con un N-MOS) como protección de polaridad común. Ese FET se apaga con SHDN y con el UVLO del limitador, y el buck quedaría alimentado por su diodo interno casi siempre (SLVSE94G §8.3.13, p. 28).

## 3. Selección y cálculos

### 3.1 Borne J1 (ALI-02)

WJ500V-5.08-2P: 2 polos a 5,08 mm, 15 A (UL) / 18 A (IEC), 300 V (`hardware/componentes/WJ500V-5.08-2P.md`). Con 5,1 A, la relación es 2,9× sobre UL. Polo 1 = +24 V y polo 2 = GND, en serigrafía (FAB-09).

### 3.2 Fusible F1 (ALI-04, ALI-12)

- Criterio: no actuar con 5,1 A continuos a 50 °C de ambiente (60 °C en la caja).
- Littelfuse recomienda trabajar al 75 % de la nominal, y aplicar además la curva de temperatura (451/453, p. 3, nota 1). La curva da ≈ 96 % a 60 °C (lectura de la figura).
- **0451010.MRL (10 A):** 10 × 0,75 × 0,96 = **7,2 A ≥ 5,1 A** (1,41×).
- Tensión: 125 V DC (tabla, p. 2) ≥ 58,6 V. Ruptura: 50 A a 125 V DC.
- Caída y disipación: R en frío 5,6 mΩ (tabla, p. 2); × 1,3 en caliente → 0,19 W a 5,1 A.
- Arranque en caliente (*hot-plug*), con C = 47 + 2 × 4,7 µF, 30 V y R ≈ 0,1 Ω (cable y ESR): I²t = C·V²/(2R) = 0,25 A²s, frente a I²t de fusión de 26,46 A²s (tabla, p. 2). No actúa.
- Papel: con la fuente de 5 A (que limita a 5,1–7,5 A), F1 solo actúa con una fuente de más corriente o con un corto franco aguas abajo (Q1 o D2 en corto). En el resto de casos limita primero la fuente o el limitador común.
- Huella: `Fuse:Fuse_Littelfuse-NANO2-451_453` (oficial).

### 3.3 Protección de polaridad Q1 (ALI-03)

P-MOS con el drenador hacia el borne y la fuente hacia `VIN_PROT`. R1 = 100 kΩ de la puerta a GND y D1 = BZT52C15 (cátodo en la fuente, ánodo en la puerta).

| Comprobación | Cálculo | Resultado |
|---|---|---|
| V_DS ≥ Vc + 10 % | V_DS = −60 V (p. 1) ≥ 58,6 V. Con polaridad invertida a 30 V, V_DS = −30 V; en directa, Q1 conduce y V_DS ≈ 0 | Cumple |
| V_GS ≤ ±20 V (p. 1) | D1: 14,25–15,75 V (LCSC C173427). Por debajo de ≈ 15 V, V_GS = −VIN; a 53,3 V, V_GS ≈ −15,75 V | Cumple (margen 4,25 V) |
| R_DS(on) con V_GS = −10 V | 15,5 mΩ máx. a 25 °C; 26 mΩ máx. a 125 °C (p. 2). Se calcula con 26 mΩ | — |
| V_GS en el UVLO de bajada | VIN ≥ 12,5 V → V_GS ≤ −12,5 V, más que los −10 V de la especificación | Cumple |
| Disipación a 5,1 A | 5,1² × 0,026 = 0,68 W; R_thJA = 50 °C/W con 1 in² de cobre (p. 1) → T_J = 60 + 34 = **94 °C** < 175 °C | Cumple |
| Corriente | I_D = −50 A (encapsulado), I_DM = −200 A (p. 1), frente a 5,1 A continuos y 11,3 A de pulso de la TVS | Cumple |
| R1, D1 | A 53,3 V: I = (53,3 − 15)/100 k = 0,38 mA; P_R1 = 14,7 mW; P_D1 = 5,7 mW. A 30 V: P_R1 = 2,3 mW | Cumple (0603, 0,1 W, 75 V) |

- Limitación aceptada: Q1 no está protegido contra transitorios **negativos** de más de ≈ 36 V en el borne, porque la TVS va detrás (ALI-04). Tiene E_AS = 135 mJ (p. 1).
- Alternativa: UMW SUD50P06-15 (60 V, 12 mΩ a −10 V según LCSC). Cuesta 0,36 $ a 5 uds., frente a 1,09 $ del Vishay. Hay que verificar su datasheet antes de usarla (SPEC-0018).

### 3.4 TVS D2 (ALI-04)

- **Unidireccional, después de Q1.** Con polaridad invertida no conduce, porque Q1 está cortado.
- V_RWM 33 V ≥ 30 V (máximo de ALI-01). V_BR mín. 36,7 V > OVP máx. de la fuente, 33,6 V.
- Vc 53,3 V a 11,3 A, 600 W 10/1000 µs (SMBJ33A.pdf, p. 1 y tabla de la p. 2).
- Fuga: 1 µA a V_RWM (despreciable).
- El aviso de sobretensión del firmware (31 V) queda por debajo de V_RWM (ALI-09).

### 3.5 Tensión nominal de las piezas del nodo de entrada (ALI-05)

Exigido: ≥ 58,6 V (53,3 V × 1,1).

| Pieza en `VIN_PROT` (o antes) | Tensión nominal | Fuente | ≥ 58,6 V |
|---|---|---|---|
| F1 0451010.MRL | 125 V | tabla, p. 2 | ✔ |
| Q1 SQD50P06-15L | 60 V | p. 1 | ✔ |
| U1 TPS26632 (IN, IN_SYS) | 60 V de funcionamiento; 67 V máx. absoluto | SLVSE94G §6.3 y §6.1, p. 5 | ✔ |
| U2 LMR36520 (VIN, EN) | 65 V de funcionamiento; 70 V máx. absoluto | SNVSBF0C §6.3 y §6.1, p. 5 | ✔ |
| C1 47 µF electrolítico | 63 V | LCSC C165628 | ✔ (7,5 % sobre 58,6 V) |
| C2, C3, C7 cerámicos X7R | 100 V | LCSC | ✔ |
| C8 220 nF X7R | 100 V | LCSC C513710 | ✔ |
| R9, R14, R1 (0603) | 75 V; la tensión que soportan a Vc es ≤ 50,8 V | LCSC | ✔ |
| J1 | 300 V | ficha | ✔ |

No se reduce el requisito: no hace falta justificar una Vc menor.

### 3.6 Buck U2: LMR36520FADDAR (ALI-05)

- **Elección:** síncrono, 65 V, 2 A, con compensación interna y EN de precisión (umbral −6 / +5,6 %). Sin diodo externo.
- Descartados:
  - **TPS54360B** (60 V, 3,5 A): necesita diodo de recuperación y compensación externa. Su EN con corrientes de histéresis (I_h 2,2–4,5 µA) deja solo 0,03–0,8 V de margen frente a ALI-06 (SNVSB93, tabla de características).
  - **LMR16030:** no síncrono y con EN de 1,05–1,38 V (SNVSAH9B).
- Variante FADDAR (FPWM): regulación sin la subida de PFM a baja carga (p. 14) y menor precio (0,92 $ a 10 uds.). La ADDAR es la alternativa con la misma huella.

| Parámetro | Cálculo | Valor |
|---|---|---|
| VOUT | VFB · (1 + RFBT/RFBB) = 1 · (1 + 100/24,9) | **5,016 V** |
| Tolerancia de VOUT | VFB ± 1,5 % (p. 6); RFBT y RFBB al 0,1 % y 25 ppm/°C: error del cociente 0,8 × (0,2 % + 2 × 25 ppm × 35 °C) = 0,30 % | 4,926–5,107 V |
| +5V tras U3 | − R_ON (≤ 60 mΩ, TPS2116 p. 6) × 0,75 A = −0,045 V | **4,881–5,107 V: −2,4 / +2,1 % (≤ ± 3 %, §6)** |
| Con resistencias al 1 % (descartado) | 4,862–5,174 V: ± 3,1 % | No cumple |
| L | Tabla 8-1 (p. 18): 10 µH. Ec. 4 (p. 19): ΔI = (VIN − VOUT)·VOUT/(VIN·f·L) = 0,83 A (15 V) / 0,99 A (24 V) / 1,04 A (30 V) / 1,13 A (53,3 V) | 10 µH |
| L mínima | M·VOUT/f = 0,42 × 5/400 kHz (ec. 5, p. 19) | 5,25 µH < 10 µH ✔ |
| I_sat de L | ≥ ISC máx. = 3,6 A (p. 6; recomendación de la p. 19) | FXL0650-100-M: I_sat 5,3 A, I_rms 4,5 A, DCR 60 mΩ ✔ |
| Corriente disponible | I_OUT,máx = ILIMIT,mín + ΔI/2 = 1,8 + 0,42 = 2,2 A (15 V); 2,3 A (30 V) (ec. 1, p. 13) | ≥ 1,5 A ✔ (ALI-05) |
| t_ON mínimo | D/f = 5/(53,3 × 400 kHz) = 235 ns > 102 ns máx. (p. 7) | ✔ |
| COUT | 2 × 22 µF 25 V X5R 1206 (C12891), según la Tabla 8-1 (2 × 22 µF nominales). Con 5 V de polarización quedan ≈ 2 × 14 µF; la tabla admite 4 × 10 µF como mínimo «compacto» | ✔ |
| CIN | 4,7 µF 100 V X7R 1210 (C381466) + 220 nF 100 V (C513710), según §8.2.1.2.5 (p. 20) | ✔ |
| CBOOT, CVCC | 100 nF 50 V y 1 µF 50 V (pp. 20-21) | ✔ |
| Disipación | P_OUT 3,75 W (0,75 A), η ≈ 88 % (90 % típ. a 1 A, p. 1) → 0,51 W; R_θJA ≈ 50 °C/W en 2 capas (fig. 8-3, p. 22) → T_J ≈ 86 °C | ✔ (< 125 °C) |

La FB se toma a la salida de U2, no tras U3: el multiplexor queda fuera del lazo.

### 3.7 UVLO del buck (ALI-06)

- Divisor R9 (VIN_PROT → EN) = 100 kΩ y R10 (EN → GND) = 10,0 kΩ, al 1 %. C13 = 100 nF en EN.
- Ecuaciones (SNVSBF0C ec. 10, p. 21):
  - V_ON = V_EN-H · (1 + R9/R10)
  - V_OFF = V_ON · (1 − V_EN-HYS/V_EN-H)
- Datos: V_EN-VOUT-H = 1,157 / 1,231 / 1,3 V; histéresis 110 mV típica, sin mínimo ni máximo (p. 6).

| Magnitud | Mín. | Nom. | Máx. |
|---|---|---|---|
| k = 1 + R9/R10 (resistencias al 1 %) | 10,80 | 11,00 | 11,20 |
| Arranque (en `VIN_PROT`) | 12,50 V | 13,54 V | 14,56 V |
| Bajada | — | 12,33 V | ≤ 14,56 V (cota: histéresis ≥ 0) |

- Caída de las protecciones (F1 + Q1): 5,6 mΩ × 1,3 + 26 mΩ = 33 mΩ.
  - En el arranque, solo con la lógica (0,2 A; el bus está apagado por REL-04): 7 mV.
  - En marcha, con 4,77 A: 0,16 V.
- **Arranque en frío:** 14,56 + 0,01 = 14,57 V ≤ 17 V ✔ (margen 2,43 V).
- **Funcionamiento:** bajada máx. + caída = 14,56 + 0,16 = **14,72 V ≤ 15,5 V** ✔ (margen 0,78 V). Prueba de §6 a 16 V bajando desde 24 V: la placa sigue en marcha.
- **Por encima de la VIN mínima del buck:** VOUT/D_máx + caídas ≈ 6 V < 12,5 V ✔.
- **Desviación del valor orientativo de ALI-06 (≈ 15 V):** el nominal queda en 13,5 V. Con la tolerancia de EN y sin histéresis mínima garantizada, el arranque máximo tiene que quedarse en ≈ 15,3 V para que la bajada cumpla 15,5 V. Eso fuerza un nominal ≤ 14,4 V. 105 kΩ daría 14,2 V con solo 0,11 V de margen; se prefieren 100 kΩ (0,78 V de margen). **Decidido por el usuario en DEC-0006** (100 kΩ / 10 kΩ, 13,5 V nominales). La cifra de ALI-06 se corrige en la spec de mantenimiento de la fase.
- EN a Vc: 53,3/11 = 4,85 V, por debajo de VIN + 0,3 V y de 65 V (p. 5) ✔.
- C13 con el Thévenin de 9,1 kΩ da τ = 0,91 ms: filtra las caídas de µs de §3.13.4 sin retrasar el arranque de forma apreciable.

### 3.8 Unión del USB-C al raíl de 5 V (ALI-08)

- **U3 TPS2116DRLR**, multiplexor de dos entradas con bloqueo de corriente inversa:
  - en modo prioridad: MODE = VIN1 y PR1 desde un divisor de VIN1 (§7.6.1, p. 12);
  - **VIN1 = salida del buck, VIN2 = VBUS**;
  - 2,5 A; R_ON ≤ 60 mΩ (−40…105 °C, 5 V); VIN ≤ 5,5 V (máximo absoluto 6 V; pp. 4-6).
- Cumple ALI-08 como unión «ideal»:
  - **sin retroalimentar el PC:** VIN2 se bloquea mientras haya buck;
  - **sin retroalimentar la entrada:** con solo USB, el canal VIN1 está cortado y bloquea; I_REV ≤ 0,25 µA hacia VIN1, así que el buck no recibe tensión por su salida (LMR36520 p. 26: «no permitir VOUT > VIN»).
- Descartado: **Schottky en las dos ramas.** La caída de 0,3–0,45 V del diodo del buck deja el +5V fuera de ± 3 % (§6) salvo que FB se tome tras el diodo, con el diodo dentro del lazo de un regulador con compensación interna. Un solo Schottky en VBUS retroalimenta la entrada a través del diodo interno del lado alto del buck.
- **Umbral de PR1:** R11 = 330 kΩ y R12 = 100 kΩ; k = 4,3. V_REF = 0,92–1,08 V (p. 6), así que conmuta con VIN1 entre 3,90 y 4,72 V (incluido el 1 %).
  - Por encima de 4,72 V selecciona el buck: su mínimo es 4,926 V (margen 0,2 V).
  - Por debajo de 3,90 V pasa a VBUS. Si el buck arranca con el USB conectado, el +5V baja como mucho a 3,9 V durante el cambio, porque el canal no conecta hasta que VOUT < VIN1 (p. 12). El LDO mantiene 3,3 V con 3,9 V a la entrada: caída de 230 mV típ. a 0,5 A (TLV1117LV p. 5).
- ST (drenador abierto) sin conectar; opcional, a un GPIO para saber si se alimenta del USB.
- Condensadores: 100 nF en VIN1; 1 µF en VIN2 (el bloque MCU añade el suyo); 2 × 22 µF en VOUT (C16, C17), frente a los ≈ 100 µF que recomienda la p. 11 si hay bloqueo inverso con inductancia en la salida. La salida es una pista corta y la expansión lleva sus propios condensadores. Se considera suficiente; validación puede pedir más.
- Con solo USB, +5V = VBUS − 0,05 V: lógica sin salidas (ALI-08).

### 3.9 Raíl de 3,3 V: U4 TLV1117LV33DCYR (ALI-07)

- 1 A (≥ 800 mA), límite de corriente ≥ 1,1 A, VIN 2–5,5 V. Estable con cerámicos de 0 Ω de ESR (pp. 1 y 5).
- Caída: 230 mV típ. a 500 mA; 700 mV máx. a 1 A (p. 5). Con +5V ≥ 4,88 V hay 1,58 V de margen.
- Precisión: ± 1,5 % + regulación de línea ≤ 5 mV + de carga ≤ 35 mV = **± 2,7 %** a 25 °C (p. 5). La deriva térmica no tiene máximo en el datasheet (fig. 6-6): es un riesgo frente al ± 3 % de §6, que se mide en el prototipo.
- Térmica (SOT-223; R_θJA JEDEC 62,9 °C/W, p. 4):
  - 0,45 A continuos (prueba de §6 con el Wi-Fi transmitiendo al 100 %): (5,107 − 3,3) × 0,45 = 0,81 W. Con ≥ 4 cm² de cobre en la pestaña y vías (R_θJA ≤ 60 °C/W) → T_J ≈ 109 °C < 125 °C.
  - Consumo medio realista (≤ 0,25 A): 0,43 W → ≈ 86 °C.
- Condensadores: C18 10 µF (entrada) y C19 10 µF + 100 nF (salida). El módulo lleva además su desacoplo (bloque MCU).
- Descartados:
  - **AMS1117-3.3:** caída de 1,1–1,3 V y necesita tántalo.
  - **AP7361C-33E:** 3 unidades en LCSC.

### 3.10 Medida de VIN (ALI-09)

- Divisor R14 = 100 kΩ (VIN_PROT) y R15 = 4,87 kΩ (GND), ambos al **0,1 % y 25 ppm/°C**. C20 = 100 nF en el pin, la misma condición en que Espressif mide el ADC (ESP32-S3 v2.2 §5.5, p. 66).
- k = 104,87/4,87 = **21,53**.
- Lectura con **ADC1 a 6 dB (ATTEN2, 0–1600 mV; error total ± 10 mV** tras la calibración, tabla 5-6, p. 66). A 12 dB el error es de ± 50 mV: descartado.
- Escala:

| VIN | V_ADC |
|---|---|
| 15,5 V | 0,720 V |
| 17 V | 0,789 V |
| 31 V | 1,440 V |
| 33 V (V_RWM) | 1,532 V (< 1,6 V ✔) |
| 53,3 V (Vc) | 2,475 V < VDD: el pin no necesita *clamp* |

- Thévenin: 4,64 kΩ; τ = 0,46 ms.

| VIN | ADC (± 10 mV) | Tolerancia del cociente (0,954 × 0,2 %) | Deriva (0,954 × 2 × 25 ppm × 35 °C) | Total | Lectura |
|---|---|---|---|---|---|
| 15,5 V | 1,39 % | 0,19 % | 0,17 % | **1,75 %** | 15,23–15,77 V |
| 16 V (prueba) | 1,35 % | 0,19 % | 0,17 % | 1,70 % | 15,73–16,27 V → avisa (< 17 V) ✔ |
| 17 V (umbral) | 1,27 % | 0,19 % | 0,17 % | **1,62 %** | 16,72–17,28 V |
| 18 V (prueba) | 1,20 % | 0,19 % | 0,17 % | 1,55 % | 17,72–18,28 V → no avisa ✔ |
| 29,5 V (prueba) | 0,73 % | 0,19 % | 0,17 % | 1,09 % | 29,18–29,82 V → no avisa ✔ |
| 31 V (umbral) | 0,69 % | 0,19 % | 0,17 % | **1,05 %** | 30,67–31,33 V |
| 32,5 V (prueba) | 0,66 % | 0,19 % | 0,17 % | 1,02 % | 32,17–32,83 V → avisa ✔ |

- **Se mide `VIN_PROT`, no el borne.** Con la carga instalada máxima (3,7 A) la caída de F1 + Q1 es de 0,12 V (0,72 % a 17 V), y el total sigue en ≤ 2,4 %. El firmware puede compensarla con la IMON (V_borne ≈ V_PROT + I · 33 mΩ).
- Margen frente a ± 3 %: ≥ 1,2 puntos para lo que el datasheet no cuantifica (25 °C y Wi-Fi apagado). En el firmware, promediar ≥ 16 muestras.

### 3.11 LED de alimentación (ALI-10)

- D4 KT-0603R (rojo; V_F 1,8–2,4 V a 20 mA; C2286) con R13 = 1 kΩ en **+3V3**. I = (3,3 − 1,9)/1 k ≈ 1,4 mA.
- Indica que la lógica está alimentada, también con solo USB.

### 3.12 Test points (ALI-11)

- Símbolo `Connector:TestPoint`, sin pieza (fuera de BOM y CPL):
  - TP1 VIN_PROT, TP2 +5V, TP3 +3V3 y TP5 BUS_24V: `TestPoint:TestPoint_Pad_D2.0mm`;
  - TP4 GND: `TestPoint:TestPoint_THTPad_D2.0mm_Drill1.0mm`, para la pinza.
- TP5 no lo pide ALI-11. Sirve para las pruebas del limitador de §6.

### 3.13 Limitador común U1: TPS26632RGER (ALI-12, ALI-13, REL-04)

#### 3.13.1 Elección

- eFuse con FET integrado (31 mΩ). Incluye:
  - límite de corriente de ± 7 %;
  - *fast-trip*;
  - apagado térmico;
  - SHDN;
  - FLT;
  - IMON de ± 6 %;
  - *clamp* de sobretensión fijo de 32–35 V en la salida (SLVSE94G pp. 2 y 6-8).
- Frente al LM5069, ahorra el NFET, R_S, el cálculo de SOA y ≈ 1 $.
- Variante 26632: 1× I_OL, PLIM desactivable y stock de 1 631.
  - La 26630/31 (OVP ajustable) no tiene stock suficiente.
  - La 26635/36 hace *clamp* a 39 V.
- El *clamp* de 32–35 V (V_OVC, p. 6) queda por encima del máximo de 30 V de ALI-01 (margen 2 V) y limita el bus de las salidas a ≤ 35 V ante sobretensiones de la entrada. La disipación del *clamp* dura como mucho t_OVC = 162 ms (p. 20).

#### 3.13.2 Umbral de corriente (banda de ALI-13)

- I_OL = 18/R_ILIM [kΩ] (ec. 5, p. 22). El datasheet solo da la tolerancia en cuatro puntos (p. 7):

| R_ILIM | Típ. | Tolerancia | Constante (típ. × R) |
|---|---|---|---|
| 3 kΩ | 6 A | ± 7 % | 18,0 |
| 4,02 kΩ | 4,5 A | ± 7 % | 18,09 |
| 9 kΩ | 2 A | ± 8 % | 18,0 |
| 30 kΩ | 0,6 A | ± 10 % | 18,0 |

- Para 4,30 kΩ (entre 3 y 9 kΩ) se toma, de forma conservadora:
  - la constante del punto más próximo, 18,09 (4,02 kΩ), que da una nominal mayor que la ec. 5;
  - la tolerancia interpolada linealmente entre 4,02 kΩ (± 7 %) y 9 kΩ (± 8 %): ± 7,06 %, redondeada a **± 7,1 %** (VAL-0017-01-02).
- R2 = R_ILIM = **4,30 kΩ** al 1 % y 100 ppm/°C (C23159). Deriva: ± 0,35 % entre 25 y 60 °C.

| | Valor |
|---|---|
| I_OL nominal = 18,09/4,30 (con la ec. 5: 4,186 A) | 4,207 A |
| I_OL mín. = 18,09/(4,30 × 1,0135) × 0,929 | **3,86 A** ≥ 3,5 A (margen 10,2 %) ✔ |
| I_OL máx. = 18,09/(4,30 × 0,9865) × 1,071 | **4,57 A** ≤ 4,9 A ✔ |
| I_OL máx. + lógica | 4,77 A < 5,14 A (margen 0,37 A) ✔ |
| *Fast-trip* (26632: 2 × I_OL, p. 7) | 8,4 A nom. Corto franco (> I_SCP = 45 A): 1 µs típ., sin máximo. Corto blando (I_FASTTRIP–I_SCP): 2,2 / 3,2 / **4,5 µs** (§6.6, p. 9) |

La tolerancia del datasheet está medida con V_IN − V_OUT = 1 V (p. 7). En un corto franco el lazo regula con ≈ 24 V de V_DS. La prueba de §6 (3,4 A y 5,5 A) lo comprueba en el prototipo.

#### 3.13.3 Respuesta a fallo y modo (REL-08)

- **MODE abierto = *latch-off*** (tabla 8-1, p. 28). Tras una sobrecarga, el limitador regula a I_OL durante un máximo de t_CL_PLIM = 162 ms, o hasta el apagado térmico si llega antes (p. 22), y se enclava con FLT a nivel bajo.
- El rearme lo hace el firmware con un flanco de SHDN de bajo a alto, después de:
  1. apagar todos los IN;
  2. rearmar;
  3. encender los canales uno a uno, vigilando FLT e IS.

  Así cumple los ≤ 5 s de REL-08.
- Se elige el *latch* frente al reintento automático (cada 648 ms, p. 27) para no recalentar contra un corto. Si el firmware se cuelga, el bus queda apagado: estado seguro.
- Arranque con un corto (SHDN alto con un canal en corto): el bucle térmico regula T_J a 145 °C durante 2,5 s como máximo y después se enclava (pp. 18 y 25).

#### 3.13.4 Corte sin bajar del UVLO (ALI-13)

- En sobrecarga o corto, la fuente entrega como mucho I_OL,máx + lógica = 4,77 A < 5,14 A. **Su protección no actúa y `VIN_PROT` no cae** de forma sostenida: la lógica no necesita retención (S2).
- Único transitorio: el tiempo hasta el *fast-trip* (§3.13.2). En el corto franco es de 1 µs típico, sin máximo publicado; en el blando, ≤ 4,5 µs (p. 9). Las cotas de la caída de `VIN_PROT`, solo con los cerámicos (2 × 4,7 µF a 24 V ≈ 7,9 µF efectivos) y sin contar C1 ni la fuente, son:
  - corto franco, con el típico: Q ≈ 45 A × 1 µs = 45 µC → ΔV ≈ 5,7 V;
  - corto blando, en el peor caso: Q ≤ 45 A × 4,5 µs = 202 µC → ΔV ≤ 25 V. La caída de `VIN_PROT` es casi total durante ≤ 4,5 µs. C1 (47 µF, ESR sin especificar) la reduce, pero no se cuantifica (VAL-0017-01-04).
- La conclusión no depende de esa cota. Con `VIN_PROT` a 0 V durante 4,5 µs:
  - el +5V lo sostienen C11/C12 (≈ 28 µF efectivos): ΔV = 0,75 A × 4,5 µs / 28 µF = **0,12 V**, y quedan además C16/C17 tras U3;
  - el EN (τ = 0,91 ms, §3.7) baja ≤ 0,5 % y no cruza el umbral;
  - el VCC interno de U2 lo sostiene su condensador de 1 µF.

  La lógica no se reinicia.
- **Verificación en el prototipo:** en la prueba de §6 «Cortocircuito en una salida» (corto franco y con cable de ≥ 10 m), medir `VIN_PROT` (TP1) y +5V (TP2) con el osciloscopio: amplitud y duración de la caída.

#### 3.13.5 Habilitación (REL-04, ALI-13)

- SHDN: bajo < 0,8 V (apagado), alto > 2 V (p. 7).
- La fuente interna de SHDN da hasta 10 µA (I_SHDN, p. 7). R5 = 10 kΩ a GND → V = 0,1 V < 0,8 V: **bus apagado durante el arranque, el reset y el flasheo**.
- El pin del ESP32-S3 no tiene *pull-up* al reset en GPIO1–GPIO21 (salvo los de arranque; ESP32-S3 v2.2, tabla de pines de la p. 16 y nota 6 de la p. 18, columna «Pin Settings»).
- Con el GPIO a 3,3 V (V_OH ≥ 2,64 V): 0,33 mA por R5. V_SHDN ≤ 5,5 V máx. absoluto ✔.
- Retardo de encendido: 742 + 49,5 × C_dVdT[nF] µs = 1,83 ms más la rampa (p. 8). El firmware espera ≥ 20 ms tras subir LIM_EN antes de activar canales.

#### 3.13.6 dVdT, salida y PGTH

- C4 = C_dVdT = 22 nF (≥ 10 nF, §6.3, p. 5). t = 20,8·10³ · V_IN · C (p. 18): 11,0 ms a 24 V y 13,7 ms a 30 V.
  - Con C_BUS ≈ 15 µF (C6 + desacoplo de los *high-side*), I_INRUSH ≈ 33 mA.
  - Disipación: 0,5 × 24 × 0,033 = 0,4 W durante 11 ms (ec. 3, p. 18) ✔.
- C6 = 4,7 µF 100 V en OUT (≥ 0,1 µF, p. 5). D3 = SS310 (100 V, 3 A), de OUT a GND (cátodo en OUT): transitorios negativos al cortar con cable inductivo (§9.6.1, ficha TPS2663).
- **PGTH a GND:** desactiva el encendido rápido tras un fallo (p. 19). PGOOD sin conectar.
- **UVLO a GND:** UVLO interno del bus, 15,1–15,9 V al subir y 14,0–15,1 V al bajar (p. 6). Habilita el bus por encima de 15,9 V (< 17,9 V en `VIN_PROT` con 18 V en el borne ✔).
- **PLIM a GND:** sin limitación de potencia (p. 25). Con PLIM, a 30 V el límite caería por debajo de 3,5 A.
- IN_SYS unido a IN, con C3 = 100 nF 100 V junto al pin (p. 27). B_GATE y DRV abiertos (p. 27). NC 19–24 sin conectar.

#### 3.13.7 FLT e IMON

- FLT: R6 = 10 kΩ a +3V3 → GPIO (entrada). V_OL = 0,33 mA × 130 Ω = 43 mV (p. 8).
- IMON: R3 = 10,0 kΩ a GND; ganancia 26,22–29,58 µA/A para 2–6 A (p. 8). V_IMON = I · 27,9 µA/A · 10 kΩ = 0,279 V/A.
  - A 3,5 A: 0,91–1,05 V (± 7 %).
  - A 4,57 A: 1,19–1,37 V.
  - Cabe en ADC1 a 6 dB.
  - R4 = 10 kΩ en serie hasta el GPIO y **C5 = 100 nF** en el pin del ADC (VAL-0017-01-03). Es la condición con la que Espressif da su ± 10 mV (ESP32-S3 v2.2 §5.5, p. 66). Con la fuente de R3 + R4 = 20 kΩ, τ ≈ 2 ms: no afecta al firmware, que detecta los fallos con FLT. En el pin de IMON no va condensador (p. 27): C5 queda detrás de R4.
  - Durante el *fast-trip*, IMON puede llegar a su tope de ≈ 4–5,5 V (V_IMONmax 4 V, máximo absoluto 5,5 V; p. 5). R4 limita la corriente por el diodo de protección del GPIO a ≤ 0,2 mA durante µs.
- Medida del total: ± 7 % (ganancia ± 6 % y R3 al 1 %) más el ± 10 mV del ADC (≈ ± 1 % a 3,5 A). Sustituye a la suma de IS (± 25 %, S4).

#### 3.13.8 Térmica de U1

- R_ON ≤ 45 mΩ a 85 °C (p. 7); R_θJA 31,4 °C/W en JEDEC (p. 6). En 2 capas se toman 50 °C/W.
- 3,5 A: 0,55 W → T_J ≈ 88 °C.
- 4,57 A (justo bajo el umbral; R_ON 53 mΩ): 1,11 W → ≈ 115 °C. Por debajo de T_J_REG (136 °C mín.) y de TSD (165 °C) ✔.
- Pad térmico al plano de GND con vías (p. 39).

#### 3.13.9 Puente de soldadura JP1 en paralelo con U1 (DEC-0006)

- **Función:** une `VIN_PROT` (U1 IN) con `BUS_24V` (U1 OUT) con una gota de estaño si U1 no se monta o falla abierto. Por defecto va **abierto**, con U1 montado.
  - No se cierra con U1 montado y sano: la corriente se lo saltaría.
  - Si U1 falla en corto, el puente no aporta nada.
- **Símbolo:** `Jumper:SolderJumper_2_Open` (oficial). Ref. JP1, sin pieza: fuera de BOM y CPL.
- **Huella:** la oficial `Jumper:SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm` tiene pads de 1,5 mm de ancho, menos que los 2,0 mm de `Power_In` (§8). Se pide una **huella nueva** en `esp-riego.pretty` (SPEC-0018), con la misma construcción que la oficial: pads solo en F.Cu y F.Mask, sin pasta.
  - Nombre: `SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm`.
  - Pads rectangulares de 1,2 mm (en el sentido de la corriente) × 3,0 mm (ancho), separados **0,6 mm**; paso 1,8 mm (VAL-0017-01-01).
  - Abertura de máscara común a los dos pads y al hueco, para poder puentearlos con el soldador.
  - Sin pasta: así no se cierra en el *reflow*.
- **Cálculo para 4,9 A** (la corriente máxima de la banda; ALI-13, REL-05):

| Tramo | Cálculo | Resultado |
|---|---|---|
| Cobre de los pads (1 oz, 3,0 mm) | IPC-2221 externa: 5,1 A necesita 2,84 mm para ΔT 10 °C (§8) | 3,0 mm ≥ 2,84 mm ✔ |
| Puente de estaño (SAC305, ρ ≈ 13,2 µΩ·cm) | Sección ≥ 3,0 mm × 0,2 mm (gota mínima) = 0,6 mm²; longitud 0,6 mm → R = ρ·L/A = 13,2·10⁻⁸ × 0,6·10⁻³ / 0,6·10⁻⁶ = 0,13 mΩ | P = 4,9² × 0,13 mΩ = **3,2 mW** |
| Equivalencia en cobre | 0,6 mm² × (1,72/13,2) = 0,078 mm², frente a 0,070 mm² de una pista de 2,0 mm en 1 oz | Igual o mejor que la pista `Power_In` ✔ |
| Densidad de corriente en el estaño | 4,9 A / 0,6 mm² = 8,2 A/mm² | Sin problema ✔ |
| Separación entre pads | Abierto, con U1 apagado (REL-04) y el bus a 0 V, `VIN_PROT` puede llegar a Vc = 53,3 V. Se aplica el mismo criterio que al resto de `Power_In` (§8): IPC-2221 B2, 51–100 V → 0,6 mm | **0,6 mm** ✔ (VAL-0017-01-01) |

  - Con la huella oficial (1,5 mm), el estaño da 0,039 mm² equivalentes (≈ 1,1 mm de pista). Corto y bien refrigerado, pero por debajo de la clase `Power_In`: descartada.
- **Funciones que se pierden con JP1 cerrado (sin U1):**

| Función | Con JP1 cerrado |
|---|---|
| Limitación común a 3,86–4,57 A (ALI-13) | Se pierde. Un corto en una salida lo limita la protección de la fuente (≥ 5,14 A, hipo o corriente constante) y la limitación del BTT6050 (≥ 38 A). Cae `VIN_PROT` y la lógica puede reiniciarse: **REL-08 no se cumple** |
| Corte general por LIM_EN (S3) | Se pierde: el bus está siempre alimentado. La comprobación de carga abierta (REL-10) funciona igual |
| FLT e IMON | Se pierden. Sin U1, FLT lee alto siempre por R6 e IMON lee 0 V; el firmware debe desactivarlos (opción de configuración) |
| *Clamp* del bus a ≤ 35 V | Se pierde: el bus ve `VIN_PROT` hasta Vc = 53,3 V. Sigue dentro de V_S(LD) = 65 V del BTT6050 (ALI-04) ✔ |
| Arranque suave del bus (dVdT) | Se pierde: el bus se carga al conectar la fuente, limitado solo por el cable |
| REL-04 (salidas apagadas en el reset y el flasheo) | **Se mantiene** por el *pull-down* de cada IN de los *high-side* (bloque de salidas). Deja de cumplirse para el corte general del bus |

- **Serigrafía y documentación** (DEC-0006): junto a JP1, «JP1: abierto = limitador · cerrado = sin limitador». Detalle de lo que se pierde en el README de `hardware/v2`.

## 4. Presupuesto de potencia (6 salidas activas)

| Raíl | Carga | Corriente de diseño | Capacidad | Margen |
|---|---|---|---|---|
| **24 V (borne)** | Salidas: 3,5 A (carga instalada máx.; tope del limitador 4,57 A) + lógica 0,18 A + U1, divisores y zéner (2,3 mA) | **3,68 A** normal; **4,77 A** con el limitador en su máximo | Fuente: sobrecarga a ≥ 5,14 A · F1: 7,2 A (derating) · Q1: 50 A · J1: 15 A | 0,37 A (7,2 %) sobre la fuente en el peor caso |
| **5 V** (U2 → U3) | 3,3 V: 0,45 A + 5 V de la expansión: 0,30 A | **0,75 A** | U2: 2 A (ALI-05 ≥ 1,5 A) · U3: 2,5 A | 2,7× |
| **3,3 V** (U4) | ESP32-S3-WROOM-1: 355 mA de pico (802.11b, 20,5 dBm; WROOM-1 v1.8 tabla 6-4, p. 28) + SHT4x, LED, *pull-ups*, LED de estado y de canal (≈ 45 mA) + 3,3 V de la expansión (≤ 50 mA) | **0,45 A** | U4: 1 A (límite ≥ 1,1 A) | 2,2× |

Potencia de la lógica en la entrada (ALI-12, §6):

- P_5V = 5,0 V × 0,75 A = 3,75 W; η del buck ≈ 88 % → 4,26 W.
- Más U1 (1,7 mA, p. 6) y divisores: 0,05 W.
- **Total: 4,32 W ≤ 4,8 W** (0,18 A a 24 V), con un margen del 10 %.
- La corriente máxima en 5 V que cabe en 4,8 W es 0,835 A.

**Propuesta para SPEC-0006 (expansión):** 5 V ≤ 0,30 A y 3,3 V ≤ 50 mA.

## 5. Térmica (resumen a 60 °C en la caja)

| Pieza | P | R_θJA usada | T_J | Límite |
|---|---|---|---|---|
| Q1 SQD50P06-15L (5,1 A) | 0,68 W | 50 °C/W (1 in², p. 1) | 94 °C | 175 °C |
| F1 (5,1 A) | 0,19 W | — | — | 7,2 A con derating |
| U1 TPS26632 (3,5 / 4,57 A) | 0,55 / 1,11 W | 50 °C/W | 88 / 115 °C | 136 °C (T_J_REG mín.) |
| U2 LMR36520 (0,75 A) | 0,51 W | 50 °C/W | 86 °C | 125 °C |
| U3 TPS2116 | 34 mW | 111,5 °C/W (p. 4) | 64 °C | 105 °C (T_A) |
| U4 TLV1117LV (0,45 / 0,25 A) | 0,81 / 0,43 W | 60 / 62,9 °C/W | 109 / 87 °C | 125 °C |

## 6. Pines del ESP32-S3 que pide el bloque (propuesta para el bloque MCU, MCU-05)

| Señal | Pin propuesto | Tipo | Nota |
|---|---|---|---|
| VIN_SENSE | GPIO1 (ADC1_CH0) | Analógica, 6 dB | k = 21,534; aviso < 17 V y > 31 V |
| LIM_IMON | GPIO2 (ADC1_CH1) | Analógica, 6 dB | 0,279 V/A (27,9 µA/A × 10 kΩ) |
| LIM_EN | GPIO21 | Salida, activa alta | R5 de 10 kΩ a GND; sin *pull-up* al reset |
| LIM_FLT | GPIO14 | Entrada, activa baja | R6 de 10 kΩ a +3V3 |

- Ningún pin de arranque (0, 3, 45, 46) ni GPIO19/20.
- La asignación final la cierra el bloque MCU junto con los IN, DEN e IS de las salidas. El YAML de `firmware/` se actualiza cuando el pinout esté en el esquema.

## 7. Lista de piezas

Referencias provisionales (las fija la anotación en SPEC-0019). Stock de LCSC del 2026-11-05. Las huellas y los símbolos son de las librerías oficiales de KiCad 10 salvo donde se indica.

| Ref. | Valor / función | Encapsulado | MPN principal | LCSC · stock | Alternativa (LCSC) | Símbolo / huella |
|---|---|---|---|---|---|---|
| J1 | Borne 2P, entrada | THT 5,08 | WJ500V-5.08-2P | C8465 · 274 005 | — | Existente (proyecto) |
| F1 | Fusible 10 A muy rápido | 2410 | Littelfuse 0451010.MRL | C44479 · 22 770 | TLC TA10 (C2998199) | `Device:Fuse` / `Fuse:Fuse_Littelfuse-NANO2-451_453` |
| Q1 | P-MOS de polaridad, 60 V | TO-252 | Vishay SQD50P06-15L_GE3 | C3281500 · 5 748 | UMW SUD50P06-15 (C7503186) | `Transistor_FET:SUD50P06-15` (comprobar G-D-S) / `Package_TO_SOT_SMD:TO-252-2` |
| D1 | Zéner 15 V, puerta de Q1 | SOD-123 | MDD BZT52C15 | C173427 · 148 150 | Diodes BZT52C15-7-F (C177014 · 52 695) | `Device:D_Zener` / `Diode_SMD:D_SOD-123` |
| R1 | 100 kΩ 1 % | 0603 | UNI-ROYAL 0603WAF1003T5E | C25803 · 7,8 M | Yageo RC0603FR-07100KL | `Device:R` / `Resistor_SMD:R_0603_1608Metric` |
| D2 | TVS SMBJ33A | SMB | Littelfuse SMBJ33A | C224019 · 9 670 | Ruilon SMBJ33A (C10219 · 10 155); el Brightking C78419 de la ficha tiene stock 0 | Existente (ficha) |
| C1 | 47 µF 63 V electrolítico 105 °C | Ø8 × 10 | SamYoung MVK 63V47 M 8*10 | C165628 · 815 | ACMECON GVZ1J476M0810CN (C22383753) | `Device:C_Polarized` / `Capacitor_SMD:CP_Elec_8x10` (10,5 mm la alternativa) |
| C2, C6, C7 | 4,7 µF 100 V X7R | 1210 | PSA FS32X475K101EGG | C381466 · 45 775 | Walsin 1210B475K101CT (C7471274) | `Device:C` / `Capacitor_SMD:C_1210_3225Metric` |
| C3 | 100 nF 100 V X7R (IN_SYS) | 0603 | Samsung CL10B104KC8NNNC | C15725 · 110 800 | — | `Device:C` / `C_0603_1608Metric` |
| U1 | eFuse 60 V, limitador común | VQFN-24 4 × 4 | TI TPS26632RGER | C1850278 · 1 631 | TPS26633RGER (C1850275; stock 11, 6,9 $; misma huella, 2× pulso) | `Power_Management:TPS26632RGE` / `Package_DFN_QFN:Texas_RGE0024H_…_ThermalVias` |
| R2 | R_ILIM 4,30 kΩ 1 % 100 ppm | 0603 | 0603WAF4301T5E | C23159 · 113 900 | Yageo RC0603FR-074K3L | `R_0603` |
| C4 | C_dVdT 22 nF 50 V X7R | 0603 | Samsung CL10B223KB8NNNC | C21122 · 109 250 | — | `C_0603` |
| R3, R4 | R_IMON y serie al ADC, 10 kΩ 1 % | 0603 | 0603WAF1002T5E | C25804 · 4,9 M | — | `R_0603` |
| C5 | 100 nF 50 V X7R (ADC de IMON) | 0603 | Samsung CL10B104KB8NNNC | C1591 · 1,46 M | — | `C_0603` |
| R5, R6 | *Pull-down* de SHDN y *pull-up* de FLT, 10 kΩ | 0603 | 0603WAF1002T5E | C25804 | — | `R_0603` |
| D3 | Schottky 100 V 3 A (OUT del limitador) | SMA | MDD SS310 | C15874 · 348 680 | UMW SS310A (C2988628 · 4 720) | `Device:D_Schottky` / `Diode_SMD:D_SMA` |
| U2 | Buck 65 V 2 A FPWM | HSOIC-8 PowerPAD | TI LMR36520FADDAR | C1858395 · 7 969 | LMR36520ADDAR (C2879422) | **Símbolo nuevo** (copiar `Regulator_Switching:LMR36510ADDA`, compatible pin a pin, p. 1) / `Package_SO:Texas_HTSOP-8-1EP_3.9x4.9mm_…_ThermalVias` |
| C8 | 220 nF 100 V X7R (CIN de AF) | 0805 | Yageo CC0805KKX7R0BB224 | C513710 · 72 260 | Samsung CL21B224KCFSFNE (C307542) | `C_0805_2012Metric` |
| C9 | CBOOT 100 nF 50 V | 0603 | Samsung CL10B104KB8NNNC | C1591 · 1,46 M | — | `C_0603` |
| C10 | CVCC 1 µF 50 V X5R | 0603 | Samsung CL10A105KB8NNNC | C15849 · 436 100 | — | `C_0603` |
| L1 | 10 µH, I_sat 5,3 A, 60 mΩ | 7 × 6,6 | Changjiang FXL0650-100-M | C475521 · 38 855 | FXLA0630-100M (C5372143; I_sat 5,5 A) | `Device:L` / `Inductor_SMD:L_Changjiang_FXL0650` (alt.: `FXL0630`) |
| C11, C12, C16, C17 | 22 µF 25 V X5R | 1206 | Samsung CL31A226KAHNNNE | C12891 · 7 980 | — (jr-conformidad) | `C_1206_3216Metric` |
| R7 | RFBT 100 kΩ 0,1 % 25 ppm | 0603 | Yageo RT0603BRD07100KL | C122538 · 1,68 M | Viking ARG03BTC1003 (C335088) | `R_0603` |
| R8 | RFBB 24,9 kΩ 0,1 % 25 ppm | 0603 | Viking AR03BTCX2492 | C4156365 · **760** | Yageo RT0603BRE0724K9L (C861775; stock 0) | `R_0603` |
| R9 | EN superior 100 kΩ 1 % | 0603 | 0603WAF1003T5E | C25803 | — | `R_0603` |
| R10 | EN inferior 10 kΩ 1 % | 0603 | 0603WAF1002T5E | C25804 | — | `R_0603` |
| C13 | Filtro de EN, 100 nF 50 V | 0603 | CL10B104KB8NNNC | C1591 | — | `C_0603` |
| U3 | Multiplexor 5 V 2,5 A | SOT-583 | TI TPS2116DRLR | C3235557 · 54 523 | — (sin equivalente en la misma huella; reserva: 2 Schottky, §3.8) | `Power_Management:TPS2116DRL` / `Package_TO_SOT_SMD:SOT-583-8` |
| R11 | PR1 superior 330 kΩ 1 % | 0603 | 0603WAF3303T5E | C23137 · 404 100 | — | `R_0603` |
| R12 | PR1 inferior 100 kΩ 1 % | 0603 | 0603WAF1003T5E | C25803 | — | `R_0603` |
| C14 | 100 nF (VIN1) | 0603 | CL10B104KB8NNNC | C1591 | — | `C_0603` |
| C15 | 1 µF (VIN2) | 0603 | CL10A105KB8NNNC | C15849 | — | `C_0603` |
| U4 | LDO 3,3 V 1 A | SOT-223 | TI TLV1117LV33DCYR | C15578 · 1 530 | JSMSEMI TLV1117LV33DCYR (C48937499; verificar datasheet) | `Regulator_Linear:TLV1117-33` (comprobar el pinout 1 GND, 2/tab OUT, 3 IN; p. 3) / `Package_TO_SOT_SMD:SOT-223-3_TabPin2` |
| C18, C19 | 10 µF 10 V X5R | 0603 | Samsung CL10A106KP8NNNC | C19702 · 1,47 M | — | `C_0603` |
| C21 | 100 nF (salida del LDO) | 0603 | CL10B104KB8NNNC | C1591 | — | `C_0603` |
| R14 | Divisor de VIN 100 kΩ 0,1 % 25 ppm | 0603 | Yageo RT0603BRD07100KL | C122538 | Viking ARG03BTC1003 (C335088) | `R_0603` |
| R15 | Divisor de VIN 4,87 kΩ 0,1 % 25 ppm | 0603 | Yageo AT0603BRD074K87L | C855888 · 4 010 | Yageo RT0603BRE074K87L (C849789; 50 ppm: suma 0,17 % al error) | `R_0603` |
| C20 | 100 nF (ADC de VIN) | 0603 | CL10B104KB8NNNC | C1591 | — | `C_0603` |
| D4 | LED rojo | 0603 | Hubei KENTO KT-0603R | C2286 · 4,2 M | XINGLIGHT XL-1608SURC-06 (C965799) | `Device:LED` / `LED_SMD:LED_0603_1608Metric` |
| R13 | 1 kΩ 1 % | 0603 | 0603WAF1001T5E | C21190 · 2,86 M | — | `R_0603` |
| JP1 | Puente de soldadura `VIN_PROT`–`BUS_24V`, abierto | Pads 1,2 × 3,0 mm, hueco 0,6 mm | — (sin pieza; estaño a mano) | — | Huella oficial `SolderJumper-2_P1.3mm_Open_Pad1.0x1.5mm` (descartada para 4,9 A, §3.13.9) | `Jumper:SolderJumper_2_Open` / **huella nueva** `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` (SPEC-0018). Excluir de BOM y CPL |
| TP1–TP5 | Test points | Pad | — (sin pieza) | — | Keystone 5000/5001 | `Connector:TestPoint` / `TestPoint:TestPoint_Pad_D2.0mm` (TP4: `TestPoint_THTPad_D2.0mm_Drill1.0mm`) |

- **Piezas sin ficha en `hardware/componentes/`:** LMR36520, TPS2116, TLV1117LV, SQD50P06-15L, 0451010.MRL, FXL0650-100-M, SS310 y BZT52C15. Los datos clave y las páginas están en §3 y §0.
- La ficha de TPS2663 existe. Hay que añadirle la variante elegida (26632, *latch*, PLIM y UVLO a GND).
- **Símbolos o huellas nuevos:**
  - el símbolo LMR36520, que se puede derivar de LMR36510ADDA;
  - la huella `SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` de JP1 (§3.13.9).

  El resto existe en las librerías oficiales. Hay que comprobar el pinout de SUD50P06-15 frente a SQD50P06-15L y el de TLV1117-33 frente a TLV1117LV.
- **Coste orientativo del bloque:** ≈ 8,9 $ por placa (5 placas) y ≈ 7,7 $ (10 placas), con los tramos de LCSC de la cantidad real. **Aceptado en DEC-0006**.
  - El limitador cuesta 3,56 / 3,02 $, por encima de los 2–3 $ que estimaba DEC-0003.
  - La alternativa UMW de Q1 ahorra ≈ 0,7 $.

## 8. Restricciones de layout

| Red | Corriente | Ancho mín. | Separación | Ubicación / keepout | Notas |
|---|---|---|---|---|---|
| VIN_RAW (J1 → F1), VIN_F (F1 → Q1-D), VIN_PROT (Q1-S → U1 IN, D2, C1, C2) | 5,1 A continuos | **2,0 mm** en 1 oz (IPC-2221 externa: 1,87 mm para ΔT 20 °C; 2,84 mm para ΔT 10 °C) o polígono | ≥ 0,6 mm a otras redes (hasta 53 V: IPC-2221 B2, 51–100 V); en los pads de los CI, la de la huella | J1 → F1 → Q1 → D2 en línea y juntos en el borde inferior (FAB-07) | Clase `Power_In`. Retorno GND paralelo y del mismo ancho |
| BUS_24V (U1 OUT → *high-side*) | 4,57 A (4,9 A como dato de REL-05) | 2,0 mm o polígono | ≥ 0,6 mm | — | Clase `Power_In`. D3 y C6 junto a OUT/GND de U1 |
| JP1 (VIN_PROT ↔ BUS_24V) | 4,9 A con el puente cerrado | Pads de 3,0 mm; las pistas que llegan, 2,0 mm o polígono | Hueco de 0,6 mm entre pads (Vc 53,3 V con el bus a 0 V; IPC-2221 B2, 51–100 V) | Junto a U1, entre el cobre de IN y el de OUT; cara superior y accesible al soldador (sin piezas altas a ≤ 2 mm) | Sin pasta. Serigrafía «JP1: abierto = limitador · cerrado = sin limitador» |
| GND de potencia (J1-2, D2, C1, U1, U2) | 5,1 A | Plano; vías de cosido junto a J1, D2 y U1 | — | — | D2 a GND con pista corta y ancha: el pulso de 11,3 A suma L·di/dt a Vc (ficha SMBJ33A) |
| VIN_PROT → U2 VIN (rama del buck) | 0,3 A | 0,6 mm (`Power`) | ≥ 0,6 mm | C8 de 220 nF pegado a VIN–PGND de U2; C7 justo después | Bucle de entrada mínimo (SNVSBF0C §8.5) |
| SW (U2-8 → L1) | 1,5 A de pico ≈ 2 A | 1,0 mm, lo más corto posible | ≥ 0,3 mm | Lejos de la antena (MCU-02), de las entradas del ADC y del SHT4x (AMB-02) | Área mínima; sin pistas de señal debajo en la otra cara |
| +5V_BUCK (L1 → C11/C12 → U3 VIN1), +5V (U3 VOUT) | 0,75 A (diseño); 1,5 A | 0,6 mm (`Power`) | 0,2 mm | — | FB (R7/R8) tomada en C11/C12, lejos de SW y de L1 |
| VBUS → U3 VIN2 | 0,5 A | 0,5 mm | 0,2 mm | Desde el USB-C (bloque MCU) | — |
| +3V3 (U4 → módulo) | 0,45 A; 1 A máx. | 0,5 mm | 0,2 mm | — | Pestaña de U4: ≥ 4 cm² de cobre por cara con vías (T_J ≤ 109 °C, §3.9) |
| Q1 (pestaña = drenador, VIN_F) | 5,1 A | Polígono ≥ 2,5 cm² (R_thJA = 50 °C/W con 1 in², p. 1) | ≥ 0,6 mm | — | R1 y D1 junto a la puerta |
| U1 EP, U2 EP | — | Pad térmico al plano GND con vías | — | U1 junto a la salida hacia las salidas; U2 lejos de la antena y del SHT4x | SLVSE94G p. 39; SNVSBF0C §8.5 |
| ILIM (U1-10 → R2), dVdT (U1-9 → C4), IMON (U1-13 → R3) | µA | 0,25 mm | 0,2 mm | R2, C4 y R3 junto a su pin, con retorno corto al GND de U1 | R2 sin acoplamiento a SW (SLVSE94G §9.6.1) |
| EN_BUCK (R9/R10/C13 → U2-3) | µA | 0,25 mm | ≥ 0,6 mm entre el lado VIN_PROT de R9 y el resto | R10 y C13 junto a U2 | Nodo de alta impedancia: lejos de SW |
| VIN_SENSE (R14/R15 → C20 → GPIO), LIM_IMON (R4 → C5 → GPIO) | µA | 0,25 mm | 0,2 mm (≥ 0,6 mm en el lado VIN_PROT de R14) | C20 y C5 junto al pin del módulo | Lejos de SW, de L1 y de las salidas. Sin cortes del plano debajo (FAB-04) |
| LIM_EN, LIM_FLT | — | 0,25 mm | 0,2 mm | — | R5 junto a U1-12 (SHDN) |
| U2 + L1 + C11/C12 | — | — | — | *Keepout*: ≥ 15 mm del SHT4x y fuera de la zona de la antena | MCU-02, AMB-02 |

## 9. Trazabilidad

| Requisito | Pieza o cálculo | Sección |
|---|---|---|
| ALI-01 (18–30 V; 24 V ± 2 %) | Arranque ≤ 14,57 V; V_RWM 33 V; *clamp* de U1 ≥ 32 V; bus habilitado desde ≤ 15,9 V | §3.4, §3.7, §3.13.6 |
| ALI-02 | J1 WJ500V-5.08-2P | §3.1 |
| ALI-03 | Q1 SQD50P06-15L + D1 + R1; 5,1 A a 60 °C, T_J 94 °C | §3.3 |
| ALI-04 | F1 10 A (7,2 A con derating); D2 SMBJ33A tras Q1; Vc ≤ nominal del nodo | §3.2, §3.4, §3.5 |
| ALI-05 | U2 65 V / 2 A; nodo ≥ 60 V | §3.5, §3.6 |
| ALI-06 | R9/R10: arranque 12,50–14,56 V; bajada ≤ 14,56 V | §3.7 |
| ALI-07 | U4 TLV1117LV 1 A | §3.9 |
| ALI-08 | U3 TPS2116 en modo prioridad | §3.8 |
| ALI-09 | R14/R15 al 0,1 %, ADC1 a 6 dB: ≤ ± 1,75 % | §3.10 |
| ALI-10 | D4 + R13 | §3.11 |
| ALI-11 | TP1–TP5 | §3.12 |
| ALI-12 | Presupuesto: 4,77 A máx.; lógica 4,32 W | §4 |
| ALI-13 | U1 TPS26632: 3,86–4,57 A, *latch*, SHDN con *pull-down*, FLT e IMON; buck antes del limitador. JP1 abierto por defecto (DEC-0006) | §3.13, §3.13.9 |
| REL-04 | R5: bus apagado en el reset y el flasheo | §3.13.5 |

## 10. Riesgos y puntos abiertos

1. **ALI-06, valor orientativo:** cerrado por DEC-0006 (13,5 V nominales). Queda pendiente la corrección del texto de ALI-06 en la spec de mantenimiento.
2. **Fuente real:** DEC-0004 y `docs/03` piden comprobar en su etiqueta que es de tensión constante y su punto de sobrecarga. La banda se ha calculado con los supuestos de DEC-0004.
3. **Tolerancia de I_OL con V_DS alta** (corto franco): el datasheet la da con 1 V (§3.13.2). Se comprueba en las pruebas de §6.
4. **TLV1117LV:** sin deriva térmica máxima publicada (§3.9); ± 2,7 % a 25 °C frente a ± 3 %.
5. **R8 (24,9 kΩ al 0,1 %):** solo hay 760 en stock. La alternativa Yageo no tiene stock.
6. **Condensadores de salida de U3:** 44 µF nominales frente a los ≈ 100 µF que sugiere el datasheet si hay bloqueo inverso (§3.8).
7. **Retroalimentación del bus apagado** a través de las entradas IN y DEN de los *high-side* (checklist de esquema): corresponde al bloque de salidas.

## Anexo A. Datos para las fichas nuevas (`hardware/componentes/`, fuera de la zona de ing-esquematicos)

| Ficha | MPN · fabricante | LCSC | Datasheet (revisión) | Pinout (página) | Símbolo / huella oficiales |
|---|---|---|---|---|---|
| LMR36520 | LMR36520FADDAR / ADDAR · TI | C1858395 / C2879422 | ti.com/lit/ds/symlink/lmr36520.pdf (SNVSBF0C) | Tabla 5-1, p. 4: 1 PGND, 2 VIN, 3 EN, 4 PG, 5 FB, 6 VCC, 7 BOOT, 8 SW, EP a PGND | Sin símbolo (usar LMR36510ADDA) / HTSOP-8-1EP 3,9 × 4,9 |
| TPS2116 | TPS2116DRLR · TI | C3235557 | ti.com/lit/ds/symlink/tps2116.pdf (SLVSFG1A) | Tabla 5-1, p. 3: 1 GND, 2/7 VOUT, 3 VIN1, 4 PR1, 5 MODE, 6 VIN2, 8 ST | `TPS2116DRL` / `SOT-583-8` |
| TLV1117LV | TLV1117LV33DCYR · TI | C15578 | ti.com/lit/ds/symlink/tlv1117lv.pdf (SBVS160C) | Tabla 5-1, p. 3: 1 GND, 2 y pestaña OUT, 3 IN | `TLV1117-33` (comprobar) / `SOT-223-3_TabPin2` |
| SQD50P06-15L | SQD50P06-15L_GE3 · Vishay | C3281500 | Vishay doc. 69098 rev. E (copia de LCSC) | p. 1: G-D-S, pestaña = D | `SUD50P06-15` / `TO-252-2` |
| 0451010.MRL | 0451010.MRL · Littelfuse | C44479 | Serie 451/453, rev. 15/06/17 (copia de LCSC) | 2 terminales | `Device:Fuse` / `Fuse_Littelfuse-NANO2-451_453` |
| FXL0650-100-M | FXL0650-100-M · Changjiang (cjiang) | C475521 | PDF de LCSC (C475521) | 2 terminales | `Device:L` / `L_Changjiang_FXL0650` |
| SS310 | SS310 · MDD | C15874 | PDF de LCSC (C15874) | K / A | `D_Schottky` / `D_SMA` |
| BZT52C15 | BZT52C15 · MDD | C173427 | PDF de LCSC (C173427) | K / A | `D_Zener` / `D_SOD-123` |
| JP1 (sin ficha de compra; huella nueva) | Puente de soldadura · — | — (fuera de BOM y CPL) | — | Pad 1 = VIN_PROT, pad 2 = BUS_24V | `Jumper:SolderJumper_2_Open` / **nueva** `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm`: pads 1,2 × 3,0 mm, hueco 0,6 mm, F.Cu y F.Mask sin pasta, máscara común (§3.13.9) |

## Anexo B. Notas para el firmware (FW-03)

- `VIN_SENSE`: `attenuation: 6dB`, `multiply: 21.534`, media de ≥ 16 muestras. Avisos a < 17 V y > 31 V.
- `LIM_IMON`: I = V / 0,279 V/A.
- Opción de configuración «sin limitador», para placas con JP1 cerrado y sin U1: ignora FLT e IMON y no usa LIM_EN para la carga abierta (§3.13.9).
- Secuencia de rearme del limitador: §3.13.3. Espera ≥ 20 ms tras habilitar el bus antes de activar canales.
