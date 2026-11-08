---
spec: SPEC-0022
agente: ing-validacion
n: 03
fecha: 2026-11-07
estado: completado
---

# SPEC-0022 · 03 · ing-validacion

## Orden recibida

Validar SPEC-0022 con nivel completo (VAL-0022-01) sobre una copia y comprobar que el repositorio no cambia.

- Rama `spec/SPEC-0022-hoja-mcu` ✔. HEAD `38090d2`, sin commits nuevos durante la revisión. MCP no usado.

## Acciones

1. Se leyeron la spec, DEC-0007, la checklist `esquema.md` v6, `mcu.md`, las tablas de campos de los logs 01/03 de SPEC-0021, VAL-0021-01 y `salidas.md` (§3 y §12). Los logs 01/02 de esta spec, al final.
2. Copia en `scratchpad\v22\hw`. MD5 de `hardware/` y `docs/` antes y después: 234 archivos, iguales.
3. `verificar.py` sobre la copia: ERC 0/0, DRC 0/0 (172 sin conectar), paridad 0.
4. Netlist `kicadxml` → `net.py`: campos de las 21 piezas y redes pin a pin frente a `mcu.md` §4–§10.
5. `labels.py`: 25 etiquetas jerárquicas con sus formas; los 25 pines de la hoja en la raíz; 5 etiquetas locales hacia Alimentación; 21 NC.
6. `pcb_an.py`, `nets_cmp.py` y `pcb_cmp.py`: cruce pad↔netlist (0 diferencias), redes 77/77, courtyards fuera del contorno, diff semántico frente a `047cabd` (solo +21 huellas y la red de 11 pads). Diff *patience* +5 865/−11.
7. PDF de la copia: cajetín de la hoja MCU correcto; U5, U6 y J2 legibles a 300 ppp.
8. Recálculos:
   - `en_sim.py` (EN): 0,1587 con el buck de 6 ms; 9,9–18,5 ms de liberación;
   - LED, con el PDF del KT-0603R;
   - U6, con la tabla 2 de ST (PDF local) y el §6 del UMW;
   - API de JLCPCB (`jlc.py`).
9. Los PDF del KT-0603R y del UMW los descargó ing-esquematicos en `scratchpad\s22`; los copié a `v22\ds_ext`. LCSC bloquea la descarga directa.

## Resultado

APROBADO_CON_OBSERVACIONES. Los 6 criterios se cumplen. Hallazgos:
- -01 (M): no hay ficha con la polaridad del KT-0603R, y la numeración de su datasheet es la inversa de la de KiCad;
- -02 (B): la cota I_mín de D5 usa VDD nominal;
- -03 (B): `hardware/v2/README.md` describe la PCB y la verificación de antes del paso 2;
- -04 (B): la decisión de pasar D5 a rojo no está registrada.

## Contraste con los logs

- Log 01: lo que afirma coincide con los artefactos (netlist, campos, raíz, recálculos). La afirmación de que `README.md` está actualizado solo es cierta tras el paso 1 (-03).
- Log 02: el cruce de 0 diferencias, los 172 sin conectar y el diff de +5 865/−11 se reproducen.

## Pendiente

- Coordinador: -01, antes de la spec de Salidas o en la de mantenimiento; -03 y -04.
