---
mpn: BTT6030-2ERA
fabricante: Infineon Technologies
funcion: interruptor inteligente *high-side* de 2 canales, 24 V, 30 mΩ por canal, con medida de corriente multiplexada (salidas, DEC-0003)
lcsc: C534865
tipo_jlcpcb: extended
stock_consultado: 2026-11-10
datasheet: https://www.infineon.com/assets/row/public/documents/10/49/infineon-btt6030-2era-datasheet-en.pdf
datasheet_espejo: https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_Infineon-Technologies-BTT6030-2ERA_C534865.pdf
datasheet_local: datasheets/BTT6030-2ERA.pdf (Rev. 1.00, 2019-03-09, 1,6 MB, idéntica byte a byte a la de infineon.com, revisión vigente comprobada el 2026-11-05)
simbolo: esp-riego:BTT6030-2ERA
huella: esp-riego:Infineon_PG-TDSO-14_8.65x3.9mm_P1.27mm_EP2.65x6.4mm
modelo_3d: ${KIPRJMOD}/../libraries/3d/Infineon_PG-TDSO-14.step
origen_assets: creado
verificado_por: pendiente (ing-validacion; la huella compartida gana vías del EP en SPEC-0024)
---

# BTT6030-2ERA · *high-side* 2 canales

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Tensión de funcionamiento V_S(OP) | 5…36 V | Tabla 1, p. 2 |
| Tensión máxima V_S(LD) | 65 V | Tabla 1, p. 2 |
| R_DS(ON) máx. a T_J = 150 °C | 62 mΩ por canal | Tabla 1, p. 2 |
| Corriente nominal | 6 A (un canal activo) / 4 A (los dos) | Tabla 1, p. 2 |
| Relación de sentido k_ILIS | 2 240 típ. | Tabla 1, p. 2 |
| Limitación mínima I_L5(SC) | 56 A | Tabla 1, p. 2 |
| Corriente en reposo I_S(OFF) | 500 nA máx. | Tabla 1, p. 2 |
| Diagnóstico | IS multiplexado entre los dos canales con DSEL; carga abierta ON/OFF; corto a GND/V_S; sobretemperatura | p. 2 |
| Encapsulado | PG-TDSO-14 con *tab* (VS) | §11, p. 51 |

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| 1 | GND | Masa lógica |
| 2 | IN0 | Entrada del canal 0 |
| 3 | DEN | Habilitación del diagnóstico |
| 4 | IS | Sentido de corriente del canal seleccionado |
| 5 | DSEL | Selección del canal diagnosticado |
| 6 | IN1 | Entrada del canal 1 |
| 7, 11 | NC | Sin conexión |
| 8, 9, 10 | OUT1 | Salida del canal 1 (unidos en la placa) |
| 12, 13, 14 | OUT0 | Salida del canal 0 (unidos en la placa) |
| *Tab* (pad 15 de la huella) | VS | Alimentación |

Tabla 2, p. 4.

## Recomendaciones de layout del fabricante

- Los pines de cada salida se unen en la placa con pista dimensionada para la corriente (nota 1 de la Tabla 2, p. 4).
- El *tab* VS es el camino térmico: cobre grande conectado a VS (§4.3.1, p. 9-10).
- Mismo encapsulado y misma huella que el BTT6050-1ERA, **ahora con 10 vías de 0,3 / 0,6 mm en el EP** (SPEC-0024, FAB-02). El *tab* es VS (BUS_24V): las vías van a un polígono BUS_24V, no a GND.
- **Distinto pinout: no es intercambiable con el BTT6050 sin rehacer el *routing*** (pines 1 GND, 2 IN0, 3 DEN, 4 IS, 5 DSEL, 6 IN1 frente a NC/GND/IN/DEN/IS del BTT6050; las salidas pasan a 8-10 y 12-14). Un símbolo `esp-riego:BTT6030-2ERA` propio tiene su numeración; no se puede poner el del BTT6050 en la misma huella.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| BTT6050-1ERA | C534868 | 1 canal, 50 mΩ; principal |
| BSP752R | C112644 | 1 canal, sin medida de corriente |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-10)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas (15 uds) | 10 placas (30 uds) |
|---|---|---|---|---|---|
| C534865 | Extended | 10 571 | 1–9: 2,978 · 10–29: 2,5018 · 30–99: 2,204 · 100–499: 1,8997 | 37,53 $ | 66,12 $ |

(Supuesto: 3 circuitos de 2 canales para 6 salidas.)

## Notas de los assets

Creados desde el datasheet (sin versión oficial ni en PartReel). Ver la ficha del BTT6050-1ERA: misma huella y mismo modelo 3D (SolidCraft, cotas de la Figura 54, p. 51, idénticas a las de la Figura 53, p. 49 del BTT6050; origen, cotas y supuestos en esa ficha).

## Uso en el proyecto

DEC-0003, salidas. Segunda fuente del BTT6050-1ERA.
