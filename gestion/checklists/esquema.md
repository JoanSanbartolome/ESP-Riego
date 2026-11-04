# Checklist de revisión de esquema

**Versión:** v2 (2026-11-04). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

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
- [ ] Disipación de reguladores, resistencias de potencia y etapa de salida dentro de márgenes a +50 °C de ambiente (§5).

## Alimentación

- [ ] Puente rectificador, condensador de bulk, fusible y TVS en la entrada; el buck no cae por debajo del UVLO con 20 V AC a plena carga (ALI-01 … ALI-04).
- [ ] UVLO calculado y ajustable (ALI-06).
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
- [ ] Protección de la carga inductiva según la tecnología elegida: diodo, *snubber* o varistor (REL-03).
- [ ] Corriente por canal y total según REL-05 y la decisión D8.
- [ ] Orden de pines de los bornes idéntico en los 6 canales y coherente con la serigrafía (REL-06, H1).
- [ ] ESD o TVS en todos los conectores de campo; fusible o limitación donde un cortocircuito del cable pueda dañar algo (REL-08, EXP-01, EXP-02).
- [ ] Sensor de temperatura y humedad con su desacoplo y pull-ups de I²C; conector de expansión según el informe de SPEC-0006 (AMB-01, EXP-02).

## Entregables para layout

- [ ] Tabla de restricciones de layout en `docs/diseno/` (red, corriente, ancho, separación, ubicación, keepouts).

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-04 | Requisitos v0.2 (DEC-0002): entrada de 24 V AC rectificada, 6 salidas con tecnología por decidir, sensor en placa, sin lazo 4–20 mA |
