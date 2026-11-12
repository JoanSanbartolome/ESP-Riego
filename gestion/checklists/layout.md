# Checklist de revisión de layout

**Versión:** v7 (2026-11-12). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

`[auto: X]`: lo comprueba X y nadie lo repasa a mano. `comprobar.py <punto>` es un punto de `herramientas/kicad/comprobar.py`, que `verificar.py` añade a su informe. `layout.restricciones` no aplica hasta que exista la tabla de restricciones (`docs/diseno/restricciones.csv`, fase 4). `[juicio]`: lo repasan el autor, antes de entregar, y validación.

## Reglas y verificación

- [ ] [juicio] `.kicad_dru` y clases de red según FAB-02, FAB-03 y KIC-04.
- [ ] [auto: verificar.py] DRC sin errores y sin elementos sin conectar.
- [ ] [auto: verificar.py] Paridad esquema↔PCB sin incidencias (KIC-03, H1).
- [ ] [auto: comprobar.py layout.zonas] Zonas rellenadas antes de verificar.
- [ ] [juicio] Cajetín comprobado en el PDF exportado (`kicad-cli pcb export pdf --include-border-title`, sobre una copia).
- [ ] [auto: comprobar.py layout.incrustados] La PCB no lleva `embedded_files` con hojas de dibujo u otros archivos ajenos al diseño actual.
- [ ] [auto: comprobar.py layout.salida] `pcbplotparams/outputdirectory` vacío o dentro de `fabricacion/<versión>/`.

## Floorplan

- [ ] [juicio] Salidas 1–3 en el borde superior y 4–6 en el inferior, con la entrada y la expansión en el inferior; USB-C accesible desde un lateral (REL-09, FAB-07).
- [ ] [juicio] Antena del módulo en el borde con zona libre de cobre en todas las capas (MCU-02).
- [ ] [juicio] Buck junto a la entrada con bucle de conmutación mínimo.
- [ ] [juicio] Sensor de temperatura y humedad en un borde, con ranuras y sin cobre debajo, lejos del buck, del LDO, del módulo ESP32-S3 y de las salidas (AMB-02).
- [ ] [juicio] Divisor de VIN alejado del buck y de las salidas.
- [ ] [auto: comprobar.py layout.restricciones] Pistas de entrada, limitador común y bus de las salidas (`Power_In`) para 5,1 A, y retornos GND de los bornes de salida para la corriente máxima del limitador, 4,9 A (FAB-03).
- [ ] [juicio] Dimensiones dentro del objetivo (FAB-08) y 4 taladros M3.
- [ ] [juicio] Presupuesto de longitud de cada borde con los taladros M3 y todos los conectores de FAB-07.

## Potencia y cargas

- [ ] [auto: comprobar.py layout.restricciones] Anchos de pista según la tabla de restricciones de layout del esquema.
- [ ] [auto: comprobar.py layout.restricciones] Pistas de las salidas para la carga máxima de REL-05 con ΔT ≤ 10 °C y para la corriente máxima del limitador (4,9 A) con ΔT ≤ 40 °C (≈ 1,2 mm con 1 oz), y separación de la clase `Salidas` (FAB-03).
- [ ] [juicio] Número de vías suficiente en cada cambio de capa de potencia.

## Masa

- [ ] [juicio] Planos de GND continuos en ambas caras, sin cortes bajo el buck ni bajo señales analógicas (FAB-04).
- [ ] [juicio] Cosido de vías.
- [ ] [auto: verificar.py] Ninguna conexión térmica incompleta ni isla aislada (H10).

## Fabricación y montaje

- [ ] [auto: verificar.py] Separación cobre-borde ≥ 0,5 mm (FAB-02).
- [ ] [juicio] Fiduciales para montaje SMT.
- [ ] [auto: comprobar.py layout.smd_cara] Componentes SMD solo en la cara superior, salvo justificación.
- [ ] [juicio] Serigrafía legible (≥ 0,8 mm), fuera de pads, con función de cada borne, polaridades, tensión máxima, versión y fecha (FAB-09).

## 3D y mecánica

- [ ] [auto: comprobar.py layout.3d] Modelo 3D en todos los componentes (FAB-11).
- [ ] [juicio] Encaje en la caja ventilada y acceso a los bornes y al USB-C (D5).

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-04 | Requisitos v0.2 (DEC-0002): bornes en dos bordes, sensor aislado térmicamente, sin zona del lazo 4–20 mA; ajustes de VAL-0004-01. Se ajustó antes del merge de SPEC-0004 (VAL-0004-02-10) |
| v3 | 2026-11-04 | Requisitos v0.3 (DEC-0003) y propuestas de VAL-0004-02: bus de salidas y retornos para 4–5 A, presupuesto de los bordes |
| v4 | 2026-11-05 | Requisitos v0.4 (DEC-0004): pistas y retornos de salida para la corriente máxima del limitador. Se ajustó antes del merge de SPEC-0011 (VAL-0011-01) |
| v5 | 2026-11-05 | Propuestas de VAL-0013-01 y VAL-0013-02: cajetín en el PDF, `embedded_files` ajenos y directorio de trazado |
| v6 | 2026-11-11 | DEC-0009: cada punto marcado `[auto]` o `[juicio]` |
| v7 | 2026-11-12 | SPEC-0027: los ocho `[auto: pendiente]` pasan a `comprobar.py`; los tres de anchos y corriente dependen de la tabla de restricciones |
