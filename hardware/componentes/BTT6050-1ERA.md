---
mpn: BTT6050-1ERA
fabricante: Infineon Technologies
funcion: interruptor inteligente *high-side* de 1 canal, 24 V, 50 mΩ, con medida de corriente (salidas, DEC-0003)
lcsc: C534868
tipo_jlcpcb: extended
stock_consultado: 2026-11-10
datasheet: https://www.infineon.com/assets/row/public/documents/10/49/infineon-btt6050-1era-datasheet-en.pdf
datasheet_espejo: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Infineon-Technologies-BTT6050-1ERA_C534868.pdf
datasheet_local: datasheets/BTT6050-1ERA.pdf (Rev. 1.00, 2019-03-09, 1,7 MB, idéntica byte a byte a la de infineon.com, revisión vigente comprobada el 2026-11-05)
simbolo: esp-riego:BTT6050-1ERA
huella: esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm
modelo_3d: ${KIPRJMOD}/../libraries/3d/Infineon_PG-TDSO-14.step
origen_assets: creado
verificado_por: pendiente (ing-validacion; SPEC-0024 modifica la huella: vías del EP)
---

# BTT6050-1ERA · *high-side* 1 canal

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Tensión de funcionamiento | V_NOM 8–36 V (típ. 28 V); V_S(OP) ampliado 5–48 V (Tabla 4, p. 8). La Tabla 1 (p. 2) resume «5 V … 36 V». V_S > 48 V solo con JP1 cerrado y durante el impulso de la TVS: cubierto por V_S(LD) = 65 V | Tabla 4, p. 8; Tabla 1, p. 2 |
| Tensión máxima V_S(LD) (*load dump*) | 65 V | Tabla 1, p. 2 |
| R_DS(ON) máx. a T_J = 150 °C | 100 mΩ (50 mΩ típ.) | Tabla 1, p. 2 |
| Corriente nominal I_L(NOM) | 4,5 A | Tabla 1, p. 2 |
| Limitación mínima I_L5(SC) | 38 A | Tabla 1, p. 2 |
| Relación de sentido de corriente k_ILIS | 1 500 típ. (1 600 por debajo de 0,1 A en el firmware) | Tabla 1, p. 2 |
| Corriente en reposo I_S(OFF) | 0,5 µA máx. (T_J = 25 °C) | Tabla 1, p. 2 |
| Entradas lógicas | compatibles con 3,3 V y 5 V (V_IN(H) = 2,0 V máx.) | p. 2; Tabla 10, p. 34 |
| Diagnóstico | IS analógico, carga abierta ON/OFF, corto a GND/V_S, sobretemperatura | p. 2 |
| R_thJA | 50 K/W con ≥ 300 mm² de cobre en VS (Fig. 7) | p. 10 |
| Encapsulado | PG-TDSO-14 con *tab* (VS) | §11, p. 49 (Fig. 53) |

### Errata del datasheet (P_7.5.2, p. 30)

La condición de P_7.5.2 (umbral de carga abierta en ON, I_L(OL) = 4…25 mA) dice «I_IS(OL) = 8 mA». **Se lee 8 µA**: 8 mA superaría I_IS(FAULT) mín. (6 mA), y 4–25 mA / k_ILIS (1 600) = 2,5–16 µA encierra 8 µA (razonamiento en `docs/diseno/salidas.md` §3.2). Con R_IS = 820 Ω, el máximo de V_IS en carga abierta es 8 µA × 828 Ω + 10 mV = 16,6 mV. No hay *erratum* publicado por Infineon: es una lectura nuestra, por confirmar en el prototipo (`salidas.md` §13.7).

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| 1, 2, 7, 8, 9, 13, 14 | NC | Sin conexión interna |
| 3 | GND | Masa lógica |
| 4 | IN | Entrada de activación |
| 5 | DEN | Habilitación del diagnóstico |
| 6 | IS | Salida de sentido de corriente y diagnóstico |
| 10, 11, 12 | OUT | Salida protegida (los tres pines unidos en la placa) |
| *Tab* (pad 15 de la huella) | VS | Alimentación (BUS_24V); es el disipador |

Tabla 2, p. 4. Símbolo `esp-riego:BTT6050-1ERA`: 15 pines (4 IN, 5 DEN, 6 IS, 3 GND, 15 VS, 10–12 OUT apilados y 7 NC apilados), comprobados frente a esta tabla el 2026-11-10.

**BTT6030-2ERA tiene la misma huella pero otro pinout (1 GND, 2 IN0, 3 DEN, 4 IS, 5 DSEL, 6 IN1, 8-10 OUT1, 12-14 OUT0): no es intercambiable sin rehacer el *routing*** (`BTT6030-2ERA.md`, `salidas.md` §10).

## Recomendaciones de layout del fabricante

- Los tres pines OUT se unen en la placa y la pista debe soportar la corriente máxima (nota 1 de la Tabla 2, p. 4).
- El *tab* VS es el camino térmico: cobre grande conectado a VS bajo y alrededor; el datasheet simula con 600 mm² de cobre de refrigeración y 2s2p con una matriz de vías bajo el pad expuesto (§4.3.1, Figuras 4 y 5, p. 9-10; sin cotas de las vías). El *land pattern* de Infineon (`infineon.com/package/PG-TDSO-14-11`) no publica vías.
- **Vías del EP:** la huella `esp-riego:Infineon_PG-TDSO-14_…_EP2.65x6.4mm` lleva 10 vías de 0,3 / 0,6 mm numeradas 15 (rejilla 1,9 × 1,2 mm, FAB-02). **Van a un polígono BUS_24V en la cara inferior, no al plano de GND** (el *tab* es VS). Con ≥ 300 mm² de cobre en VS por BTT (`salidas.md` §11).
- Esquema de aplicación del fabricante (p. 1 y Tabla 11, p. 48): R_IN, R_DEN, R_IS, C_VS (100 nF) y, además, R_GND (27 Ω) con diodo y zéner de 58 V en VS. **En este proyecto no se montan R_GND ni zéner en VS** (`salidas.md` §4.4): la polaridad inversa la bloquea Q1, V_S ≤ 53,3 V queda por debajo de V_S(AZ) = 65 V mín. (Tabla 7, p. 22), I_GND ≤ 9 mA y una R_GND restaría margen a V_IN(H). C_VS = 220 nF 100 V (C513710).

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| BTT6030-2ERA | C534865 | 2 canales, 30 mΩ; **misma huella, distinto pinout**; Extended, 10 571 el 2026-11-10 |
| BSP752R | C112644 | 1 canal, 200 mΩ, sin medida de corriente (ST digital) |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-10)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas (30 uds) | 10 placas (60 uds) |
|---|---|---|---|---|---|
| C534868 | Extended | 1 628 | 1–9: 1,2763 · 10–29: 1,165 · 30–99: 1,0947 · 100–499: 1,0227 · 500–999: 0,9916 | 32,84 $ | 65,68 $ |

6 canales por placa (`salidas.md` §9): 60 de 1 628 uds. para 10 placas (3,7 %); margen limitado (el stock bajó de 1 698 el 2026-11-05 a 1 628).

## Notas de los assets

El símbolo y la huella se han creado desde el datasheet: no hay versión en la librería oficial de KiCad 10 ni en PartReel, y la API de EasyEDA no está accesible desde aquí. La huella usa el *land pattern* oficial de Infineon para el encapsulado PG-TDSO-14-11 (https://www.infineon.com/package/PG-TDSO-14-11, imagen «footprint», consultada el 2026-11-05) y el dibujo de la p. 49 para el cuerpo (ver el log de SPEC-0015).

**Vías del EP (SPEC-0024, 2026-11-10; pasta corregida tras VAL-0024-01).** 10 vías `thru_hole` de taladro 0,3 y diámetro 0,6 mm (FAB-02), numeradas 15, en x = ±0,95 e y = −2,4, −1,2, 0, 1,2, 2,4 mm (el anillo queda a ≥ 0,075 mm del borde del EP y a 0,5 mm de los extremos). Distancia entre taladros 0,9 mm: cumple las dos reglas de JLCPCB (jlcpcb.com/capabilities/pcb-capabilities), vía a vía 0,2 mm y «Pad Hole-to-Hole Spacing» 0,45 mm (las vías son pads `thru_hole`). Capas `*.Cu` sin capas de máscara: sin apertura de máscara en B.Cu; JLCPCB no garantiza el tapado de vías con apertura en F.Mask (las vías quedan dentro de la apertura del pad 15), así que quedan abiertas por arriba y su estado real se comprueba en los Gerber de la fase 5. Pad 15 también en B.Cu (2,65 × 6,4, sin máscara) y `zone_connect 2` (conexión sólida) en el pad y en las vías, como las huellas oficiales `*_ThermalVias` de KiCad. Pasta: 14 ventanas a ≥ 0,10 mm del taladro, 11,03 mm² = 65 % del EP (frente al 85 % de la versión sin vías): 2 de 1,40 × 2,95 en (0; ±1,625), 8 de 0,375 × 0,70 en (±1,0875; ±0,60 y ±1,80) y 4 de 0,375 × 0,45 en (±1,0875; ±2,875). Vías sin relleno (no cambia el coste). Pads 1–14, tamaño del EP, serigrafía, patio y 3D sin cambios.

**Modelo 3D** (`Infineon_PG-TDSO-14.step`, compartido con el BTT6030-2ERA): creado con SolidCraft (fuentes en `hardware/libraries/3d/fuentes-solidcraft/`). Origen = origen de la huella, Z = 0 en la cara superior de la placa, offset 0, rotación 0 y escala 1. Cotas del datasheet (Figura 53, p. 49): cuerpo 8,65 × 3,9, altura máxima 1,15 con *standoff* de 0,05, pad expuesto 2,65 × 6,4, patillas de 0,4 de ancho a 1,27 de paso con puntas a ±3,0. Supuestos: patillas rectas de 0,2 de grosor y pie de 0,67 modelado desde |x| = 2,3; cuerpo prismático (sin ángulo de flanco); cuerpo hasta 1,15 (máximo, no la cota de referencia de 0,95); marca del pin 1 como hendidura de Ø 0,8 × 0,1 junto al pad 1 (sin cotas en el dibujo). Comprobado con `kicad-cli pcb render` (SPEC-0015 y SPEC-0024, `render_SPEC-0024_top.png` y `_bottom.png`): patillas sobre sus pads, marca junto al pad 1 y vías del EP visibles por debajo.

## Uso en el proyecto

DEC-0003. U7–U12 en `salidas.kicad_sch` (un canal por chip, canales 1–6; 3 por borde, REL-09). Principal; sin R_GND ni zéner en VS (§4.4); *tab* a BUS_24V con las vías de la huella.
