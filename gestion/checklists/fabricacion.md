# Checklist de revisión del paquete de fabricación

**Versión:** v1 (2026-11-03). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Generación

- [ ] Todas las salidas generadas con `kicad-cli` a partir del commit etiquetado (KIC-05).
- [ ] Carpeta `fabricacion/<versión>/` con Gerber, taladros, BOM, CPL y PDF de esquema y PCB.

## Gerber y taladros

- [ ] Todas las capas necesarias y archivo de trabajo (`.gbrjob`).
- [ ] Revisión visual de cada capa en un visor de Gerber.
- [ ] Taladros con tamaños y número de agujeros coherentes con la PCB.

## BOM

- [ ] Todas las referencias, con cantidades correctas y componentes DNP excluidos.
- [ ] Código LCSC en cada línea montada por JLCPCB, con stock comprobado (fecha anotada).
- [ ] Piezas *Extended* justificadas.

## CPL (pick and place)

- [ ] Cara correcta para cada componente.
- [ ] Rotaciones comprobadas en la previsualización de JLCPCB (especialmente SOT, SOIC, diodos y LED).

## Coherencia

- [ ] Versión y fecha de la serigrafía coinciden con la etiqueta de git.
- [ ] Revisión DFM de JLCPCB sin errores.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
