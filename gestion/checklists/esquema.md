# Checklist de revisión de esquema

**Versión:** v9 (2026-11-12). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

`[auto: X]`: lo comprueba X y nadie lo repasa a mano. `comprobar.py <punto>` es un punto de `herramientas/kicad/comprobar.py`, que `verificar.py` añade a su informe. `[juicio]`: lo repasan el autor, antes de entregar, y validación.

## Estructura

- [ ] [auto: comprobar.py esquema.hojas] Hojas jerárquicas por bloque (KIC-02); ninguna hoja huérfana (H9).
- [ ] [juicio] Cajetín con proyecto, hoja, versión y fecha, comprobado en el PDF exportado (`kicad-cli sch export pdf`, sobre una copia), no solo en el `title_block`.
- [ ] [auto: verificar.py] ERC sin errores; cada aviso restante justificado en el parte del autor.
- [ ] [auto: verificar.py] Referencias anotadas, sin duplicados.

## Campos de cada símbolo

- [ ] [auto: comprobar.py esquema.campos] `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet` y `Description` presentes (FAB-05); a lo que va fuera del BOM (puntos de prueba, puentes, taladros) solo se le piden `Value`, `Footprint` y `Description`.
- [ ] [auto: comprobar.py esquema.huellas] La huella asignada existe en una librería del repositorio o en las oficiales de KiCad 10 (KIC-01).
- [ ] [auto: comprobar.py esquema.vias] Las huellas con vías (`*_ThermalVias` o propias) cumplen FAB-02 (0,3 / 0,6 mm); si no, se usa la variante sin vías y las pone el layout (VAL-0018-02-01, VAL-0019-01-02).
- [ ] [auto: comprobar.py esquema.dnp] Componentes no montados marcados como DNP.

## Cálculos (deben estar en `docs/diseno/`)

- [ ] [juicio] Cada valor calculado tiene fórmula, datos de entrada con su fuente (datasheet + página) y margen.
- [ ] [juicio] Recalculado de forma independiente por el revisor; desviación explicada si la hay.
- [ ] [juicio] Tensiones nominales de cada pieza ≥ peor caso del nodo, incluido el *clamping* de la TVS (ALI-04, ALI-05).
- [ ] [juicio] Condensadores cerámicos con *derating* por tensión DC y temperatura.
- [ ] [juicio] La energía de desmagnetización de cada salida se calcula con el número máximo de cargas por canal y la ecuación del fabricante, y se compara con la curva E_AS(I_L), no con el E_AS a corriente nominal (REL-03).
- [ ] [juicio] Si se calcula una autonomía (*hold-up*), va desde la VIN mínima (ALI-01) menos las caídas hasta el umbral de **bajada** del UVLO (ALI-06), con la potencia de pico de la lógica y la tolerancia del condensador.
- [ ] [juicio] Disipación de reguladores, resistencias de potencia y etapa de salida dentro de márgenes a +50 °C de ambiente (§5) más el calentamiento interno de la caja (≥ 10 °C, o el valor estimado en `docs/diseno/`).

## Alimentación

- [ ] [juicio] Protección de polaridad, fusible y TVS en la entrada, dimensionados para 5,1 A continuos a 50 °C sin actuar (ALI-03, ALI-04, ALI-12).
- [ ] [juicio] TVS unidireccional después de la protección de polaridad, o bidireccional si va en el borne; en el P-MOSFET de polaridad, VGS limitada (zener) a la tensión máxima de entrada y VDS ≥ Vc.
- [ ] [juicio] Divisor de VIN: escala hasta ≥ la VRWM dentro del rango del ADC1, y pin protegido ante Vc (ALI-09).
- [ ] [juicio] Limitador común del bus de salidas (ALI-13): el buck se alimenta antes; banda del umbral, con su tolerancia, dentro de 3,5–4,9 A, calculada en `docs/diseno/`; corte por fallo antes de que el buck baje del UVLO; habilitación con *pull-down*.
- [ ] [juicio] Con el bus de salidas apagado, las entradas IN y DEN a nivel alto no lo alimentan a través del *high-side*.
- [ ] [juicio] TVS: VRWM ≥ tensión máxima de entrada (ALI-01) y Vc ≤ tensión nominal de cada pieza del nodo protegido (ALI-04, ALI-05).
- [ ] [juicio] UVLO referido a la tensión tras las protecciones y ajustable (ALI-06).
- [ ] [juicio] Presupuesto de consumo de la fuente con las 6 salidas activas (ALI-12).
- [ ] [juicio] VBUS unido con diodo, sin retroalimentación al USB ni a la entrada (ALI-08).

## Microcontrolador

- [ ] [juicio] Pines de arranque (GPIO0, 3, 45, 46) sin cargas que alteren el arranque (MCU-05).
- [ ] [juicio] Entradas analógicas solo en ADC1, GPIO1–GPIO10 (MCU-05, H2).
- [ ] [juicio] GPIO19/20 solo para USB; GPIO35–37 libres si hay PSRAM octal.
- [ ] [juicio] Red RC en EN, pulsadores BOOT y RESET (MCU-04).
- [ ] [juicio] Desacoplo según la guía de diseño hardware de Espressif.
- [ ] [juicio] Pinout coherente con el YAML de ESPHome (FW-02, H12).

## Salidas e interfaces de campo

- [ ] [juicio] Salidas desactivadas durante el reset y el flasheo (REL-04).
- [ ] [juicio] Protección de la carga inductiva según REL-03: desmagnetización en el *high-side* (DEC-0003) dentro de su curva E_AS.
- [ ] [juicio] Corriente por canal y total según REL-05 y ALI-12; pistas, bornes y retornos GND de salida para la corriente máxima del limitador, sin protección por canal (REL-05, FAB-03, DEC-0004).
- [ ] [juicio] Cálculo térmico del *high-side* a 4,9 A y comportamiento ante su apagado térmico con enclavamiento (REL-08).
- [ ] [juicio] El LED de cada canal no enmascara la carga abierta en OFF (REL-10).
- [ ] [juicio] Salidas de diagnóstico analógicas (IS) hacia el ADC1 con la tensión máxima en fallo acotada por debajo del máximo del pin; *pull-up* de carga abierta con fuga ≤ 1 mA (REL-10).
- [ ] [juicio] Un corto en una salida: se comprueba qué ven el resto de canales y la lógica hasta que actúa el limitador común (REL-08).
- [ ] [juicio] Orden de pines de los bornes idéntico en los 6 canales y coherente con la serigrafía (REL-06, H1).
- [ ] [juicio] ESD o TVS en todos los conectores de campo; fusible o limitación donde un cortocircuito del cable pueda dañar algo (REL-08, EXP-01, EXP-02).
- [ ] [juicio] Sensor de temperatura y humedad con su desacoplo y pull-ups de I²C; conector de expansión según el informe de SPEC-0006 (AMB-01, EXP-02).

## Entregables para layout

- [ ] [juicio] Tabla de restricciones de layout en `docs/diseno/` (red, corriente, ancho, separación, ubicación, keepouts).

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-04 | Requisitos v0.2 (DEC-0002): fuente de 24 V DC, 6 salidas con tecnología por decidir, sensor en placa, sin lazo 4–20 mA; ajustes de VAL-0004-01. Se ajustó antes del merge de SPEC-0004 (VAL-0004-02-10) |
| v3 | 2026-11-04 | Requisitos v0.3 (DEC-0003) y propuestas de VAL-0004-02 y VAL-0005-01: TVS frente a polaridad, divisor de VIN, limitador común, energía inductiva con la curva E_AS, *hold-up*, IS acotada y corto en una salida |
| v4 | 2026-11-05 | Requisitos v0.4 (DEC-0004) y propuestas de VAL-0007-01 y VAL-0011-01: banda del limitador, salidas y retornos para la corriente del limitador, LED frente a carga abierta, retroalimentación del bus apagado, fusible de entrada y térmica del *high-side*. Se ajustó antes del merge de SPEC-0011 (VAL-0011-01 y VAL-0011-02) |
| v5 | 2026-11-05 | Propuestas de VAL-0013-01 y VAL-0013-02: cajetín comprobado en el PDF exportado |
| v6 | 2026-11-06 | Propuesta de VAL-0019-01: vías de las huellas conforme a FAB-02 |
| v7 | 2026-11-11 | DEC-0009: cada punto marcado `[auto]` o `[juicio]` |
| v8 | 2026-11-12 | SPEC-0027: los cinco `[auto: pendiente]` pasan a `comprobar.py` |
| v9 | 2026-11-12 | VAL-0027-01-10: excepción de lo que va fuera del BOM en los campos |
