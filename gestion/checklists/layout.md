# Checklist de revisión de layout

**Versión:** v2 (2026-11-04). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Reglas y verificación

- [ ] `.kicad_dru` y clases de red según FAB-02, FAB-03 y KIC-04.
- [ ] DRC sin errores y sin elementos sin conectar.
- [ ] Paridad esquema↔PCB sin incidencias (KIC-03, H1).
- [ ] Zonas rellenadas antes de verificar.

## Floorplan

- [ ] Salidas 1–3 en el borde superior y 4–6 en el inferior, con la entrada y la expansión en el inferior; USB-C accesible desde un lateral (REL-09, FAB-07).
- [ ] Antena del módulo en el borde con zona libre de cobre en todas las capas (MCU-02).
- [ ] Buck junto a la entrada con bucle de conmutación mínimo.
- [ ] Sensor de temperatura y humedad en un borde, con ranuras y sin cobre debajo, lejos del buck, del LDO y de las salidas (AMB-02).
- [ ] Divisor de la tensión rectificada alejado del buck y de las salidas.
- [ ] Dimensiones dentro del objetivo (FAB-08) y 4 taladros M3.

## Potencia y cargas

- [ ] Anchos de pista según la tabla de restricciones de layout del esquema.
- [ ] Pistas de las salidas para la corriente de REL-05 con ΔT ≤ 10 °C, y separación de la clase `Salidas` (FAB-03).
- [ ] Número de vías suficiente en cada cambio de capa de potencia.

## Masa

- [ ] Planos de GND continuos en ambas caras, sin cortes bajo el buck ni bajo señales analógicas (FAB-04).
- [ ] Cosido de vías.
- [ ] Ninguna conexión térmica incompleta ni isla aislada (H10).

## Fabricación y montaje

- [ ] Separación cobre-borde ≥ 0,5 mm (FAB-02).
- [ ] Fiduciales para montaje SMT.
- [ ] Componentes SMD solo en la cara superior, salvo justificación.
- [ ] Serigrafía legible (≥ 0,8 mm), fuera de pads, con función de cada borne, polaridades, tensión máxima, versión y fecha (FAB-09).

## 3D y mecánica

- [ ] Modelo 3D en todos los componentes (FAB-11).
- [ ] Encaje en la caja ventilada y acceso a los bornes y al USB-C (D5).

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-04 | Requisitos v0.2 (DEC-0002): bornes en dos bordes, sensor aislado térmicamente, sin zona del lazo 4–20 mA |
