# Checklist de revisión del paquete de fabricación

**Versión:** v5 (2026-11-12). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

`[auto: X]`: lo comprueba X y nadie lo repasa a mano. `[auto: pendiente]`: lo comprobará un script del paquete de fabricación (fase 5); hasta entonces se repasa. `[juicio]`: lo repasan el autor, antes de entregar, y validación.

## Generación

- [ ] [juicio] Todas las salidas generadas con `kicad-cli` a partir del commit etiquetado (KIC-05).
- [ ] [auto: pendiente] Carpeta `fabricacion/<versión>/` con Gerber, taladros, BOM, CPL y PDF de esquema y PCB.
- [ ] [auto: pendiente] `copper_finish` del *stackup* según FAB-01 (HASL sin plomo o ENIG) y grosor de cobre según D6.
- [ ] [auto: pendiente] Las rutas de salida del `.kicad_pro` (`plot`, `bom_export_filename`, `step`, `svg`) y del `.kicad_pcb` (`pcbplotparams/outputdirectory`) están vacías o dentro de `fabricacion/<versión>/`.

## Gerber y taladros

- [ ] [auto: pendiente] Todas las capas necesarias y archivo de trabajo (`.gbrjob`).
- [ ] [juicio] Revisión visual de cada capa en un visor de Gerber.
- [ ] [auto: pendiente] Taladros con tamaños y número de agujeros coherentes con la PCB.

## BOM

- [ ] [auto: pendiente] Todas las referencias, con cantidades correctas y componentes DNP excluidos.
- [ ] [auto: pendiente] Código LCSC en cada línea montada por JLCPCB, con stock comprobado (fecha anotada).
- [ ] [juicio] Piezas *Extended* justificadas.

## CPL (pick and place)

- [ ] [auto: pendiente] Cara correcta para cada componente.
- [ ] [juicio] Rotaciones comprobadas en la previsualización de JLCPCB (especialmente SOT, SOIC, diodos y LED).

## Coherencia

- [ ] [juicio] Versión y fecha de la serigrafía coinciden con la etiqueta de git.
- [ ] [juicio] Revisión DFM de JLCPCB sin errores.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-05 | Propuestas de VAL-0013-01 y VAL-0013-02: rutas de salida del proyecto y de la PCB |
| v3 | 2026-11-05 | Propuesta de VAL-0014-01: acabado y cobre del *stackup* |
| v4 | 2026-11-11 | DEC-0009: cada punto marcado `[auto]` o `[juicio]` |
| v5 | 2026-11-12 | SPEC-0027: los `[auto: pendiente]` de esta checklist quedan para el paquete de fabricación (fase 5) |
