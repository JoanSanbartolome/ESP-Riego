---
spec: SPEC-0018
agente: jr-conformidad
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 01 · jr-conformidad

## Orden recibida

SPEC-0018 · rama spec/SPEC-0018-piezas-alimentacion · Lee: spec + docs/diseno/alimentacion.md (lista de piezas y Anexo A) + log SPEC-0017 · Haz: todo el alcance · Entrega: librerías, fichas y huella JP1 + este log. Único usuario del MCP; guardar y `close_project` al terminar. Brevedad.

## Contexto consultado

- Spec, `alimentacion.md` §3, §7, §8 y Anexo A, log SPEC-0017, `checklists/librerias.md` v3.
- Datasheets: TI LMR36520 SNVSBF0C (pp. 1, 4, 17-21, 38-39), TPS2116 SLVSFG1A (p. 3; DRL0008A pp. 22-24), TLV1117LV SBVS160C (pp. 3, 13, 14), TPS2663 SLVSE94G (pp. 3-4); Vishay 69098 rev. E; UMW SUD50P06-15 (nov. 2024); Littelfuse 451/453 (p. 4); MDD SS310 (rev. 2024A5), BZT52C15 (rev. 2025A6); cjiang FXL0650 (pp. 5, 16).
- API JLCPCB `selectSmtComponentList` (2026-11-05); SimSurfing de Samsung (`product.samsungsem.com/mlcc/*.do`).
- MCP de KiCad: **no usado** (sin proyecto cargado; nada que cerrar). Los `.kicad_sym`/`.kicad_mod` se validan con `kicad-cli`.

## Acciones

- Todas las piezas de la lista existen en las oficiales de KiCad 10 con símbolo, huella y 3D salvo: símbolo LMR36520, huella JP1 y 3D del fusible. Se comprobó que cada `.step` de las huellas oficiales existe en la instalación.
- `esp-riego.kicad_sym`: añadido `LMR36520FADDA` (copia de `Regulator_Switching:LMR36510ADDA`, BOOT a pasivo, campos `LCSC Part#` C1858395 y `MPN`, datasheet de TI).
- `esp-riego.pretty/SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm.kicad_mod`: JP1 (DEC-0006).
- `esp-riego.pretty/Fuse_Littelfuse-NANO2-451_453.kicad_mod`: copia de la oficial con el 3D propio `libraries/3d/Fuse_Littelfuse-NANO2-451_453.step`, porque KiCad 10.0.6 no trae el `.step` oficial. Fuente: `fuentes-solidcraft/gen.py` (sección «Fusible») y `nano2.json`.
- `hardware/v2/sym-lib-table` y `fp-lib-table`: añadida la entrada `esp-riego` (`${KIPRJMOD}/../libraries/...`). El proyecto v2 no la tenía.
- Fichas nuevas: `LMR36520`, `TPS2116`, `TLV1117LV`, `SQD50P06-15L` (con el análisis de la alternativa UMW), `0451010.MRL`, `FXL0650-100-M`, `SS310`, `BZT52C15`. `TPS2663.md`: variante 26632 añadida.
- `componentes/bloque-alimentacion.md`: campos (fabricante, LCSC, tipo, stock, fecha) de las 4 clases de pieza, derating y pendientes de SPEC-0017.
- Datasheets copiados a `componentes/datasheets/` (LMR36520, TPS2116, TLV1117LV, SQD50P06-15L, SUD50P06-15-UMW, 0451010.MRL, SS310, BZT52C15).

## Decisiones y justificación

- Huella JP1 con la construcción de la oficial (pads en F.Cu y F.Mask, sin pasta, rectángulo en F.Mask sobre el hueco). Cotas de §3.13.9: pads 1,2 × 3,0 mm a ± 0,9 mm (paso 1,8), hueco 0,6 mm, apertura de máscara común 0,6 × 3,0 mm entre pads. Serigrafía a 0,25 mm de los pads, *courtyard* a 0,5 mm, marcas «1» en serigrafía y Fab.
- Se deja la huella oficial del LMR36520 aunque difiere del land pattern de TI (ver «Requiere verificación»): el alcance dice reutilizar las oficiales.
- Se crea un 3D propio para el fusible por faltar el oficial; mismas convenciones que los otros 3D propios.
- Derating: criterio de suma (tensión + temperatura) con los datos de Samsung. Para C2/C6/C7 (PSA) se usa de proxy un Samsung 100 V X7R 1210 de 4,7 µF; está indicado.

## Verificación

- `python herramientas/verificar.py hardware/v2`: ERC 0, DRC 0, paridad 0, LIMPIO (solo se tocaron las tablas).
- `kicad-cli sym export svg esp-riego.kicad_sym` y `fp export svg esp-riego.pretty`: cargan las 3 piezas nuevas sin error.
- `kicad-cli pcb render --side top` sobre una placa de prueba (scratchpad, no versionada): el fusible aparece con el 3D alineado con sus pads; JP1 muestra los dos pads con el hueco abierto, «1» a la izquierda.
- Cada `.step` de las huellas de la lista existe salvo el del fusible oficial, que se sustituye.

### Repaso de `checklists/librerias.md` v3

| Punto | Estado |
|---|---|
| Orden de preferencia, origen anotado en la ficha | Cumple (oficial → creado solo para LMR36520, JP1 y 3D del fusible) |
| Formato nativo; nada de EasyEDA | Cumple |
| `kicad-cli upgrade` antes de dar por no convertible | No aplica (sin JSON de EasyEDA) |
| Fidelidad en importaciones o conversiones | No aplica |
| `git diff` al sustituir una pieza | No aplica: las piezas son nuevas |
| Tablas con `${KIPRJMOD}` | Cumple (las dos entradas nuevas) |
| Tablas sin restos de la versión anterior | **No cumple**: `hardware/v2/*-lib-table` conservan 5 librerías de símbolos y 8 de huellas del TFG (PS2705, BC817, 1548129, PRT-10811, Wemos, KiCad, PhoenixTerminal, SMMS0530, DC-Jack). No las he quitado: no son de esta spec y `mcu.kicad_sch` y `salidas.kicad_sch` las nombran. Pendiente: coordinador |
| Land pattern del fabricante antes de derivar una huella | Cumple: JP1 es de §3.13.9 (no hay land pattern de fabricante); el fusible, del dibujo de Littelfuse p. 4 |
| Símbolo: pines y nombres con el datasheet | Cumple: LMR36520 frente a la Tabla 5-1 (p. 4); TPS2116 (p. 3); TLV1117LV (p. 3); SQD50P06 (p. 1); TPS26632 (Fig. 5-3, p. 3) |
| Tipo eléctrico | Cumple: BOOT a pasivo; VCC `power_out`; PAD `power_in` |
| Campos del símbolo | `LMR36520FADDA`: `Value`, `Footprint`, `LCSC Part#`, `MPN`, `Datasheet`, `Description`. Los oficiales traen los suyos; los campos del proyecto se rellenan al colocar (SPEC-0019), con `componentes/bloque-alimentacion.md` |
| Huella: tabla de cotas frente al datasheet | JP1: contra §3.13.9 (sin datasheet). Fusible: datasheet p. 4, coincide. TPS2116 y FXL0650: coinciden (fichas). LMR36520: la oficial **no** coincide con TI (ficha) |
| Pin 1 en serigrafía y Fab | JP1: «1» en ambas. El resto, oficiales |
| *Courtyard* y serigrafía fuera de pads | Cumple en JP1 |
| `pcb render`: pin 1 del 3D sobre el pad 1 | Fusible: sin polaridad, alineado. JP1: sin 3D |
| THT: patilla desde el corte; taladro | No aplica (solo SMD) |
| 3D presente y alineado, en `.step` | Fusible: creado y comprobado. Resto: existe en la instalación |
| Pads `custom` | No aplica |
| Extensiones 3D como binary en `.gitattributes` | Cumple (`*.step` y `*.STEP`) |
| Símbolo ↔ huella: números de pin | Cumple (`SUD50P06-15`/`TO-252-2`, `TLV1117-33`/`SOT-223-3_TabPin2`, TPS26632/RGE0024H pad 25 = EP, LMR36520/HTSOP pad 9 = EP) |
| Ficha: LCSC, tipo, fecha, datasheet, datos | Cumple en las 8 nuevas y en TPS2663. WJ500V y SMBJ33A conservan la suya |
| Datasheet del fabricante, revisión vigente | TI y Vishay: sí. Littelfuse, MDD y cjiang: espejo de LCSC (la web de Littelfuse da 403; no se localizó la URL de MDD ni de cjiang) |
| Piezas sin LCSC: API de JLCPCB | Cumple: todas con código. Datos de la API de JLCPCB (la base local del MCP está vacía) |

## Requiere verificación de validación

| Pieza | Qué | Datasheet y página |
|---|---|---|
| `esp-riego:LMR36520FADDA` (símbolo) | Pines y tipos | TI SNVSBF0C, Tabla 5-1, p. 4; ficha `LMR36520.md` |
| `esp-riego:SolderJumper-2_P1.8mm_Open_Pad1.2x3.0mm` (huella) | Cotas de §3.13.9: pads 1,2 × 3,0 mm, hueco 0,6 mm, apertura de máscara, sin pasta | Sin datasheet; `alimentacion.md` §3.13.9 (DEC-0006) |
| `esp-riego:Fuse_Littelfuse-NANO2-451_453` (huella; solo cambia el modelo 3D) | Pads 1,96 × 3,15 a ± 2,455 mm | Littelfuse 451/453, p. 4 |
| `3d/Fuse_Littelfuse-NANO2-451_453.step` | Cuerpo 6,10 × 2,69 × 2,69 mm, casquillos de 1,45 mm | Littelfuse 451/453, p. 4 |
| Huella oficial del LMR36520 (no modificada) | Difiere del land pattern TI: pads 2,2 × 0,5 a ± 2,875 mm frente a 1,55 × 0,6 a ± 2,7 mm. ¿Se acepta o se crea una propia? | TI SNVSBF0C, DDA0008B, p. 39 del PDF |

## Pendiente

- **ing-esquematicos** (observaciones del derating, `bloque-alimentacion.md` §3; para la spec de mantenimiento o SPEC-0019, según decida el coordinador):
  - **C7 no basta como CIN de U2:** da 3,0–3,4 µF efectivos a 24–30 V y el datasheet pide ≥ 4,7 µF efectivos (pp. 17 y 20). Con C2 junto a U2 se cumple. Falta reflejarlo en §8.
  - C3 (IN_SYS): 62–72 nF efectivos frente a «≥ 0,1 µF»; propuesta 220 nF 100 V.
  - C10 (CVCC): 0,64 µF efectivos frente a «1 µF» de la p. 21.
  - §3.13.4 usa 7,9 µF para C2+C6/C7 y 28 µF para C11/C12: con el fabricante salen 6,4–7,1 y 26,8 µF. No cambian las conclusiones.
  - FXL0650-100-M: I_sat y I_rms de §3.6 son los **típicos** (5,3 y 4,5 A); los máximos garantizados son 4,24 y 3,8 A (p. 16). Se sigue cumpliendo 3,6 A.
- **Coordinador:**
  - R8: Yageo RT0603BRD0724K9L (C136967, 25 ppm, 14 308 en stock) en vez de Viking C4156365 (774).
  - C1591 (Extended) → Yageo C14663 (Basic) en C5, C9, C13, C14, C20, C21.
  - El bloque lleva 20 piezas Extended distintas y 9 Basic.
  - Limpiar las tablas de v2 de restos del TFG (ver checklist).
  - Los archivos `.claude/agent-memory/ing-esquematicos/*` aparecen modificados y sin seguimiento; no son míos.
- **Validación:** la tabla anterior. No pude confirmar la revisión vigente de Littelfuse, MDD y cjiang.

## Notas para el siguiente agente

- SPEC-0019: usar `esp-riego:Fuse_Littelfuse-NANO2-451_453` para F1 (no la oficial `Fuse:`: su 3D no existe en KiCad 10.0.6), `esp-riego:LMR36520FADDA` para U2 y las demás oficiales de `bloque-alimentacion.md`. Los campos `LCSC Part#`, `MPN`, `Datasheet` y `Description` salen de ese archivo y de las fichas.
- El símbolo `TLV1117-33` y `TPS26632RGE` oficiales no traen las huellas del proyecto (TLV1117 sin huella): se asignan al colocar.
- JP1: atributos `exclude_from_bom` y `exclude_from_pos_files` ya en la huella.
