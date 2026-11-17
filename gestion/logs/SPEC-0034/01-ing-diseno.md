---
spec: SPEC-0034
agente: ing-diseno
n: 01
fecha: 2026-11-17
estado: completado
---

# SPEC-0034 · 01 · ing-diseno

## Hecho

- `docs/diseno/salidas.md`: tabla de límites de uso REL-11 en §0 (valor, origen, consecuencia); §1, §3.2–§3.4 con la carga como parámetro; §5 rehecho (rueda libre montada: §5.1 energía en el BTT, §5.2 apagado normal, §5.3 corto e I_FSM, §5.4 fuga frente a R_OL, §5.5 cierre); §8 serigrafía; §9, §11, §12 (avisos de carga baja y de suma de 3,5 A), §13, §14 y anexos sin válvula de referencia ni DNP.
- `hardware/v2/salidas.kicad_sch`: D12–D17 `dnp no`, `in_bom yes`, `in_pos_files yes`; Description «…, montado (DEC-0014)»; nota de la hoja; fecha 2026-11-17. `esp-riego.kicad_pcb`: huellas de D12–D17 con `(attr smd)`. BOM y CPL (`--exclude-dnp`) con las 6.
- `docs/diseno/estudio-salidas.md`: aviso de documento histórico en la cabecera.
- `viabilidad-expansion.md` §0, §1, §2.3 y §12.2; `alimentacion.md` §1; `sensores.md` §0, §5 y §9 (caso de carga = suma de 3,5 A; las 6 salidas a 0,25 A, ejemplo). Las menciones de `sensores.md` estaban en §0 y §5, no en §6 y §7.
- Memoria: `project_salidas_d8.md`, índice y `reference_herramientas_kicad.md`.

## Decisiones y desviaciones

- Carga mínima del diagnóstico en ON: 80 mA en el peor caso (entrada a 18 V, bobina caliente) ⇔ ≤ 218 Ω, con el umbral de 18 mV sin cambiar (§3.2).
- Aviso de suma sobre LIM_IMON > 3,3 A: con ± 7 % es el único umbral que avisa siempre con 3,6 A (prueba de `docs/02` §6); puede avisar desde 3,05 A (§12).
- Serigrafía en ASCII, tres líneas por grupo de bornes (§8); «una carga por salida» va al manual, no a la serigrafía.
- Límites que añado y que no lista REL-11: sin PWM y sin solenoides biestables (§0, fila «Tipo de carga»).

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 errores, paridad 0, 448 sin conectar (placa sin rutar). Puntos [auto]: falla `esquema.dnp` (6: la tabla `campos-salidas.csv` aún dice DNP), pendiente de jr-conformidad.
- Imagen de la hoja de salidas y del cajetín revisadas (D12–D17 sin la cruz de DNP, cátodo a OUTn).
- Cálculos reproducibles en §3.2, §3.3, §5 y §12 (fórmula y página en cada uno).

## Para validación

- §5.3: I²t del corto (0,098 A²s) frente a I_FSM²·t/2 (3,75 A²s); el M7 no da I²t, se deriva de la semionda. El caso con JP1 cerrado (impulsos repetidos mientras el BTT conmuta por temperatura) no está calculado: queda como prueba de prototipo (§13.9).
- §5.4: fuga del M7 con la cota de 50 µA (125 °C, 1000 V), muy conservadora; típica ≤ 1 µA (Fig. 2).

## Pendiente

- jr-conformidad: `campos-salidas.csv`, fila D12–D17, `DNP` = no y `Description` = «Rectificador 1 kV 1 A SMA: rueda libre del canal n (K = OUTn / A = GND), montado (DEC-0014)», igual que el esquema; hoy difieren en las dos (`campos.py revisar`: 12 diferencias). Además `M7.md` y `bloque-salidas.md`.
- Usuario: la válvula instalada (bobina AC en continua) disipa 14–16 W a 24 V; que lo admita es dato de la válvula (`salidas.md` §0 y §13.10).
