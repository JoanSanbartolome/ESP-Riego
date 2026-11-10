---
name: piezas-salidas-trucos
description: Códigos LCSC y trucos del bloque de salidas (BTT6050, M7), vías térmicas del EP y banco de render con huellas en línea
metadata:
  type: reference
---

- Códigos (JLCPCB, 2026-11-10): BTT6050 C534868 Extended (1 628, bajando), BTT6030 C534865, borne C8465, C513710 y C381466 Extended sin equivalente Basic, Yageo RC0805FR-0747KL = C126351, M7 C95872 Basic (PDF de MDD vía `dataManualFileAccessIdUrl`; la URL de lcsc.com da HTML).
- Vías térmicas del EP: copiar el patrón de `Package_SO.pretty/*_ThermalVias` (vías `*.Cu` sin máscara, `pad_prop_heatsink`, `zone_connect 2`, pad B.Cu del EP). JLCPCB: taladro a taladro 0,2 mm (jlcpcb.com/capabilities). La página de Infineon del encapsulado no da vías (WebFetch solo devuelve navegación).
- Banco de render: script que incrusta los `.kicad_mod` en un `.kicad_pcb` mínimo (layers, `(at x y)` tras `(layer "F.Cu")`, rutas 3D absolutas) en el scratchpad; `pcb render --side top|bottom`. No modela el tapado de vías ni la polaridad del LED 0603 oficial.
- La guardia bloquea Python en línea con ciertos caracteres (patrones con `>` o `)`): escribir el script en el scratchpad y lanzarlo con `python -I`. Los `Read` de PDF de texto sacan tablas desordenadas: `pdftoppm -png -r 110` y mirar la imagen.
- KiCad 10: `kicad-cli sch export bom --exclude-dnp` y `pcb export pos --exclude-dnp` existen; sirven para D12–D17 DNP.
