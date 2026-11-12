# Checklist de revisión de librerías y componentes

**Versión:** v5 (2026-11-12). Cada informe cita la versión usada. Cualquier cambio sube la versión y se anota en el historial.

`[auto: X]`: lo comprueba X y nadie lo repasa a mano. `comprobar.py <punto>` es un punto de `herramientas/kicad/comprobar.py`, que `verificar.py` añade a su informe. `[juicio]`: lo repasan el autor, antes de entregar, y validación.

## Origen

- [ ] [juicio] Se ha seguido el orden de preferencia: librería oficial de KiCad 10 → PartReel → JLCPCB/LCSC → creación propia. El origen está anotado en la ficha del componente.
- [ ] [auto: comprobar.py librerias.formato] Formato nativo (`.kicad_sym`, `.pretty`); nada leído de JSON de EasyEDA (H8).
- [ ] [juicio] Antes de dar un JSON de EasyEDA por no convertible, se prueba `kicad-cli fp|sym upgrade -o` y se anota la orden.
- [ ] [juicio] En importaciones o conversiones, la fidelidad se comprueba con una conversión independiente y un `diff` sin las UUID, además de la comparación normalizada de los pads.
- [ ] [juicio] Al sustituir una pieza, `git diff` confirma que el archivo cambia; si sale idéntico, se anota.
- [ ] [auto: comprobar.py librerias.rutas] Tablas de librerías con rutas `${KIPRJMOD}`; ninguna ruta absoluta (KIC-01).
- [ ] [juicio] Las tablas de librerías del proyecto solo listan librerías en uso o previstas, sin restos de la versión anterior.
- [ ] [juicio] Antes de derivar una huella por IPC, se busca el *land pattern* en la página del encapsulado del fabricante (p. ej. `infineon.com/package/<encapsulado>`), no solo en el datasheet.

## Símbolo

- [ ] [juicio] Número y nombre de cada pin coinciden con el datasheet.
- [ ] [juicio] Tipo eléctrico de cada pin correcto (entrada, salida, alimentación, pasivo…).
- [ ] [auto: comprobar.py librerias.campos] Campos `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet`, `Description`.

## Huella (obligatorio para huellas creadas o modificadas)

- [ ] [juicio] Tabla de cotas del informe: cada pad (tamaño, paso, posición) frente al dibujo recomendado del datasheet, con página.
- [ ] [juicio] Pin 1 marcado en serigrafía y en la capa Fab.
- [ ] [auto: comprobar.py librerias.patio] Courtyard presente y con margen.
- [ ] [auto: comprobar.py librerias.serigrafia] Serigrafía fuera de los pads.
- [ ] [juicio] Un `kicad-cli pcb render` (vista superior) sobre una placa de prueba confirma que el pin 1 del modelo 3D cae sobre el pad 1; los STEP generados por script llevan la Y hacia arriba.
- [ ] [juicio] En conectores THT, la posición de la patilla sale de la cota del corte o de la vista lateral, y la cara de entrada del cable se marca en Fab.
- [ ] [juicio] Taladro acabado ≥ diagonal máxima de la patilla + 0,1 mm, o justificado.
- [ ] [auto: comprobar.py librerias.3d] Modelo 3D presente, en `.step` (KiCad 10 no instala los `.wrl`), y las rutas `${KICADn_3DMODEL_DIR}` apuntan a archivos que existen.
- [ ] [juicio] Modelo 3D alineado (posición, rotación, altura), mirado con `vista.py huella --3d`.
- [ ] [juicio] Atributo de la huella (`smd` o `through_hole`) coherente con sus pads: sin él, `kicad-cli pcb export pos --smd-only` deja la pieza fuera del CPL (SPEC-0027).
- [ ] [juicio] Antes de llamar artefacto a un pad `custom`, se mide la envolvente de sus primitivas (el `size` del ancla no da el tamaño del cobre).
- [ ] [auto: comprobar.py librerias.gitattributes] Las extensiones de los modelos 3D, en mayúsculas y en minúsculas, están como `binary` en `.gitattributes`.

## Mapeo símbolo ↔ huella

- [ ] [juicio] Cada número de pin del símbolo corresponde al pad correcto según el datasheet.

## Ficha del componente

- [ ] [auto: comprobar.py librerias.fichas] Existe `hardware/componentes/<MPN>.md` con LCSC, tipo (basic/extended), fecha de consulta de stock, datasheet y datos clave.
- [ ] [juicio] El datasheet enlazado es el del fabricante, en su revisión vigente; LCSC queda como espejo.
- [ ] [juicio] Si LCSC no encuentra la pieza, se consulta la API de JLCPCB y se anota que solo está disponible para montaje.

## Historial

| Versión | Fecha | Cambio |
|---|---|---|
| v1 | 2026-11-03 | Versión inicial |
| v2 | 2026-11-05 | Propuestas de VAL-0009-01 y VAL-0010-01 (antes en SPEC-0012): conversión de EasyEDA con `kicad-cli`, fidelidad con una conversión independiente, `git diff` al sustituir, modelos `.step`, pads `custom` y binarios en `.gitattributes` |
| v3 | 2026-11-05 | Propuestas de VAL-0014-01 y VAL-0015-01: tablas sin restos, land pattern del fabricante, pin 1 del 3D con render, patilla THT desde el corte, taladro frente a la diagonal, datasheet del fabricante y API de JLCPCB |
| v4 | 2026-11-11 | DEC-0009: cada punto marcado `[auto]` o `[juicio]` |
| v5 | 2026-11-12 | SPEC-0027: los `[auto: pendiente]` pasan a `comprobar.py`; el modelo 3D se parte en presente (`[auto]`) y alineado (`[juicio]`); atributo `smd` o `through_hole` de la huella |
