# Checklist de revisión de esquema

**Versión:** v14 (2026-11-17). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

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
- [ ] [juicio] La rueda libre de cada salida (REL-03) soporta con margen la tensión del bus y la corriente media de la carga en uso (REL-05), y el pico de un corto con su I_FSM frente a la corriente y la duración que deja pasar el *high-side*. Su fuga en caliente cabe en el presupuesto de la carga abierta (REL-10).
- [ ] [juicio] Los límites de uso de las salidas (REL-11) tienen valor, origen y consecuencia de superarlos, y son coherentes con REL-05, ALI-12, ALI-13 y REL-10; ningún cálculo de las salidas usa una válvula concreta como dato de diseño (DEC-0014). Cada uso prohibido (AC, fuentes externas, biestables, PWM) lleva también su consecuencia.
- [ ] [juicio] Un cálculo que se apoya en una protección de un CI (reintento, enclavamiento, apagado térmico, rearme por subtensión) cita la página de su descripción funcional y no contradice otras secciones del documento.
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
- [ ] [juicio] Protección de la carga inductiva según REL-03: rueda libre montada en cada salida, de GND a la salida (DEC-0014).
- [ ] [juicio] Corriente por canal y total según REL-05 y ALI-12; pistas, bornes y retornos GND de salida para la corriente máxima del limitador, sin protección por canal (REL-05, FAB-03, DEC-0004).
- [ ] [juicio] Cálculo térmico del *high-side* a 4,9 A y comportamiento ante su apagado térmico con enclavamiento (REL-08).
- [ ] [juicio] El LED de cada canal no enmascara la carga abierta en OFF (REL-10).
- [ ] [juicio] Salidas de diagnóstico analógicas (IS) hacia el ADC1 con la tensión máxima en fallo acotada por debajo del máximo del pin; *pull-up* de carga abierta con fuga ≤ 1 mA (REL-10).
- [ ] [juicio] Un corto en una salida: se comprueba qué ven el resto de canales y la lógica hasta que actúa el limitador común (REL-08).
- [ ] [juicio] Orden de pines de los bornes idéntico en los 6 canales y coherente con la serigrafía (REL-06, H1).
- [ ] [juicio] ESD o TVS en todos los conectores de campo; fusible o limitación donde un cortocircuito del cable pueda dañar algo (REL-08, EXP-02).
- [ ] [juicio] Sensor de temperatura y humedad con su desacoplo y pull-ups de I²C; conector de expansión según el informe de SPEC-0006 (AMB-01, EXP-02).

## Estilo (KIC-06, DEC-0015)

Los cuatro primeros puntos no se aplican a las hojas que lista `hardware/v2/estilo-pendiente.txt` (transición de SPEC-0035, que lo borra al terminar); esas se repasan sobre su imagen.

- [ ] [auto: comprobar.py esquema.cruces] Ningún cable cruza un símbolo ni un texto, y ningún texto (referencia, valor, etiqueta, nota) se solapa con otro ni con un símbolo.
- [ ] [auto: comprobar.py esquema.sueltas] Ninguna etiqueta suelta: cada etiqueta está en el extremo de un cable o en un pin.
- [ ] [auto: comprobar.py esquema.recuadros] Toda pieza está dentro de un recuadro de bloque (rectángulo de trazo y punto con su título).
- [ ] [auto: comprobar.py esquema.etiquetas] Dentro de un recuadro no hay etiquetas locales que unan piezas del mismo bloque: se unen con cables. Las globales y jerárquicas, solo para las señales que salen del bloque o de la hoja.
- [ ] [auto: comprobar.py esquema.pcb_main] El diff de la PCB frente a `main` solo toca las huellas de las referencias que la spec cambia; si toca otras, el parte las lista (VAL-0034-01).
- [ ] [juicio] Título de cada recuadro arriba a la izquierda con el nombre del bloque, sus referencias principales y sus IDs de requisito.
- [ ] [juicio] Alimentación con símbolos `power` unidos al pin por un cable corto (tensiones hacia arriba, GND hacia abajo), y el circuito leído de izquierda a derecha.
- [ ] [juicio] Cifras clave junto a la pieza (frecuencia de corte, corriente, umbral) y como mucho 2 o 3 líneas de nota por bloque; el detalle, en `docs/diseno/`.
- [ ] [juicio] Rejilla de 1,27 mm y tamaños de texto por defecto de KiCad.

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
| v10 | 2026-11-13 | SPEC-0030: sin EXP-01, retirado en los requisitos v0.6 (DEC-0011) |
| v11 | 2026-11-17 | SPEC-0033: requisitos v0.7 (DEC-0014). Rueda libre montada en lugar de la curva E_AS; límites de uso de las salidas (REL-11) |
| v12 | 2026-11-17 | SPEC-0034 (VAL-0034-01): consecuencia de cada uso prohibido en REL-11; cálculos sobre protecciones de un CI con su página |
| v13 | 2026-11-17 | SPEC-0035: sección «Estilo» (KIC-06, DEC-0015) y diff de la PCB limitado a las referencias de la spec (VAL-0034-01) |
| v14 | 2026-11-17 | SPEC-0035 (paso 1): los cinco `[auto: pendiente]` de «Estilo» pasan a `comprobar.py`; transición con `estilo-pendiente.txt` |
