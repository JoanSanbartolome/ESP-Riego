---
id: DEC-0019
titulo: Desglose del resto de la fase 4, caja después de la PCB y cobre de 1 oz provisional
fecha: 2026-11-24
estado: aceptada
decide: usuario
specs: []
requisitos: [FAB-02, FAB-03, FAB-08, KIC-04, MCU-02, AMB-02, REL-05]
---

# DEC-0019 · Desglose del resto de la fase 4, caja después de la PCB y cobre de 1 oz provisional

## Contexto

Con SPEC-0038 cerrada, el esquema de `hardware/v2` está estable y `colocacion-b4.csv` da 0 obligatorias sobre la PCB real. Quedan por decidir el desglose del layout, D5 (caja) y D6 (grosor del cobre).

## Decisión

El usuario (2026-11-24):

- **Desglose de la fase 4**, por este orden:
  1. aplicar b4 a la PCB de `hardware/v2`, con la imagen aprobada antes por el usuario. Incluye FAB-08 a 100 × 100 mm, la zona de U5 y la isla y las ranuras del SHT40;
  2. clases de red y `.kicad_dru` con las reglas de JLCPCB (FAB-02, FAB-03, KIC-04);
  3. rutado: potencia y salidas, después la analógica y por último las señales; planos de GND con cosido de vías. Si es grande, en dos specs;
  4. cierre: DRC 0, paridad 0 y revisión en 3D.
- **SPEC-0036** sigue adelante: se quiere una pieza de respaldo para U1. No se abre todavía.
- **D5:** la caja se diseña cuando la PCB esté terminada. La revisión en 3D con la caja y el recorte de la zona de U5 que dependa de ella quedan para entonces.
- **D6:** cobre de **1 oz**, provisional. No es definitivo, porque falta el trabajo de diseño térmico; se revisa al rutar.
- **Rieles:** el usuario no los cree necesarios. J10 lo suelda él, y las huellas caben dentro de la placa. Para J2 y U5, que monta JLCPCB al ras del borde, se confirma en la revisión DFM antes del pedido.

## Consecuencias

- El coordinador no abre ninguna spec hasta que el usuario lo pida.
- `docs/02` §7 (D5 y D6) y `docs/03` (fase 4) se ponen al día en la primera spec de la fase 4.
- La spec de rutado incluye el diseño térmico con 1 oz y propone 2 oz, con su coste, si no basta.
