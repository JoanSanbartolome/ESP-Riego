# Checklist de revisión de librerías y componentes

**Versión:** v2 (2026-11-05). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

## Origen

- [ ] Se ha seguido el orden de preferencia: librería oficial de KiCad 10 → PartReel → JLCPCB/LCSC → creación propia. El origen está anotado en la ficha del componente.
- [ ] Formato nativo (`.kicad_sym`, `.pretty`); nada leído de JSON de EasyEDA (H8).
- [ ] Antes de dar un JSON de EasyEDA por no convertible, se prueba `kicad-cli fp|sym upgrade -o` y se anota la orden.
- [ ] En importaciones o conversiones, la fidelidad se comprueba con una conversión independiente y un `diff` sin las UUID, además de la comparación normalizada de los pads.
- [ ] Al sustituir una pieza, `git diff` confirma que el archivo cambia; si sale idéntico, se anota.
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
- [ ] Modelo 3D presente y alineado (posición, rotación, altura), en `.step`: KiCad 10 no instala los `.wrl`, y las rutas `${KICADn_3DMODEL_DIR}` apuntan a archivos que existen.
- [ ] Antes de llamar artefacto a un pad `custom`, se mide la envolvente de sus primitivas (el `size` del ancla no da el tamaño del cobre).
- [ ] Las extensiones de los modelos 3D, en mayúsculas y en minúsculas, están como `binary` en `.gitattributes`.

## Mapeo símbolo ↔ huella

- [ ] Cada número de pin del símbolo corresponde al pad correcto según el datasheet.

## Ficha del componente

- [ ] Existe `hardware/componentes/<MPN>.md` con LCSC, tipo (basic/extended), fecha de consulta de stock, datasheet y datos clave.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-05 | Propuestas de VAL-0009-01 y VAL-0010-01 (antes en SPEC-0012): conversión de EasyEDA con `kicad-cli`, fidelidad con una conversión independiente, `git diff` al sustituir, modelos `.step`, pads `custom` y binarios en `.gitattributes` |
