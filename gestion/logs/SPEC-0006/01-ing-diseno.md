---
spec: SPEC-0006
agente: ing-diseno
n: 01
fecha: 2026-11-15
estado: completado
---

# SPEC-0006 · 01 · ing-diseno

## Hecho

- `docs/diseno/viabilidad-expansion.md`: informe de las 5 arquitecturas con los mismos criterios, costes (6 y 8 canales; 5 y 10 uds; montaje JLCPCB), recomendación (1 · I²C TCA9535 + ADS1115), alternativa (4 · nodo ESP32-S3) y definición de EXP-02 (§10: tipo, pines, alimentación, *pull-ups*, ESD, piezas y restricciones de layout).
- `hardware/componentes/stock-expansion.csv`: 158 precios de JLCPCB (código, cantidad del pedido, tramo, stock, 2026-11-15).
- `herramientas/kicad/jlc.py` + README: modo `--buscar` (MPN o texto, hasta 25 resultados, `--detalle`). Probado a mano y con `test_kicad.py Jlc` (OK).

## Decisiones y desviaciones

- **El módulo lleva su propia entrada de 24 V y su TPS26632:** dos limitadores en la fuente de 5 A pasan de 5,14 A (ALI-12, ALI-13). Por EXP-02 no pasan 24 V.
- EXP-02 usa los 4 GPIO de `mcu.md` §9.2 sin cambiar su número. **EXP_IO2 pasa a EXP_EN** (salida, *pull-down* de 100 kΩ, habilita el limitador del módulo). GPIO10, 18, 37 y 39 quedan libres para EXP-03.
- Añadidos que la spec no pedía: dos TPS2553 (5 V con límite de 343–439 mA, 3,3 V con 115–159 mA) para que un corto en el cable no tumbe la lógica (§10.3). Línea Extended nueva: +≈ 2 $ por placa.
- TCA9555 y PCA9555 descartados: el *pull-up* interno pone IN en alto al encender (TCA9555 p. 3).
- Conector sin enclavamiento positivo: las versiones con expulsores no tienen stock. La opción con enclavamiento es Micro-Fit 3.0 (C277725), con otra tabla de pines.

## Verificación

- No se ha tocado ningún proyecto KiCad ni se ha usado el MCP: `verificar.py` no aplica.
- Checklist de requisitos, «Estudios de diseño»: los tres puntos `[juicio]` se cumplen (tramos reales; cada descarte con su parámetro y página; sin datos de entrada cambiados).

## Para validación

- Supuestos: capacidad del pin del ESP32-S3 y del ADS1115 (10 pF), PCB de 10 uds a 5 $, cable de 47,5 pF/m (3M 3365, TS-0080 p. 1).
- Poco margen: T_J del TLV1117LV, 121 °C con los dos raíles del cable en corto (§10.3). EXP_EN, 2,43 V con 4 módulos frente a 2,0 V (§10.2).
- El TCA9535 no está probado en ESPHome (sí el PCA9535, misma huella).
- CAN (§7): las cifras de distancia y nodos son típicas de ISO 11898-2, sin datasheet.

## Pendiente

1. Usuario: decidir D9. Requisito nuevo (EXP-04 o un ID nuevo) que diga que el módulo tiene su propia fuente de 24 V y su limitador. La otra opción, una fuente común más grande, cambia ALI-12, ALI-13 y DEC-0004.
2. Corriente de las válvulas (DEC-0011): fija R_ILIM y la fuente del módulo. Con 42 Ω, solo 5 válvulas a la vez por cada fuente de 5 A (§2.3).
3. Coordinador: stock 0 del fusible 0451010.MRL (C44479) en JLCPCB, también para F1 de la placa (alternativa TA10, C2998199, 1 307). TPS26632: 1 240.
4. Coordinador: añadir a `test_kicad.py` la prueba de `jlc.resultados` (`--buscar`), que está fuera de mi zona.
5. SPEC-0031: pasar §10 a `conectores.md` y a la hoja, y actualizar `mcu.md` §9.2 (GPIO35/36/47/48, EXP_EN) y §14.2.
