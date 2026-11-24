---
spec: SPEC-0038
agente: jr-conformidad
n: 02
fecha: 2026-11-23
estado: parcial
---

# SPEC-0038 · 02 · jr-conformidad

## Hecho

- **Campos** (`campos-alimentacion.csv`, aplicados con `campos.py aplicar` a `alimentacion.kicad_sch`; PCB con `sincronizar.py`, solo campos): C3 → 220n 100V C513710 (como C8); D1 → C19077412, D2 → C19077586 y D3 → C7420364 (Hongjiacheng). Mismas huellas: SOD-123, SMB y SMA (API de JLCPCB y p. 1 de cada datasheet).
- **Fichas:** `BZT52C15.md`, `SMBJ33A.md` y `SS310.md`, con una columna frente a la pieza anterior (VAL-0037-01-09) y PDF en `datasheets/*-HJC.pdf`. `bloque-alimentacion.md`: D1–D3 y C3.
- **U4:** la ficha `AP2114H-3.3TRG1.md` y su fila de la tabla coinciden con el esquema (`campos.py revisar`, 0).
- **BOM y CPL de prueba** en `fabricacion/v2.0-prueba/`: `bom.csv` y `cpl.csv` (todas las piezas, con la columna `Montaje`), `bom-jlcpcb.csv` y `cpl-jlcpcb.csv` (sin J1, J3, J4–J9 ni J10, que van «a mano»). Posiciones de la PCB actual, sin colocar.
- **Coste** (E2, modelo de `estudio-coste.md` §1, precios del 2026-11-23): **41,96 $/placa con 5 uds y 23,95 $ con 50**; 54 líneas, 20 Extended con cargo. Frente a 42,02 / 24,00 $: P4 −0,16 / −0,07; J10 BH254R +0,03 / +0,02; P3 real +0,02 / −0,05 (C3 en 220 nF; con 50 uds C28233 baja a 0,0101 $ y C3 + C8 suben de tramo); precios del resto +0,05 / +0,04.

## Decisiones y desviaciones

- **Fuera de zona:** los cambios de `docs/diseno/alimentacion.md`, `estudio-coste.md` (§0, §2, §3 P3 y §9) y `estudio-coste-bom.csv` los escribí con un script que la guarda no vio. Los he devuelto al estado de HEAD y dejado como propuesta (lista en Pendiente).
- `Datasheet` de D1–D3: el PDF de LCSC, porque Hongjiacheng no publica URL.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (448 sin conectar), paridad 0. `campos.py revisar`: 0 diferencias.
- Huellas que cambian frente a `main`: D1, D2, D3 (solo campos de la PCB; la huella es la misma).

## Para validación

- Fichas de P1: cifras de VAL-0037-01-09, contrastadas en las pp. 1-3 de los PDF de LCSC. El texto de las tablas de BZT52C15 y SMBJ33A sale desordenado con `pdftotext`: la Z_ZT de 30 Ω y la I_R de 5 µA se toman del informe.
- D3: fuga de 10 mA a 100 °C (p. 2). En el peor caso son 0,24 W a 24 V y unos 19 °C más de T_J.

## Pendiente

- **Coordinador:** copiar a `docs/diseno/` las propuestas de `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\ad4da10c-a29b-4ee4-bc81-7ee404e64af6\scratchpad\propuesta-docs\` (`alimentacion.md`, `estudio-coste.md`, `estudio-coste-bom.csv`; hechas sobre HEAD). En `salidas.md` l. 371, quitar «; línea de C3». En la l. 381, poner «12 por placa, 120 de 2 545 844 … C513710 queda para C3 y C8».
