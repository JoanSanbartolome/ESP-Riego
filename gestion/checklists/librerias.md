# Checklist de revisión de librerías y componentes

**Versión:** v1 (2026-11-03). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Origen

- [ ] Se ha seguido el orden de preferencia: librería oficial de KiCad 10 → PartReel → JLCPCB/LCSC → creación propia. El origen está anotado en la ficha del componente.
- [ ] Formato nativo (`.kicad_sym`, `.pretty`); nada leído de JSON de EasyEDA (H8).
- [ ] Tablas de librerías con rutas `${KIPRJMOD}`; ninguna ruta absoluta (KIC-01).

## Símbolo

- [ ] Número y nombre de cada pin coinciden con el datasheet.
- [ ] Tipo eléctrico de cada pin correcto (entrada, salida, alimentación, pasivo…).
- [ ] Campos `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet`, `Description`.

## Huella (obligatorio para huellas creadas o modificadas)

- [ ] Tabla de cotas del informe: cada pad (tamaño, paso, posición) frente al dibujo recomendado del datasheet, con página.
- [ ] Pin 1 marcado en serigrafía y en la capa Fab.
- [ ] Courtyard presente y con margen.
- [ ] Serigrafía fuera de los pads.
- [ ] Modelo 3D presente y alineado (posición, rotación, altura).

## Mapeo símbolo ↔ huella

- [ ] Cada número de pin del símbolo corresponde al pad correcto según el datasheet.

## Ficha del componente

- [ ] Existe `hardware/componentes/<MPN>.md` con LCSC, tipo (basic/extended), fecha de consulta de stock, datasheet y datos clave.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
