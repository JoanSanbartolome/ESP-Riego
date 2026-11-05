---
spec: SPEC-0018
agente: jr-conformidad
n: 03
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 03 · jr-conformidad

## Orden
Corregir VAL-0018-01 hallazgos 01, 02, 06, 07 (no tocar docs/diseno/). MCP: solo `validate_symbol_library`; sin proyecto cargado.

## Acciones
- 01: `esp-riego:SMBJ33A` en `esp-riego.kicad_sym`: pin 1 = K (cátodo, izq.), pin 2 = A; forma de `Diode:SM6T33A` (K en pin 1, mismo mapeo a pad 1 de `Diode_SMD:D_SMB`, pad 1 = cátodo por convención KiCad). Campos Footprint, Datasheet, Description, `LCSC Part#` C224019, `MPN`. Fichas `SMBJ33A.md` y `bloque-alimentacion.md` (fila D2) actualizadas. `Device:D_TVS` descartado (bidireccional).
- 02: huella propia `esp-riego.pretty/Texas_DDA0008B_HTSOP-8-1EP_3.9x4.9mm_P1.27mm_EP2.95x4.9mm_Mask2.71x3.4mm.kicad_mod` (derivada de la oficial): pads 1-8 de 1,55×0,6 a ±2,7; EP Cu 2,95×4,9 (+B.Cu 2,6×3,3); máscara y pasta EP 2,71×3,4 (margen 0); 6 vías 0,2/0,45 sin máscara (tapadas); courtyard ±3,8×±2,75; 3D oficial (sin cambios). Símbolo `LMR36520FADDA` apunta a ella. `LMR36520.md` y `bloque-alimentacion.md` corregidos (se elimina el error «pasta 2,6×3,3» y «caben en ambos»).
- 06: JP1 `(zone_connect 2)` (sólido).
- 07: JP1 `Reference` a y = −2,9.

## Verificación
- `validate_symbol_library`: válida, 5 símbolos. `kicad-cli fp export svg` de la huella nueva: parsea y traza.
- `verificar.py hardware/v2`: ERC 0, DRC 0, paridad 0 (LIMPIO).
- No hecho: DRC de placa de prueba para JP1 (07) ni render 3D de U2; lo repite validación.

## Requiere verificación de validación
- `esp-riego:SMBJ33A` (símbolo): Littelfuse smbj.pdf, p. 1-2 (polaridad, sufijo A) y p. 5 (dibujo SMB; cátodo/banda). Comprobar K→pad 1.
- Huella DDA0008B de U2: `datasheets/LMR36520.pdf` pp. 38-40 (4214849/B). Vías tapadas bajo pasta (nota 10) y pasta 2,71×3,4 a 0,125; decidir si 3,03×3,80 a 0,1 mm.
- JP1 (huella modificada): `alimentacion.md` §3.13.9 (zone_connect, referencia).

## Checklist librerías v3
- Símbolo polarizado con polaridad visible y K en pad marcado: cumple (D2).
- Huella oficial/propia con tabla de cotas: cumple (ficha LMR36520.md).
- zone_connect coherente en huellas de potencia: cumple (JP1).
- Tablas sin restos (hallazgo 08): sin cambios; pendiente a la spec de mantenimiento.
- Pendiente: 03, 04, 05 y 08 no son de este encargo.
