---
mpn: TS-1187A-B-A-B
fabricante: XKB Connection (XKB Industrial Precision)
funcion: pulsador táctil SMD SPST 5,1 × 5,1 mm, 160 gf, altura 1,5 mm (RESET y BOOT, MCU-04)
lcsc: C318884
tipo_jlcpcb: basic
stock_consultado: 2026-11-06
datasheet: http://www.helloxkb.com/public/images/pdf/TS-1187A-X-X-X.pdf (URL de la huella oficial; no responde desde este equipo). Espejo de LCSC (dataManualUrl de la API, 2026-11-07): https://www.lcsc.com/datasheet/lcsc_datasheet_2304140030_XKB-Connection-TS-1187A-B-A-B_C318884.pdf. Copia local del dibujo de LCSC/JLCPCB (hoja única): datasheets/TS-1187A-B-A-B.pdf
simbolo: Switch:SW_Push
huella: esp-riego:SW_Push_1P1T_XKB_TS-1187A (copia de Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A; solo cambia la ruta del 3D)
modelo_3d: ${KIPRJMOD}/../libraries/3d/SW_Push_1P1T_XKB_TS-1187A.step (propio; KiCad 10.0.6 no trae el oficial)
origen_assets: creado (3D); huella y símbolo kicad-oficial
verificado_por:
---

# TS-1187A-B-A-B · pulsador táctil SMD

## Datos clave

| Parámetro | Valor | Fuente (página) |
|---|---|---|
| Código de pedido | TS-1187A-X-X-X: 1.º X = fuerza (A 100 gf, B 160 gf, C 260 gf); 2.º X = altura H (A 1,5 · B 1,6 · C 1,7 · D 2,0 · E 2,5 mm); 3.º X = tecla (A PA46, B latón) | Hoja única, tablas «Code-X» |
| Esta variante (B-A-B) | 160 gf, H = 1,5 mm, tecla de latón | ídem |
| Cuerpo | 5,1 ± 0,05 × 5,1 ± 0,05 mm; ancho con terminales 6,5 ± 0,25 | Vista superior |
| Tecla | Ø 2,0; recorrido 0,2 ± 0,1 mm | Alzado |
| Eléctrico | 50 mA, 12 V CC; resistencia de contacto ≤ 100 mΩ; aislamiento ≥ 100 MΩ a 500 V CC; rigidez 250 V CA/min | «Specification» |
| Temperatura | −30…+85 °C (funcionamiento), −30…+80 °C (almacén) | ídem |
| Esquema | A-B unidos y C-D unidos; contacto SPST entre los dos pares | Símbolo de la hoja |
| *Layout* de PCB | pads de 1,0 × 0,75: 7,0 exterior, 5,0 interior (X), 4,5 exterior, 3,0 interior (Y) → centros ±3,0 / ±1,875 | «P.C.B LAYOUT» |

## Pinout

| Pin | Nombre | Función |
|---|---|---|
| 1 (×2 pads, arriba izq. y der.) | A-B | Par superior unido internamente |
| 2 (×2 pads, abajo izq. y der.) | C-D | Par inferior unido internamente |

El conmutador cierra 1-2. El componente es simétrico: no tiene polaridad. El 3D lleva una marca roja en la esquina del pad 1 (arriba a la izquierda en la vista superior) solo como referencia de orientación.

## Recomendaciones de layout del fabricante

- Usar el *layout* de la hoja (huella oficial dibujada sobre él).
- Altura total 1,5 mm: cabe bajo cualquier caja; la variante C-E-B (alternativa) mide 2,5 mm.

## Alternativas

| MPN | LCSC | Diferencias |
|---|---|---|
| TS-1187A-C-E-B | C318887 | Extended; 260 gf y **H = 2,5 mm** (1 mm más alto: revisar con la caja, FAB-11); misma huella; stock 81 180 (2026-11-06) |

## Aprovisionamiento (JLCPCB/LCSC, consulta 2026-11-06)

| Código | Tipo | Stock | Precio unitario por tramo (USD) | 2 uds. por placa |
|---|---|---|---|---|
| C318884 | **Basic** | 969 468 | 1–199: 0,0207 · 200–599: 0,0160 · 600–3999: 0,0139 | ≈ 0,04 $ |

## Nota sobre el modelo 3D

KiCad 10.0.6 no instala `Button_Switch_SMD.3dshapes/SW_Push_1P1T_XKB_TS-1187A.step`. El modelo propio sale de `hardware/libraries/3d/fuentes-solidcraft/gen_ts1187a.py` (SolidCraft). Cotas del PDF: cuerpo 5,1, terminales 0,5 de ancho hasta ±3,25, tecla Ø 2,0, H = 1,5. Supuestos: tapa hasta z = 0,9 (cota 0,9 del alzado), tecla de 0,9 a 1,5, terminales de 0,3 de grosor. **Simplificación (VAL-0021-01-04):** se omite el escalón de la tapa de 0,9 a 1,2 mm del alzado, y el cuerpo empieza en z = 0,15 (separado de la placa); la altura máxima (1,5) es correcta, así que no afecta a FAB-11. Render de comprobación: `hardware/libraries/3d/fuentes-solidcraft/render_SPEC-0021_top.png` (terminales sobre los pads y marca del pin 1 arriba a la izquierda).

## Uso en el proyecto

SW1 (RESET) y SW2 (BOOT) de `mcu.kicad_sch` (SPEC-0022). MCU-04, FAB-11.
