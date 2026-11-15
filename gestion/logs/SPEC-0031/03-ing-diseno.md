---
spec: SPEC-0031
agente: ing-diseno
n: 03
fecha: 2026-11-15
estado: completado
---

# SPEC-0031 · 03 · ing-diseno

## Hecho

- `docs/diseno/conectores.md`: completo. Tiene el resumen con la tabla de restricciones, la comparación del paso 1 corregida (§1.3 y la fila B'' de §1.5–1.6) y EXP-02 con las referencias definitivas (§2). También los pulsadores según DEC-0013 (§3), los bordes con los taladros M3 (§4), la justificación, el símbolo, los riesgos, la trazabilidad y el Anexo A de etiquetas.
- `hardware/v2/conectores.kicad_sch` (A3, 32 piezas), `mcu.kicad_sch`, `esp-riego.kicad_sch` y `esp-riego.kicad_pcb` (28 huellas nuevas sin colocar). En la hoja MCU, U5-29 pasa a EXP_EN, U5-30 queda NC y U5-32 pasa a BTN_INT. En la raíz se quitan 5 NC y se añaden 7 pines y 12 etiquetas.
- `hardware/libraries/esp-riego.kicad_sym`: símbolo nuevo `TPS2553DBVR` (SLVS841G p. 4).
- `docs/diseno/mcu.md`: cambios de §10.6 (§9.2, §10.1, §10.2, Anexo B; §14.2 cerrada), GPIO39 = BTN_INT, bus de la placa a 100 kHz y restos de EXP-01. Restos de EXP-01 también en `estudio-salidas.md` (S6 y §1.8), `ESP32-S3-WROOM-1.md` y `hardware/v2/README.md`.
- `hardware/componentes/campos-conectores.csv`: fila `H1-H4` (MountingHole, fuera del BOM), para que `campos.py revisar` dé 0 diferencias con la tabla.

## Decisiones y desviaciones

- BTN_INT es el nombre de la red del INT de U18 (GPIO39), en `mcu.md` y en las tres hojas.
- Tres uniones con cable, porque `hoja.py` no dibuja cables: EN–IN de U14/U15, los GND 2-4-6-8 de J10 (girado 180°) y A0–A2 de U18. Por eso `hoja.py generar` ya solo funciona en esta hoja con `--forzar`, y después hay que volver a añadir los cables.
- I_OS con la R al 1 %: 343–440 mA y 104–146 mA (p. 16, rev. G). Las de jr-conformidad, 347–435 y 105–144 mA, no incluyen la tolerancia.
- Bordes: se reservan 8 mm por esquina (patio del taladro 7,45 mm; cabeza y arandela M3 7,5 mm). Superior: 34 de 84 mm; inferior: 71 de 84 mm.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 (0 avisos), paridad 0. Sin conectar: 448 (antes 358; +90, todas de las 28 huellas nuevas).
- Fallan `librerias.gitattributes` (\*.WRL) y `librerias.fichas`: C23162, C23186, C23345 y C45783, todos de la hoja MCU y de antes (SPEC-0028). C19666 ya no falla.
- `campos.py revisar`: 0 diferencias con las tablas. Las 20 «misma pieza con campos distintos» son de antes (Alimentacion sin `Fabricante`; `Value` de C23 «1uF» frente a C15 «1u»). Las piezas nuevas siguen a su tabla.
- Netlist (`kicad-cli`) frente al plan: correcta red a red (Anexo A de `conectores.md`). `huella.py --simbolo`: los 6 pines del TPS2553 con su pad.
- Imágenes de la hoja Conectores, de la zona de U5 y de la raíz: sin solapes. El cajetín (A3, fecha y comentario 1) se ha mirado en el render de `vista.py`, no en el PDF.
- Checklist `[juicio]`: el pinout frente al YAML (FW-02) no aplica, porque todavía no hay YAML. El *derating* de C50/C51 es el de `viabilidad-expansion.md` (el TPS2553 no pide una C_OUT mínima).

## Para validación

- Símbolo `esp-riego:TPS2553DBVR` (pines y tipos en §6, p. 4 del datasheet). Es creación propia, así que hay que verificarlo.
- Supuestos: ≈ 10 pF del TCA9554 y ≈ 10 cm de pista en el bus de la placa (C_bus ≈ 70 pF). Cabeza M3 con arandela de Ø 7 mm.
- Herramientas: `hoja.py` (extraer ×3, pines ×7, generar ×5), `huella.py` ×6, `vista.py` ×7, `sincronizar.py` ×1, `campos.py` ×4, `verificar.py` ×3 y `comprobar.py` ×1.
- Scripts de la carpeta temporal: `s31_simbolo.py` (símbolo), `s31_con_json.py` (descripción de la hoja), `s31_cables.py` (cables) y `s31_raiz.py` (raíz). Además, cuatro trozos de Python en línea (JSON de MCU, netlist y páginas de datasheets).

## Correcciones de VAL-0031-01

- -01: `sensores.md`, las cuatro líneas (Dirección, Bus I²C de la placa, §3, §8) pasan a 100 kHz, con U18 TCA9554 (0x20) en el mismo bus.
- -02: `TPS2553.md`, cabecera: `simbolo: esp-riego:TPS2553DBVR (creación propia…)` y `origen_assets: … símbolo propio`.
- -03: `Description` del símbolo, «75-1700 mA typ.», en la librería y en la copia de `lib_symbols` de `conectores.kicad_sch`, que se cambia también para no dar `lib_symbol_mismatch`. `verificar.py`: ERC 0, DRC 0 con 448 sin conectar, paridad 0.
- -04: `mcu.md`, Anexo C: borrada la fila antigua de I2C_SDA/SCL.
- -05: `conectores.md` (§0, Fuentes y §2.3) y `TPS2553.md` citan las pp. 16–17, ec. (1)–(3); `TCA9554PWR.md`, la p. 25. La nota de la hoja Conectores sigue con «SLVS841G p. 16», porque no se tocan las hojas.
- -06: no se corrige; queda para SPEC-0028. Retiro la petición de ampliar `hoja.py`: basta con `P:<red>` en cada pin.

## Pendiente

1. Coordinador: la fila `H1-H4` añadida a `campos-conectores.csv` (archivo del paso 3).
2. SPEC-0028: quitar los 7 cables de `conectores.kicad_sch` (VAL-0031-01-06) y cambiar la cita de la nota a «pp. 16–17».
