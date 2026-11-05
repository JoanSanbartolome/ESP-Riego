---
mpn: BSP752R
fabricante: Infineon Technologies
funcion: interruptor inteligente *high-side* miniPROFET de 1 canal, 6-52 V, 200 mΩ (salidas, tercera opción de DEC-0003)
lcsc: C112644
tipo_jlcpcb: extended
stock_consultado: 2026-11-05
datasheet: https://www.infineon.com/assets/row/public/documents/10/49/infineon-bsp752r-datasheet-en.pdf
datasheet_espejo: https://www.lcsc.com/datasheet/lcsc_datasheet_1810010328_Infineon-Technologies-BSP752R_C112644.pdf
datasheet_local: datasheets/BSP752R.pdf (V1.3, 2017-06-13, 0,5 MB; idéntica byte a byte a la de infineon.com, revisión vigente comprobada el 2026-11-05)
simbolo: esp-riego:BSP752R
huella: Package_SO:Infineon_PG-DSO-8-24_4x5mm
modelo_3d: ${KICAD10_3DMODEL_DIR}/Package_SO.3dshapes/Infineon_PG-DSO-8-24_4x5mm.step
origen_assets: símbolo creado; huella y 3D de la librería oficial de KiCad 10
verificado_por: pendiente (ing-validacion), solo el símbolo
---

# BSP752R · *high-side* miniPROFET

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Tensión de funcionamiento V_bb(on) | 6…52 V | Tabla 1, p. 1 |
| V_bb(AZ) (sobretensión) | 62 V | Tabla 1, p. 1 |
| R_ON | 200 mΩ | Tabla 1, p. 1 |
| I_L(nom) | 1,3 A | Tabla 1, p. 1 |
| Limitación de corto I_L(SCp) | 9 A máx. (T_j = −40 °C, V_bb = 20 V); 6,5 A típ. (25 °C); 4 A mín. (150 °C) | p. 5 |
| Entrada | Umbral de conexión V_IN(T+) ≤ 2,2 V; de desconexión V_IN(T−) ≥ 0,8 V; histéresis 0,4 V típ.; compatible con 3,3 V | p. 6 |
| Diagnóstico | ST de drenador abierto, V_ST(low) ≤ 0,4 V a 1,6 mA (25 °C); corto y sobretemperatura; carga abierta solo en OFF con R externa | p. 1 y p. 6 |
| Encapsulado | PG-DSO-8-24 | Figura 1, p. 16 impresa (p. 17 del PDF) |

Criterio de páginas: las del número impreso en cada hoja del datasheet; entre paréntesis, la del PDF cuando difiere.

## Pinout (vista superior, p. 2)

| Pin | Nombre | Función |
|---|---|---|
| 1 | GND | Masa lógica |
| 2 | IN | Entrada: activa el interruptor con nivel alto |
| 3 | OUT | Salida a la carga |
| 4 | ST | Retroalimentación de diagnóstico (drenador abierto) |
| 5, 6, 7, 8 | Vbb | Alimentación positiva (los cuatro pines unidos) |

## Recomendaciones de layout del fabricante

- Los cuatro pines Vbb se unen con cobre amplio para repartir la corriente y disipar el calor.
- Resistencia en serie con GND para protección contra inversión de polaridad (p. 1: «reverse battery protection with external resistor»).
- El datasheet no da más indicaciones de layout; la huella oficial de KiCad cita este mismo datasheet (p. 16 impresa).

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| BTT6050-1ERA | C534868 | Principal; con medida de corriente |
| ISP752RFUMA1 | C454923 | Industrial; stock de 89 el 2026-11-04 (descartado) |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-05)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 5 placas (30 uds) | 10 placas (60 uds) |
|---|---|---|---|---|---|
| C112644 | Extended | 288 | 1–9: 1,5405 · 10–29: 1,2920 · 30–99: 1,1350 · 100–499: 0,9747 | 34,05 $ | 68,10 $ |

El stock de 288 cubre las 60 unidades de 10 placas con poco margen: riesgo de aprovisionamiento si se elige esta opción (el estudio anotó 277 el 2026-11-04).

## Notas de los assets

Símbolo creado desde el pinout de la p. 2 (el texto del PDF viene con una fuente codificada: pines comprobados sobre la imagen de la página). Huella y 3D oficiales, sin copiar.

## Uso en el proyecto

DEC-0003, salidas: tercera opción, sin medida de corriente.
