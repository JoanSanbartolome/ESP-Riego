---
spec: SPEC-0020
agente: ing-validacion
n: 02
fecha: 2026-11-06
estado: completado
---

# SPEC-0020 · 02 · ing-validacion

## Orden recibida

SPEC-0020 · rama spec/SPEC-0020-calculos-mcu (activa en C:\Users\josan\proyectos\KICAD_mcp) · nivel completo · Lee: gestion/specs/SPEC-0020-calculos-mcu.md + docs/diseno/mcu.md + gestion/logs/SPEC-0020/01-ing-esquematicos.md + docs/diseno/alimentacion.md · Haz: validar contra la spec, requisitos, datasheets y checklists (requisitos.md, esquema.md «Cálculos» y «Microcontrolador»). Valora ambas variantes de DEN (§9.2 común y §9.3 por canal); la elección es del usuario, no la cuentes como hallazgo. Revisa también choques de referencias provisionales con alimentacion.md (p. ej. C22, que alimentación ya usa como CIN de U2). Sin KiCad necesario; si lo usas, close_project. · Entrega: gestion/informes/VAL-0020-01.md + log gestion/logs/SPEC-0020/02-ing-validacion.md. Brevedad: solo contrato de salida; log telegráfico.

## Contexto consultado

- Rama `spec/SPEC-0020-calculos-mcu`. HEAD al empezar: 304771e; al terminar: a406117 (DEC-0007, del coordinador; `mcu.md` no cambia).
- Spec, DEC-0007, `docs/02` v0.4, `mcu.md`, `alimentacion.md` y `estudio-salidas.md`. Checklists `esquema.md` v5 y `requisitos.md` v3.
- Datasheets:
  - WROOM-1 v1.8: pp. 3, 11-16, 27-28 y 41;
  - S3 v2.2: pp. 16-19;
  - HDG: pp. 7-9, 13, 15, 18-19 y 28-31;
  - TLV1117LV: pp. 5 y 8;
  - LMR36520: p. 7;
  - TPS2116: pp. 7 y 15;
  - BTT6050: pp. 21 y 34;
  - USBLC6: p. 2.
- Librerías de KiCad 10: símbolos `ESP32-S3-WROOM-1`, `USBLC6-2SC6`, `USB_C_Receptacle_USB2.0_16P` y `SW_Push`; huellas WROOM-1 (*keepout*), TS-1187A y HRO; carpetas de 3D.
- LCSC JSON (25 códigos) y SimSurfing CL21A226MAQNNN, a 2026-11-06.

## Acciones

- Recálculos en el *scratchpad* `val20/`:
  - `en_sim.py`: EN con τ de 7,35–10 ms, con y sin el TPS2116;
  - presupuesto de +3V3, TLV1117LV, *pull-downs*, I²C, LED y coste;
  - mapeo de pines GPIO ↔ módulo ↔ símbolo.
- Lectura de las tablas 2-1/2-2 del S3 y de la tabla 12 y las Fig. 24/26 de la HDG, renderizadas.
- Escrito el informe `gestion/informes/VAL-0020-01.md`.

## Decisiones y justificación

- Las variantes de DEN no cuentan como hallazgo: el usuario eligió en DEC-0007. Las dos cumplen REL-04.
- C22 duplicada → M: SPEC-0019 ya la dibuja en alimentación, y SPEC-0021/0022 toman las referencias de `mcu.md`.

## Verificación

- `verificar.py`: no aplica, porque la rama no cambia KiCad. Sin MCP ni `kicad-cli`.
- Veredicto: APROBADO_CON_OBSERVACIONES (1 M, 6 B).

## Pendiente

- ing-esquematicos: VAL-0020-01-01 antes del merge. 02–07, a mantenimiento o junto con la 01.
- jr-conformidad (SPEC-0021): Basic y stock en JLCPCB de C14663 para C24 (DEC-0007).

## Notas para el siguiente agente

- El log 01 dice «C22–C25 siguen a alimentación»: es falso desde el merge de SPEC-0018.
- C15849 tiene stock de nuevo (211 050, 2026-11-06).
