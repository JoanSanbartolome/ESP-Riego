---
mpn: BTT6050-1ERA
fabricante: Infineon Technologies
funcion: interruptor inteligente *high-side* de 1 canal, 24 V, 50 mΩ, con medida de corriente (salidas, DEC-0003)
lcsc: C534868
tipo_jlcpcb: extended
stock_consultado: 2026-11-05
datasheet: https://www.infineon.com/assets/row/public/documents/10/49/infineon-btt6050-1era-datasheet-en.pdf
datasheet_espejo: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Infineon-Technologies-BTT6050-1ERA_C534868.pdf
datasheet_local: datasheets/BTT6050-1ERA.pdf (Rev. 1.00, 2019-03-09, 1,7 MB, idéntica byte a byte a la de infineon.com, revisión vigente comprobada el 2026-11-05)
simbolo: esp-riego:BTT6050-1ERA
huella: esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm
modelo_3d: ${KIPRJMOD}/../libraries/3d/Infineon_PG-TDSO-14.step
origen_assets: creado
verificado_por: pendiente (ing-validacion)
---

# BTT6050-1ERA · *high-side* 1 canal

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Tensión de funcionamiento V_S(OP) | 5…36 V (hasta 48 V según el estudio de salidas) | Tabla 1, p. 2 |
| Tensión máxima V_S(LD) (*load dump*) | 65 V | Tabla 1, p. 2 |
| R_DS(ON) máx. a T_J = 150 °C | 100 mΩ (50 mΩ típ.) | Tabla 1, p. 2 |
| Corriente nominal I_L(NOM) | 4,5 A | Tabla 1, p. 2 |
| Limitación mínima I_L5(SC) | 38 A | Tabla 1, p. 2 |
| Relación de sentido de corriente k_ILIS | 1 500 típ. | Tabla 1, p. 2 |
| Corriente en reposo I_S(OFF) | 0,5 µA máx. (T_J = 25 °C) | Tabla 1, p. 2 |
| Entradas lógicas | compatibles con 3,3 V y 5 V | p. 2 |
| Diagnóstico | IS analógico, carga abierta ON/OFF, corto a GND/V_S, sobretemperatura | p. 2 |
| Encapsulado | PG-TDSO-14 con *tab* (VS) | §11, p. 49 |

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| 1, 2, 7, 8, 9, 13, 14 | NC | Sin conexión interna |
| 3 | GND | Masa lógica |
| 4 | IN | Entrada de activación |
| 5 | DEN | Habilitación del diagnóstico |
| 6 | IS | Salida de sentido de corriente y diagnóstico |
| 10, 11, 12 | OUT | Salida protegida (los tres pines unidos en la placa) |
| *Tab* (pad 15 de la huella) | VS | Alimentación; es el disipador |

Tabla 2, p. 4.

## Recomendaciones de layout del fabricante

- Los tres pines OUT se unen en la placa y la pista debe soportar la corriente máxima (nota 1 de la Tabla 2, p. 4).
- El *tab* VS es el camino térmico: cobre grande conectado a VS bajo y alrededor; el datasheet simula con 600 mm² de cobre de refrigeración (§4.3.1, Figuras 4 y 5, p. 9-10).
- Componentes externos recomendados en el esquema de aplicación (p. 1): R_IN, R_DEN, R_IS, R_GND, C_VS y diodo Zener/TVS en VS.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| BTT6030-2ERA | C534865 | 2 canales, 30 mΩ; misma huella |
| BSP752R | C112644 | 1 canal, 200 mΩ, sin medida de corriente (ST digital) |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-05)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas (30 uds) | 10 placas (60 uds) |
|---|---|---|---|---|---|
| C534868 | Extended | 1 698 | 1–9: 1,2756 · 10–29: 1,1644 · 30–99: 1,0941 · 100–499: 1,0221 | 32,82 $ | 65,65 $ |

(Supuesto: 6 canales por placa, como en `docs/diseno/estudio-salidas.md` §11; el stock de 1 698 cubre 10 placas con margen limitado.)

## Notas de los assets

El símbolo y la huella se han creado desde el datasheet: no hay versión en la librería oficial de KiCad 10 ni en PartReel, y la API de EasyEDA no está accesible desde aquí. La huella usa el *land pattern* oficial de Infineon para el encapsulado PG-TDSO-14-11 (https://www.infineon.com/package/PG-TDSO-14-11, imagen «footprint», consultada el 2026-11-05) y el dibujo de la p. 49 para el cuerpo (ver el log de SPEC-0015). 

**Modelo 3D** (`Infineon_PG-TDSO-14.step`, compartido con el BTT6030-2ERA): creado con SolidCraft (fuentes en `hardware/libraries/3d/fuentes-solidcraft/`). Origen = origen de la huella, Z = 0 en la cara superior de la placa, offset 0, rotación 0 y escala 1. Cotas del datasheet (Figura 53, p. 49): cuerpo 8,65 × 3,9, altura máxima 1,15 con *standoff* de 0,05, pad expuesto 2,65 × 6,4, patillas de 0,4 de ancho a 1,27 de paso con puntas a ±3,0. Supuestos: patillas rectas de 0,2 de grosor y pie de 0,67 modelado desde |x| = 2,3; cuerpo prismático (sin ángulo de flanco); cuerpo hasta 1,15 (máximo, no la cota de referencia de 0,95); marca del pin 1 como hendidura de Ø 0,8 × 0,1 junto al pad 1 (sin cotas en el dibujo). Comprobado con `kicad-cli pcb render` sobre una placa de prueba: patillas sobre sus pads y marca junto al pad 1.

## Uso en el proyecto

DEC-0003, salidas (`salidas.kicad_sch`). Principal.
