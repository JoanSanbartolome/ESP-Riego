# Estudio de coste efectivo de ESP-Riego v2 (SPEC-0037, paso 6)

**Autor:** ing-diseno · **Fecha:** 2026-11-20 · **Estado:** propuesta; lo que cambia un requisito o una decisión lo decide el usuario (columna «Decide»). **Rev. VAL-0037-01** (2026-11-23, DEC-0018): P4 queda como «LDO a elegir en SPEC-0038», P3 sin C8, P5 retirada; ahorros recalculados; procedimiento de b4 en §8.10. **Rev. SPEC-0038** (2026-11-23, jr-conformidad): P1 aplicada, U4 → AP2114H-3.3TRG1 (P4 con cifra), C3 se queda en 220 nF (usuario, DEC-0018), J10 BH254R-10P; BOM y coste recalculados en §0, §2 y §9. §1, §3–§6 conservan las cifras del 2026-11-20.
**Entradas:** BOM de `hardware/v2` (187 piezas montables, 53 líneas, campos de `hardware/componentes/campos-*.csv`), colocación `docs/diseno/colocacion-b4.csv` (100 × 100 mm), DEC-0007, DEC-0016, DEC-0017.
**Precios y stock:** API de JLCPCB (`herramientas/kicad/jlc.py`), consulta del 2026-11-20 (2026-11-23 en §0, §2 y §9); precio unitario del tramo de 5 y de 50 placas. Línea a línea: `docs/diseno/estudio-coste-bom.csv` (2026-11-23, con la columna `montaje`). BOM y CPL de prueba con los THT «a mano»: `fabricacion/v2.0-prueba/`.

## 0. Resumen

| Decisión o hallazgo | Cifra | Fuente |
|---|---|---|
| Coste por placa del estudio (2026-11-20), Economic a una cara, THT por JLCPCB (E1) | 47,15 $ con 5 uds · 25,02 $ con 50 | §1, §6 |
| **Coste por placa tras SPEC-0038** (2026-11-23): P1 + P2 (THT a mano, E2) + P3 con C3 en 220 nF + P4 | **41,96 $ con 5 uds · 23,95 $ con 50** (209,79 $ y 1 197,31 $ por pedido; 54 líneas, 20 Extended con cargo). Sin P2 (E1): 44,97 / 24,66 $ | §9; `estudio-coste-bom.csv` |
| Lo que más pesa con 5 uds: la carga de las 26 líneas Extended | 79,82 $ por pedido = **16,0 $ por placa (34 %)** | JLCPCB *PCB Assembly Price*, 2026-10-22 |
| Lo que más pesa con 50 uds: las piezas | 21,46 $ por placa (86 %) | `estudio-coste-bom.csv` |
| Bloque más caro | Alimentación: 39 % (5 uds) · Salidas: 33 % (50 uds) | §1 |
| Quitar Q1 (ALI-03) | **No recomendado.** U1 no rechaza la polaridad inversa por sí solo: necesita un N-MOSFET externo en B_GATE (SLVSE94G §8.3.5, pp. 20-21, Fig. 8-7 y 8-8). Sin protección, la entrada invertida pone en corto la fuente a través de la rueda libre M7 y del diodo del BTT6050 | §2.1 |
| Montaje | **Economic a una cara**; THT a mano por el usuario si acepta el trabajo (−3,02 $/placa con 5 uds). Dos caras (Standard): +18,2 $/placa con 5 uds | §6 |
| Rieles | Economic no los pide («Edge rails: Not necessary»); preguntar a JLCPCB por J2, U5 y J10 al ras antes del primer pedido | §7 |
| U4 (TLV1117LV33 de TI, stock 0) | **AP2114H-3.3TRG1** (C150716, Extended, 2 300 uds el 2026-11-23): 0,2386 $ con 5 uds y 0,1899 $ con 50, frente a 0,3967 / 0,2645 $ del de TI (P4, SPEC-0038; `alimentacion.md` §3.9) | §2 |
| Ahorro de lo aceptado (P1 + P2 + P3 con C3 en 220 nF + P4) | 5,19 $/placa con 5 uds · 1,07 $ con 50 (frente a 47,15 / 25,02 $) | §9 |

Colocación del paso 6: `colocacion-b4.csv`, 0 obligatorias, 58 objetivos (61 en b3), J10 horizontal al ras; E02 (D2 junto a Q1) resuelto. §8.

## 1. Método y coste por bloque

- **Montaje Economic** (JLCPCB *PCB Assembly Price*, https://jlcpcb.com/help/article/pcb-assembly-price, actualizado 2026-10-22, consultado 2026-11-20): preparación 8,18 $, plantilla 1,53 $, 0,0016 $ por junta SMT, **3,07 $ por línea Extended** (las «Extended preferidas» y las Basic no pagan), mano de obra THT 3,58 $ por pedido + 0,0164 $ por junta. Standard: preparación 25,56 / 51,12 $ (una / dos caras), plantilla 8,21 / 16,42 $, 1,53 $ por línea cargada (la tabla dice «Basic/Extend»), manipulación ≥ 14,93 $, utillaje 16,42 $ (1–29 uds) o 24,63 $ (30–99), embalaje ≈ 0,50 $.
- **Juntas:** pads con cobre de cada huella (sin las vías térmicas de los EP), de la PCB de `hardware/v2`: 585 SMT y 28 THT (J1, J4–J9, J10, J3).
- **PCB:** 2 $ por 5 uds hasta 100 × 100 mm (Z01). Para 50 uds JLCPCB no publica tarifa: se usa **15 $, estimación sin fuente vigente** (pedir presupuesto); pesa 0,30 $/placa y no cambia la comparación.
- No se cuentan el envío, los aranceles ni las piezas de reserva que JLCPCB añade a cada línea.
- La cuota Extended de una línea compartida se reparte entre los bloques por número de piezas.

| Bloque | Piezas | Líneas | Extended (cuota) | Juntas SMT / THT | BOM 5 uds ($/placa) | Montaje 5 uds | Total 5 uds | Peso | BOM 50 uds | Total 50 uds | Peso |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Alimentación | 49 | 29 | 14,95 | 136 / 2 | 9,13 | 9,43 | 18,56 | 39 % | 6,96 | 8,13 | 32 % |
| Salidas | 87 | 13 | 3,05 | 246 / 12 | 8,41 | 2,46 | 10,87 | 23 % | 7,48 | 8,26 | 33 % |
| MCU + USB | 21 | 16 | 3,33 | 101 / 4 | 5,51 | 2,27 | 7,78 | 17 % | 4,33 | 4,76 | 19 % |
| Conectores + expansión | 28 | 15 | 3,67 | 96 / 10 | 2,37 | 2,57 | 4,94 | 10 % | 1,73 | 2,27 | 9 % |
| Sensores | 2 | 2 | 1,00 | 6 / 0 | 1,31 | 0,62 | 1,93 | 4 % | 0,96 | 1,03 | 4 % |
| Común (preparación, plantilla, THT, PCB) | — | — | — | — | — | — | 3,06 | 6 % | — | 0,57 | 2 % |
| **Total** | **187** | **53** | **26** | **585 / 28** | **26,73** | | **47,15** | | **21,46** | **25,02** | |

Montaje de un bloque = cuota Extended × 3,07 $ / N + juntas SMT × 0,0016 + juntas THT × 0,0164.

**Agrupar valores no ahorra en Economic:** las Basic no pagan carga. Solo en Standard (1,53 $ por línea) compensaría unificar 4,3k/4,7k/5,1k, 470/820/1k o 68k/100k/220k/330k, y cada cambio rehace un cálculo. No se propone.

## 2. Alimentación (39 % con 5 uds)

**Coste:** 15 líneas Extended de 29: C1, C2/C6/C7/C22 (C381466), C3/C8 (C513710, compartida con salidas), D1, D2, D3, F1, J1, L1, Q1, R7/R14, R8, R15 (0,1 %), U1, U2, U3, U4. Lo caro: U1 3,52 $, U2 1,16 $, Q1 1,09 $ (tramo de 5).

**Problemas para el layout y la fabricación:**
- Cuatro fuentes de calor con cobre pedido (U1 300, U2 300, U4 400, Q1 250 mm²); en b4 todas quedan justo en el margen de +10 % (U1 331/330, Q1 276/275, U2 319/315 con +5 %).
- U1 VQFN-24 de 0,5 mm con EP y vías de 0,3/0,6 (FAB-02; la huella `_ThermalVias` no vale); JP1 a mano junto a U1.
- C1 electrolítico de 10 mm de alto: cuenta como pieza alta para pulsadores y LED (P05, L01).
- **Stock:** U4 (C15578) 0 uds, resuelto con P4 (AP2114H, 2 300 uds el 2026-11-23); U1 (C1850278) 93 uds, sin alternativa con stock (VAL-0032-01-01, §8.9).

**Soluciones:**

| Id | Propuesta | Ahorro $/placa (5 / 50 uds) | Riesgo | Requisito | Decide |
|---|---|---|---|---|---|
| P1a | D2 SMBJ33A → misma pieza de hongjiacheng C19077586 (Extended preferida, 50 264 uds; 33 V, 40,6 V, 53,3 V, 600 W, igual que la ficha). **Aplicada en SPEC-0038**; I_R 5 µA (ficha `SMBJ33A.md`) | 0,70 / 0,13 | Bajo: segunda marca; validación compara la ficha | ALI-04 | Sin consulta (DEC-0007) tras validación |
| P1b | D1 BZT52C15 → hongjiacheng C19077412 (preferida, 481 173 uds; 14,25–15,75 V, como C173427). **Aplicada en SPEC-0038**; P_D 350 mW (ficha `BZT52C15.md`) | 0,61 / 0,06 | Bajo | ALI-03 | DEC-0007 |
| P1c | D3 SS310 → hongjiacheng C7420364 (preferida, 390 469 uds; 100 V, 3 A, 850 mV). **Aplicada en SPEC-0038**; I_R 10 mA a 100 °C (ficha `SS310.md`) | 0,61 / 0,06 | Bajo | — | DEC-0007 |
| P4 | **LDO a elegir en SPEC-0038** (U4 de TI con stock 0). Tiene que cumplir: ALI-07 (≥ 800 mA); mantener 3,3 V con los 3,9 V del cambio de U3 (`alimentacion.md` §3.8), es decir, caída ≤ 0,6 V a 0,45 A en todo el rango de temperatura; estable con los cerámicos de la placa (C19 10 µF); disipar 0,81 W (SOT-223 o mejor, θJA ≈ 60 °C/W); patillaje del SOT-223 (1 GND, 2/pestaña OUT, 3 IN) si puede ser; stock en JLCPCB. **Elegido en SPEC-0038: Diodes AP2114H-3.3TRG1** (C150716, Extended, 2 300 uds; mismo patillaje; `alimentacion.md` §3.9). Descartados: TECH PUBLIC TPTLV1117LV33DCYR (C52146079) y JSMSEMI C48937499, 1117 clásicos con 1,2 V de caída (VAL-0037-01-01). Ahorro = 0,3967 − 0,2386 con 5 uds y 0,2645 − 0,1899 con 50 | **0,16 / 0,07** | Medio: R_θJA con cobre sin publicar (prueba del prototipo) | ALI-07, ALI-08 | Usuario (DEC-0018): aplicada |
| ~~P5~~ | **Retirada** (DEC-0018). R15 al 1 % daba 2,91 % a 15,5 V sin contar la caída de F1 + Q1 (0,12 V con 3,7 A, `alimentacion.md` §3.10); con ella, 3,68 % a 15,5 V y 3,49 % a 17 V, por encima del 3 % de ALI-09 (VAL-0037-01-03). R15 sigue en 4,87 kΩ al 0,1 % | 0 | — | ALI-09 | Usuario: retirada |
| P3 | C27–C38 de salidas 220 nF 100 V C513710 → 100 nF 100 V C28233 (Basic). **C3 se queda en 220 nF** (usuario, 2026-11-23, DEC-0018: con 100 nF serían 73–80 nF efectivos frente al «0,1 µF o más» del TPS2663, p. 27). **C8 se queda en 220 nF 100 V X7R**: TI lo exige, «a small case size 220-nF ceramic capacitor must be used at the input… The 220 nF must also be rated at 100-V with an X7R dielectric» (LMR36520 SNVSBF0C, p. 20; VAL-0037-01-02). La línea C513710 sigue en la BOM por C3 y C8: no se ahorra la cuota Extended. Ahorro (2026-11-23) = 12 × (0,0294 − 0,0159) con 5 uds; con 50, 12 × (0,0200 − 0,0101) menos 0,019 $, porque C3 y C8 solas caen al tramo de 1–199 uds de C513710 (0,0295 $) | **0,16 / 0,10** (12 piezas) | Bajo: C_VS 73–80 nF efectivos frente a los 100 nF de Infineon (aceptado, DEC-0018) | ALI-05, salidas.md §5 | Usuario: aceptada sin C8 (DEC-0018) |
| P7 | U3 TPS2116 → dos Schottky (ALI-08 lo admite) | 0,92 / 0,24 | Alto: +5V cae a ≈ 4,65 V (−7 %), fuera del ± 3 % de §6; no recomendado | ALI-08 | Usuario |
| P8 | U4 → AMS1117-3.3 C6186 (Basic) | por determinar (frente al LDO de P4) | Alto: caída 1,1 V a 800 mA; con 3,9 V en el cambio de U3 (§3.8) el 3,3 V cae; no recomendado | ALI-07, ALI-08 | Usuario |
| — | R7/R8 al 1 % | — | VOUT ± 3,1 %, no cumple (`alimentacion.md` §3.6): se quedan al 0,1 % | — | No se propone |

### 2.1 Quitar Q1 (ALI-03)

**Qué dice el datasheet de U1 (TPS2663, SLVSE94G, junio de 2024):**
- p. 1: «Reverse polarity protection and reverse current blocking **support with an external N-channel FET**».
- §8.3.5, pp. 20-21: el rechazo de la polaridad inversa necesita un N-MOSFET de potencia (Q1 de TI) entre IN_SYS e IN, gobernado por B_GATE, y un FET de señal en DRV (Fig. 8-7). Sin ellos, IN e IN_SYS van juntos y B_GATE y DRV quedan abiertos (Fig. 8-8), que es como está la placa (`alimentacion.md` §0: B_GATE y DRV sin conectar).
- §6.1, p. 5: IN e IN_SYS aguantan −60 V. U1 sobrevive, pero su FET interno (drenador en IN, fuente en OUT) tiene el diodo de cuerpo de OUT a IN: con la entrada invertida, BUS_24V sigue a la entrada menos un diodo.

**Qué pasa sin Q1 y sin otra protección**, con la entrada a −24 V:
- BTT6050: «During reverse polarity, no protection functions are available» (§6.4, p. 19); −V_S(REV) ≤ 28 V durante < 2 min solo con los componentes externos de la Fig. 17 (P_4.1.2). En esta placa, GND → M7 (ánodo a GND, cátodo a OUT) → diodo de cuerpo del BTT (OUT → VS) → bus: dos diodos en directa entre los polos de la fuente. Corto franco: actúa la fuente o F1, y las M7 y los BTT disipan la corriente de corto.
- D2 (SMBJ33A unidireccional) conduce en directa: otro corto.
- C1 (electrolítico) queda polarizado al revés; U2 tiene VIN ≥ −0,3 V (LMR36520 SNVSBF0C §6.1, p. 5).

**Opciones:**

| Opción | Piezas | Ahorro $/placa (5 / 50) | Placa | ALI-03 |
|---|---|---|---|---|
| A. Mantener Q1 + D1 + R1 (actual) | — | 0 | Q1 TO-252 (77,7 mm² de patio) + 250 mm² de cobre | Cumple |
| B. N-MOSFET en B_GATE de U1 (Fig. 8-7; TI usa CSD19537Q3, ≥ 80 V) + FET de señal (BSS138 C7420339, preferida) en el camino del bus; Schottky en serie solo para la lógica (SS210 C14996, Basic; 0,2 A × 0,6 V = 0,12 W); D2 → SMBJ33CA bidireccional (C19077587, preferida); ≥ 300 kΩ entre UVLO e IN_SYS (p. 20); C1, divisores R9/R10 y R14/R15 detrás del Schottky | −Q1, −D1, −R1, +4 piezas | ≈ 0,5 / ≈ 0,4 (el N-MOSFET es Extended, sin cotizar) | Libera ≈ 150–200 mm² (FET de 3,3 × 3,3 mm con la mitad de disipación) | Cumple con el texto nuevo |
| C. Sin protección | −Q1, −D1, −R1 | 2,34 / 1,05 | Libera ≈ 370 mm² (3,7 % de la placa): Q1, D1, R1 y su anillo de cobre | **No cumple; destruye la placa** (arriba) |

`alimentacion.md` §2 ya descartó la B tal cual: el FET de B_GATE se apaga con SHDN y con el UVLO del limitador, y el buck quedaría alimentado por su diodo (SLVSE94G §8.3.13, p. 28). La B de esta tabla lo evita con el Schottky propio de la lógica, a cambio de rehacer el UVLO del buck (−0,6 V de caída) y la medida de VIN (ALI-06, ALI-09).

**Recomendación:** **A, mantener Q1.** El ahorro de B (≈ 0,5 $) no paga rehacer ALI-06, ALI-09 y el bloque, y C no es aceptable. Si el usuario quiere B, texto propuesto para ALI-03:

> ALI-03 | M | Protección contra inversión de polaridad de bajas pérdidas en el camino de las salidas (P-MOSFET, controlador de diodo ideal o el N-MOSFET de bloqueo del limitador), dimensionada para la corriente de entrada de ALI-12. El camino de la lógica (≤ 0,2 A) puede llevar un diodo Schottky en serie. Con la entrada invertida, ninguna pieza conduce (TVS bidireccional).

**A tener en cuenta:** Q1 sigue sin protección frente a transitorios negativos de más de ≈ 36 V (`alimentacion.md` §3.3, limitación aceptada).

## 3. Salidas (33 % con 50 uds)

**Coste:** 6 × BTT6050 (1,09 $; 1 604 uds) = 6,55 $ de 8,41 $. Extended: BTT6050, C513710, C381466 (C45/C46) y J4–J9 (C8465, compartida con J1).

**Problemas:**
- Seis TDSO-14 con EP y 10 vías cada uno, 300 mm² de cobre por canal (+10 %): es lo que llena la placa. En b4, U10 330/330, U11 y U12 332/330: sin margen para pistas o vías nuevas.
- Separación de 0,6 mm de FAB-03 dentro de las huellas (DEC-0008).
- Bornes de 14 mm de alto en los dos bordes: condicionan pulsadores y LED (P05, L01, O04).
- Las R_IN/R_DEN/R_IS (O10, O11) quedan a 5–15 mm de U5: 15 objetivos sin cumplir.

**Soluciones:**

| Id | Propuesta | Ahorro $/placa (5 / 50) | Riesgo | Requisito | Decide |
|---|---|---|---|---|---|
| P3 | C_OUT C33–C38 → 100 nF 100 V Basic (Infineon propone 10 nF, Tabla 11, p. 48: mejora τ de la carga abierta); C_VS también (73–80 nF efectivos, DEC-0018) | incluido en P3 | Bajo | salidas.md §5 | Usuario / validación |
| P2 | J4–J9 a mano (escenario E2) | incluido en P2 | Trabajo del usuario: 12 juntas por placa | FAB-06 | Usuario |
| P9 | Cobre de 2 oz (FAB-01, D6) para recuperar margen térmico sin crecer | coste por presupuesto | Precio de la PCB | FAB-01, D6 | Usuario |

**A tener en cuenta:** no hay alternativa Basic ni preferida para el BTT6050 ni para el 4,7 µF 100 V (memoria de proyecto y búsqueda del 2026-11-20).

## 4. Microcontrolador y USB (17–19 %)

**Coste:** U5 ESP32-S3-WROOM-1-N8 4,91 $ (4 384 uds); J2 TYPE-C-31-M-12 0,19 $ (Extended); U6 USBLC6 (C7519, compartida); J3 (C124378, THT Extended).

**Problemas:**
- Zona sin cobre de la antena: 298 mm² dentro de la placa (§8.4).
- J2 al ras del borde (B12) y U5 con la antena al ras (A01): la pregunta de los rieles (§7).
- USB: par diferencial de 90 Ω ± 10 % y referencia continua (HDG §1.4.8, p. 30); en 2 capas de 1,6 mm hay que calcular el coplanar con plano.
- Desacoplos de U5 a 0,11–0,18 mm de su patio (F02): sin sitio para vías por ese lado.

**Soluciones:**

| Id | Propuesta | Ahorro $/placa (5 / 50) | Riesgo | Requisito | Decide |
|---|---|---|---|---|---|
| P2 | J3 a mano (E2) | incluido en P2 | Bajo | FAB-06 | Usuario |
| P10 | U5 N8 → N8R2 (C2913204, 10 188 uds, 3,84 $ a 50) si hiciera falta PSRAM | +0,01 | — | MCU-01 | No se propone |

**A tener en cuenta:** el módulo no tiene sustituto Basic; el stock de 4 384 da para 50 placas.

## 5. Conectores con expansión (9–10 %) y sensores (4 %)

**Coste:** TCA9554 0,83 $, 2 × TPS2553 0,46 $, 2 × USBLC6, J10 (pasa de BH254V C492442 a **BH254R-10P C492448**, la misma cuota Extended y 0,116 $ a 50 uds; ficha `hardware/componentes/BH254R-10P.md`), SHT40 1,31 $.

**Problemas:**
- J10 horizontal: su patio tiene 15,1 mm de fondo frente a 9,9 del vertical, aunque ya no necesita los 2,5 mm al borde: ocupa ≈ 2,7 mm más hacia dentro. Su altura (8,9 mm de cuerpo, ≈ 6,0 mm en los codos de los pines) sigue por encima de 5 mm: **P05, E08 y L01 no cambian de cifra** (recalculado en las reglas). Lo que sí gana: el cable sale por el borde y la clavija no tapa nada.
- Fila de U14–U17 entre la rejilla de resistencias y J10, con 0,5 mm justos a cada lado (F02); U16 junto a H4.
- Pulsadores a 10,2 mm de paso frente a 12,7 (P02, objetivo).
- SHT40: S02–S04 sin cumplir (mismo lateral que la antena, 22,9 mm de las fuentes de calor y 17,5 de U5); la isla con ranuras no está aún en `Edge.Cuts`.

**Soluciones:**

| Id | Propuesta | Ahorro $/placa (5 / 50) | Riesgo | Requisito | Decide |
|---|---|---|---|---|---|
| P2 | J10 a mano (E2) | incluido en P2 | Bajo | FAB-06 | Usuario |
| P11 | Alternativa de J10: ZHOURI DC3-2.54-10PAL (C5156674, 0,079 $) | 0,04 / 0,04 | Medio: 1,5 A, cotas a confirmar en la misma huella | EXP-02 | DEC-0007 tras validación |
| P12 | P02: aceptar 10,2 mm de paso (las teclas solo se usan con la caja abierta, EXP-03) | — | Bajo | EXP-03 | Usuario |

## 6. Montaje por una cara frente a dos, y THT

Clases de JLCPCB (*PCB Assembly Capabilities*, https://jlcpcb.com/capabilities/pcb-assembly-capabilities, consultado 2026-11-20): **Economic** coloca una sola cara («Single sided placement (SMT/Thru-hole)»), 0402 como mínimo, de 2 a 50 uds, rieles y fiduciales «Not necessary». **Standard**, una o dos caras, rieles y fiduciales «Necessary», placa ≥ 70 × 70 mm. El THT se suelda a mano u ola (FAQ); no hay tarifa de selectiva. La página no dice si el THT puede ir con el cuerpo en la cara inferior.

| Escenario | Qué incluye | 5 uds: total · por placa | 50 uds: total · por placa |
|---|---|---|---|
| **E1** Economic, una cara, SMT + THT por JLCPCB (actual) | 26 Extended; 28 juntas THT | 235,73 $ · **47,15 $** | 1 251,07 $ · **25,02 $** |
| **E2** Economic, una cara, SMT por JLCPCB; J1, J4–J9, J10 y J3 comprados y soldados por el usuario | 23 Extended (sin C8465, C492442, C124378); sin THT | 220,64 $ · **44,13 $** | 1 215,32 $ · **24,31 $** |
| **S2** Standard a dos caras, THT por JLCPCB | 53 líneas × 1,53 $, preparación y plantilla de dos caras, manipulación, utillaje | 326,68 $ · **65,34 $** | 1 350,23 $ · **27,00 $** |

**Pasar piezas a la cara inferior:**
- Bornes, J10 y J3 abajo: FAB-06 (M) pide los THT arriba, la clavija y los tornillos quedarían hacia la caja y los pulsadores tienen que verse con la caja abierta (EXP-03). Pulsadores abajo: no se alcanzan. C1 (SMD) abajo: obliga a Standard (S2).
- Área que se liberaría: bornes 797 mm², J10 323, J3 41, C1 92, pulsadores 346: ≈ 1 600 mm² (16 % de la placa), pero bajo los THT la cara superior solo queda libre entre pines.
- Cuesta +18,2 $/placa con 5 uds y +2,0 $ con 50 frente a E1, y cambia FAB-06.

**Recomendación:** Economic a una cara. **E2** si el usuario acepta soldar 28 juntas por placa (≈ 15 min); con 50 uds el ahorro baja a 0,72 $/placa y E1 es razonable.

## 7. Rieles por J2, U5 y J10 al ras

- **Economic:** «Edge rails / Fiducials: Not necessary» (capacidades PCBA, consultado 2026-11-20). JLCPCB paneliza los pedidos Economic y fresa con ± 0,2 mm; recomienda pistas y piezas a > 0,3 mm del borde (*PCB Assembly FAQs (Part 2)*, P14, https://jlcpcb.com/help/article/pcb-assembly-faqs-part-2, actualizado 2026-09-09).
- **Términos** (https://jlcpcb.com/help/article/terms-and-conditions-of-jlcpcb-assembly-service, actualizado 2026-09-09): §2.3 pide 2,5 mm del cuerpo al borde; §5.5 dice que, si los rieles faltan o no valen, JLCPCB «will help to add or modify them by default», sin precio; §5.14, que sin rieles elige el método (p. ej., *mouse bites*).
- **Rieles** (*How to add edge rails/fiducials*, actualizado 2026-09-09): ≥ 5 mm; la placa se entrega con ellos puestos y quitarlos tiene un cargo sin publicar.
- **Coste si los pide:** J2/U5 en el borde izquierdo y J10 en el inferior → rieles en los dos ejes, panel de 110 × 110 mm, fuera del precio especial de ≤ 102 × 102 (*In what cases will there be charged extra*, actualizado 2026-11-10). Con rieles solo arriba y abajo (los bordes que van por la cinta) basta para J10, y J2/U5 quedan en bordes que no tocan la guía: 100 × 110 mm, también por encima de 102. Sin tarifa publicada: presupuesto.
- **Alternativas sin rieles:** (a) **Economic tal cual**, con una nota en el pedido («J2, U5 y J10 a < 2,5 mm del borde, a propósito») y la boca de J2 y J10 a 0,3–0,5 mm del borde (P14) en lugar de 0–0,5 mm; (b) panel propio no ayuda: añade el mismo área; (c) placa de 100 × 90 mm + 2 rieles de 5 mm = 100 × 100: no cabe con la densidad actual. Mover el *V-cut* no aplica a una placa suelta (JLCPCB fresa el contorno).

**Recomendación:** (a). Decide el usuario; confirmar con JLCPCB antes del primer pedido. Para (a), la regla `ras` necesitaría un mínimo de 0,3 mm (hoy 0…0,5): cambio de herramienta en otra spec.

## 8. Fallos abiertos de la colocación (b4)

| # | Fallo | Solución propuesta | Decide |
|---|---|---|---|
| 8.1 | E02: D2 a 27 mm de Q1 | **Resuelto en b4:** D2 entre U1 y Q1, a 0,1 mm del patio de Q1, fuera del anillo de U1; D1 y R1 junto a la puerta de Q1 (W03); R2/C4 bajo U1. E01 (D2, Q1, F1 a ≤ 10 mm del borde inferior) sigue: D2 a 25,6 mm | — |
| 8.2 | O13: C46 lejos de U10–U12 | Cualquier sitio a ≤ 10 mm de un BTT de abajo cae en su anillo de cobre, y U10–U12 están a 330–332/330: no cabe sin bajar el margen. Propuestas: (a) dejar C46 arriba, junto a TP5/U9, y cambiar O13 a «≤ 10 mm de U7–U12» (la energía de desmagnetización va a la rueda libre M7, no al bus; C_VS local de 220 nF); (b) margen de +5 % para U10–U12 y C46 entre U11 y U12 | Usuario (a recomendada) |
| 8.3 | 58 objetivos (61 en b3) | U5 y canales: O10 3 + O11 12 + F02 6 (desacoplos de U5 a 0,11–0,18 mm de su patio): pasar O10/O11 a «≤ 15 mm» y eximir de F02 los pasivos junto al módulo (sus pads están en el borde contrario). Sensor: S02 + S03 + S04 (3): se resuelven con la isla y la caja (D5). Pulsadores: P02 5 (§5, P12). Alimentación: E01 3, E04 2, E05 4 (U1 no admite más piezas en su anillo: Q13 manda), D01/D04/D06 4. Conectores: C02 5, C05 2, C07 1 (R79 junto al MCU por la red INT: reescribir la regla), B10 1 (J10 a la izquierda de J7–J9: `conectores.md` §4 permite cambiar el orden), L01 1 (D9 entre J10 y J7, sin sitio a 3 mm de los dos), O04 1, M05 1, A04 1 (J3 a 9,8 mm de la antena), R01 1 (§7), T04 1 (§8.5) | Coordinador (reescritura de reglas) |
| 8.4 | Zona prohibida de U5: 15 mm a los dos lados de la antena | HDG Fig. 26, p. 31: módulo en una esquina, con el lado del punto de alimentación a ≤ 2 mm del borde, la antena a ≤ 1 mm del otro y ≥ 15 mm libres solo en el lado contrario, recortando la placa (≈ 15 × 6 mm). Cambia la huella (`esp-riego:ESP32-S3-WROOM-1`, zona de un solo lado) y `Edge.Cuts`; J2 sale de debajo de la zona. Ganancia: de 298 mm² de zona dentro de la placa a casi 0. Comprobar el lado del punto de alimentación en el dibujo del módulo | Usuario + otra spec (D5) |
| 8.5 | Textos «1» y «2» de 0,8 mm en la huella de JP1 (T04) | Subirlos a 1,0 mm de alto y 0,15 mm de trazo, o quitarlos (JP1 no tiene polaridad), en `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` | Otra spec (librería) |
| 8.6 | Margen del cobre +10 % / +5 % en lugar de +20 % | En b4 todo está en el límite (U10 330/330, U1 331/330, Q1 276/275, U2 319/315): cualquier vía o pista nueva lo rompe. Opciones: aceptar y comprobar con el rutado; cobre de 2 oz (D6); o una placa mayor (DEC-0016 la descarta) | Usuario |
| 8.7 | `checklists/layout.md`, l. 44 y l. 46 | l. 46: «Serigrafía legible (≥ 0,8 mm)» → «Serigrafía legible: alto ≥ 1,0 mm y trazo ≥ 0,15 mm (JLCPCB *PCB Capabilities*, Legend; DEC-0016)». l. 44: «Fiduciales para montaje SMT» → «Fiduciales si el montaje es Standard (Economic no los pide: JLCPCB *PCB Assembly Capabilities*)» | Coordinador |
| 8.8 | Lo que no se comprueba en texto (parte 06) | Rutado real y cara inferior: en la spec de rutado, con KiCad y DRC (`corte` es una estimación en línea recta). Altura e isla del SHT40: añadir las ranuras a `Edge.Cuts` y medirlas. Caja (D5): pendiente. Legibilidad: `vista.py` con zoom. Valores de F.Fab solapados: no se fabrican; ocultarlos o ignorarlos | Coordinador |
| 8.9 | VAL-0032-01-01: U1 sin alternativa | TPS26632**RGET** (C2862529, 34 uds, 2,72 $): el mismo silicio en bobina de 250; con RGER suman 127. TPS26631RGER (C1850273, 294 uds, 8,46 $): con OVP a GND da el corte fijo de 34,3 V (SLVSE94G §8.3.4, p. 19) en lugar del *clamp* de 35 V, y es la variante de pulso 2× (tabla de comparación, p. 2): cambia la coordinación con la fuente (ALI-13) y +5,8 $/placa. TPS26630RGER (19 uds TI; 30 del clon Tokmas sin datos): descartados. Recomendación: RGET como segunda fuente y reservar stock antes del pedido | Usuario (coste) + validación |
| 8.10 | b4 solo vale con J10 horizontal (VAL-0037-01-04) | `evaluar` de b4 sobre `hardware/v2` da 13 obligatorias, porque `hardware/v2` lleva aún la huella vertical de J10. Para reproducir b4: copia de `hardware/v2` con `hardware/libraries` al lado; en la copia de `conectores.kicad_sch`, J10 con `Footprint` = `Connector_IDC:IDC-Header_2x05_P2.54mm_Horizontal` (y `Value`, `MPN` y `LCSC Part#` de BH254R-10P, C492448); `python herramientas/kicad/sincronizar.py <copia>/v2 -o <copia>/v2/esp-riego.kicad_pcb` (recarga J10 con sus redes, paridad 0); `python herramientas/kicad/colocacion.py evaluar <copia>/v2 docs/diseno/colocacion-b4.csv` → 0 obligatorias, 58 objetivos, PUNTOS 6251. **Criterio de SPEC-0038:** tras aplicar J10 BH254R-10P, `evaluar` de b4 sobre `hardware/v2` con 0 obligatorias | Coordinador (SPEC-0038) |

## 9. Resumen de propuestas, por ahorro con 5 uds

| Id | Propuesta | Ahorro $/placa 5 uds | 50 uds | Riesgo | Requisito | Decide |
|---|---|---|---|---|---|---|
| P2 | THT a mano (E2) | 3,02 | 0,72 | Trabajo del usuario | FAB-06 | Usuario |
| — | Quitar Q1 sin protección | 2,34 | 1,05 | **Inaceptable** (corto con la entrada invertida) | ALI-03 | No se propone |
| P1 | D1, D2, D3 a sus equivalentes preferidas | 1,93 | 0,25 | Bajo | ALI-03, ALI-04 | Aplicada (SPEC-0038) |
| P7 | U3 → dos Schottky | 0,92 | 0,24 | Alto (+5V −7 %) | ALI-08 | Usuario (no recomendada) |
| B | Q1 → N-MOSFET en B_GATE + Schottky de lógica | ≈ 0,5 | ≈ 0,4 | Alto (rehace el bloque) | ALI-03, ALI-06, ALI-09 | Usuario (no recomendada) |
| P3 | C27–C38 → 100 nF 100 V Basic (C3 y C8 siguen en 220 nF) | 0,16 | 0,10 | Bajo | ALI-05, salidas | Usuario: aceptada (DEC-0018); aplicada |
| P11 | J10 → ZHOURI | 0,04 | 0,04 | Medio | EXP-02 | DEC-0007 + validación |
| P4 | U4 → AP2114H-3.3TRG1 (C150716; stock 0 de la de TI) | 0,16 | 0,07 | Medio | ALI-07, ALI-08 | Aplicada (SPEC-0038) |
| P8 | U4 → AMS1117 | por determinar | — | Alto | ALI-07 | Usuario (no recomendada) |
| ~~P5~~ | R15 al 1 % | 0 | 0 | ALI-09 en 3,68 % con la caída de F1 + Q1 | ALI-09 | Retirada (DEC-0018) |
| 8.9 | U1 RGET como segunda fuente | −0,04 | −0,04 | Bajo | ALI-13 | Usuario |
| §7 | Rieles (si JLCPCB los exige) | coste sin publicar | — | — | DEC-0016 | Usuario |
| S2 | Dos caras (Standard) | −18,19 | −1,98 | — | FAB-06 | No se propone |

Estimación del 2026-11-20, con P1 + P2 + P3 sin C8 (lo aceptado en DEC-0018): 47,15 − 1,93 − 3,02 − 0,18 = 42,02 $/placa con 5 uds; con 50 uds, 25,02 − 0,25 − 0,72 − 0,05 = 24,00 $.

**Recalculado tras SPEC-0038** (BOM de `hardware/v2`, precios del 2026-11-23, escenario E2, mismo modelo de §1; `estudio-coste-bom.csv`): **41,96 $/placa con 5 uds** (209,79 $ por pedido) y **23,95 $ con 50** (1 197,31 $). 187 piezas, 54 líneas (C28233 entra como línea nueva), 20 Extended con cargo (23 con E1), 585 juntas SMT; 28 THT a mano (J1, J3, J4–J9, J10).

| Diferencia frente a 42,02 / 24,00 $ | 5 uds | 50 uds |
|---|---|---|
| P4: U4 AP2114H (0,2386 / 0,1899 $) frente al TLV1117LV de TI (0,3967 / 0,2645 $) | −0,16 | −0,07 |
| J10 BH254R-10P C492448 (0,1476 / 0,1164 $) frente al BH254V C492442 (0,1176 / 0,0937 $) | +0,03 | +0,02 |
| P3 real frente a la estimación: C3 se queda en 220 nF (12 piezas en lugar de 13: +0,014 con 5 uds); con 50, C28233 cae al tramo de 600 uds (0,0101 $ en lugar de 0,0159) y C3 + C8 suben al tramo de 1–199 uds (+0,019) | +0,02 | −0,05 |
| Precios del 2026-11-20 al 2026-11-23 en el resto (U5 +0,013, BTT6050 6 × +0,003, C15849 +0,014, U1 +0,009, U14/U15 −0,011…) | +0,05 | +0,04 |
| **Total** (con el redondeo de 47,15 y 25,02) | **−0,06** | **−0,05** |
