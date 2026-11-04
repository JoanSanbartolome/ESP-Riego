# Checklist de revisión de esquema

**Versión:** v1 (2026-11-03). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

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
- [ ] Disipación de reguladores, resistencias de potencia y MOSFET dentro de márgenes a +60 °C.

## Alimentación

- [ ] Protección de polaridad, fusible y TVS en la entrada (ALI-03, ALI-04).
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

- [ ] Relés desactivados durante el reset y el flasheo (REL-04).
- [ ] Diodo de rueda libre en cada bobina (REL-03).
- [ ] Orden de pines de los bornes idéntico en los 4 canales y coherente con la serigrafía (REL-06, H1).
- [ ] ESD o TVS en todos los conectores de campo; limitación de corriente donde un cortocircuito del cable pueda dañar algo (NIV-02).
- [ ] Lazo 4–20 mA: ≥ 12 V en el transmisor a 20 mA con VIN mínimo (NIV-01, H3).

## Entregables para layout

- [ ] Tabla de restricciones de layout en `docs/diseno/` (red, corriente, ancho, separación, ubicación, keepouts).

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
