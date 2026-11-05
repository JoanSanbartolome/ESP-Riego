# Checklist de revisión de esquema

**Versión:** v4 (2026-11-05). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Estructura

- [ ] Hojas jerárquicas por bloque (KIC-02); ninguna hoja huérfana (H9).
- [ ] Cajetín con proyecto, hoja, versión y fecha.
- [ ] ERC sin errores; cada aviso restante justificado en el log del autor.
- [ ] Referencias anotadas, sin duplicados.

## Campos de cada símbolo

- [ ] `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet` y `Description` presentes (FAB-05).
- [ ] La huella asignada existe en una librería del repositorio o en las oficiales de KiCad 10 (KIC-01).
- [ ] Componentes no montados marcados como DNP.

## Cálculos (deben estar en `docs/diseno/`)

- [ ] Cada valor calculado tiene fórmula, datos de entrada con su fuente (datasheet + página) y margen.
- [ ] Recalculado de forma independiente por el revisor; desviación explicada si la hay.
- [ ] Tensiones nominales de cada pieza ≥ peor caso del nodo, incluido el *clamping* de la TVS (ALI-04, ALI-05).
- [ ] Condensadores cerámicos con *derating* por tensión DC y temperatura.
- [ ] La energía de desmagnetización de cada salida se calcula con el número máximo de cargas por canal y la ecuación del fabricante, y se compara con la curva E_AS(I_L), no con el E_AS a corriente nominal (REL-03).
- [ ] Si se calcula una autonomía (*hold-up*), va desde la VIN mínima (ALI-01) menos las caídas hasta el umbral de **bajada** del UVLO (ALI-06), con la potencia de pico de la lógica y la tolerancia del condensador.
- [ ] Disipación de reguladores, resistencias de potencia y etapa de salida dentro de márgenes a +50 °C de ambiente (§5) más el calentamiento interno de la caja (≥ 10 °C, o el valor estimado en `docs/diseno/`).

## Alimentación

- [ ] Protección de polaridad, fusible y TVS en la entrada, dimensionados para 5,1 A continuos a 50 °C sin actuar (ALI-03, ALI-04, ALI-12).
- [ ] TVS unidireccional después de la protección de polaridad, o bidireccional si va en el borne; en el P-MOSFET de polaridad, VGS limitada (zener) a la tensión máxima de entrada y VDS ≥ Vc.
- [ ] Divisor de VIN: escala hasta ≥ la VRWM dentro del rango del ADC1, y pin protegido ante Vc (ALI-09).
- [ ] Limitador común del bus de salidas (ALI-13): el buck se alimenta antes; banda del umbral, con su tolerancia, dentro de 3,5–4,9 A, calculada en `docs/diseno/`; corte por fallo antes de que el buck baje del UVLO; habilitación con *pull-down*.
- [ ] Con el bus de salidas apagado, las entradas IN y DEN a nivel alto no lo alimentan a través del *high-side*.
- [ ] TVS: VRWM ≥ tensión máxima de entrada (ALI-01) y Vc ≤ tensión nominal de cada pieza del nodo protegido (ALI-04, ALI-05).
- [ ] UVLO referido a la tensión tras las protecciones y ajustable (ALI-06).
- [ ] Presupuesto de consumo de la fuente con las 6 salidas activas (ALI-12).
- [ ] VBUS unido con diodo, sin retroalimentación al USB ni a la entrada (ALI-08).

## Microcontrolador

- [ ] Pines de arranque (GPIO0, 3, 45, 46) sin cargas que alteren el arranque (MCU-05).
- [ ] Entradas analógicas solo en ADC1, GPIO1–GPIO10 (MCU-05, H2).
- [ ] GPIO19/20 solo para USB; GPIO35–37 libres si hay PSRAM octal.
- [ ] Red RC en EN, pulsadores BOOT y RESET (MCU-04).
- [ ] Desacoplo según la guía de diseño hardware de Espressif.
- [ ] Pinout coherente con el YAML de ESPHome (FW-02, H12).

## Salidas e interfaces de campo

- [ ] Salidas desactivadas durante el reset y el flasheo (REL-04).
- [ ] Protección de la carga inductiva según REL-03: desmagnetización en el *high-side* (DEC-0003) dentro de su curva E_AS.
- [ ] Corriente por canal y total según REL-05 y ALI-12; pistas, bornes y retornos GND de salida para la corriente máxima del limitador, sin protección por canal (REL-05, FAB-03, DEC-0004).
- [ ] Cálculo térmico del *high-side* a 4,9 A y comportamiento ante su apagado térmico con enclavamiento (REL-08).
- [ ] El LED de cada canal no enmascara la carga abierta en OFF (REL-10).
- [ ] Salidas de diagnóstico analógicas (IS) hacia el ADC1 con la tensión máxima en fallo acotada por debajo del máximo del pin; *pull-up* de carga abierta con fuga ≤ 1 mA (REL-10).
- [ ] Un corto en una salida: se comprueba qué ven el resto de canales y la lógica hasta que actúa el limitador común (REL-08).
- [ ] Orden de pines de los bornes idéntico en los 6 canales y coherente con la serigrafía (REL-06, H1).
- [ ] ESD o TVS en todos los conectores de campo; fusible o limitación donde un cortocircuito del cable pueda dañar algo (REL-08, EXP-01, EXP-02).
- [ ] Sensor de temperatura y humedad con su desacoplo y pull-ups de I²C; conector de expansión según el informe de SPEC-0006 (AMB-01, EXP-02).

## Entregables para layout

- [ ] Tabla de restricciones de layout en `docs/diseno/` (red, corriente, ancho, separación, ubicación, keepouts).

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-04 | Requisitos v0.2 (DEC-0002): fuente de 24 V DC, 6 salidas con tecnología por decidir, sensor en placa, sin lazo 4–20 mA; ajustes de VAL-0004-01. Se ajustó antes del merge de SPEC-0004 (VAL-0004-02-10) |
| v3 | 2026-11-04 | Requisitos v0.3 (DEC-0003) y propuestas de VAL-0004-02 y VAL-0005-01: TVS frente a polaridad, divisor de VIN, limitador común, energía inductiva con la curva E_AS, *hold-up*, IS acotada y corto en una salida |
| v4 | 2026-11-05 | Requisitos v0.4 (DEC-0004) y propuestas de VAL-0007-01 y VAL-0011-01: banda del limitador, salidas y retornos para la corriente del limitador, LED frente a carga abierta, retroalimentación del bus apagado, fusible de entrada y térmica del *high-side*. Se ajustó antes del merge de SPEC-0011 (VAL-0011-01 y VAL-0011-02) |
