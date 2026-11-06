---
id: DEC-0007
titulo: DEN común a los 6 canales y cambios de compra sin consulta
fecha: 2026-11-06
estado: aceptada
decide: usuario
specs: [SPEC-0019, SPEC-0020, SPEC-0021, SPEC-0022]
requisitos: [MCU-05, REL-04, REL-10, EXP-02]
---

# DEC-0007 · DEN común a los 6 canales y cambios de compra sin consulta

## Contexto

- `docs/diseno/mcu.md` §9.2 propone un DEN común a los 6 BTT6050 (GPIO38). SPEC-0020 decía «IN, DEN e IS por canal». La variante B (§9.3), con un DEN por canal, cabe pero no deja ningún GPIO libre y obliga a compartir el I²C de la placa con la expansión.
- SPEC-0018 dejó cambios de aprovisionamiento propuestos (R8, los 100 nF de C1591) pendientes del usuario.

## Decisión

1. **DEN común:** un solo GPIO (OUT_DEN, GPIO38) va a los 6 DEN, cada uno con su R_DEN de 10 kΩ, más una R_PD de 100 kΩ a GND. Cada IS sigue en su propio canal de ADC1 (GPIO4–9). Se libera un 2.º bus I²C para la expansión y quedan 3 GPIO libres.
2. **Cambios de compra:** el usuario autoriza, sin consulta, cualquier cambio de pieza que haga la placa más fácil o más barata de fabricar (más stock, Basic en vez de Extended, menos líneas de BOM, precio) **sin empeorar ninguna especificación**. Se aplican desde ahora:
   - R8: Yageo RT0603BRD0724K9L (C136967) en vez de C4156365;
   - 100 nF de C5, C9, C13, C14, C20 y C21: C14663 (Basic) en vez de C1591.
   Cada cambio se anota en el documento del bloque y lo revisa validación como cualquier otro valor. Un cambio que empeore una especificación o cambie el coste por placa más de lo acordado sigue consultándose.

## Consecuencias

- SPEC-0020: el criterio «IN, DEN e IS por canal» pasa a «IN e IS por canal, DEN común».
- Salidas: 6 × R_DEN + 1 × R_PD de 100 kΩ en OUT_DEN (`mcu.md` §10.2).
- Firmware: OUT_DEN se activa para leer las IS; se puede dejar alto mientras se riega.
- SPEC-0019 aplica los cambios de compra en `alimentacion.md` y en los campos de la hoja.
