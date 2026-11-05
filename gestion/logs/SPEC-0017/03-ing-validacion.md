---
spec: SPEC-0017
agente: ing-validacion
n: 03
fecha: 2026-11-05
estado: completado
---

# SPEC-0017 · 03 · ing-validacion

## Orden recibida

SPEC-0017 · rama spec/SPEC-0017-calculos-alimentacion · nivel ligero · Lee: spec, DEC-0006, `docs/diseno/alimentacion.md`, logs 01 y 02 · Haz: criterios de aceptación; recalcular UVLO, banda del limitador, precisión de VIN, tensión nominal frente a Vc + 10 % y puente JP1; contradicciones con docs/02 v0.4 y DEC-0003/0004/0006. Sin MCP · Entrega: VAL-0017-01 + este log.

## Acciones

- Rama y commit comprobados: `spec/SPEC-0017-calculos-alimentacion`, `cfe843a`.
- Documento leído antes que los logs. Recálculos en el informe.
- Datasheets: TPS2663 (SLVSE94G), LMR36520 (SNVSBF0C), TPS2116, SQD50P06-15L, ESP32-S3 v2.2 (ADC y pines), SMBJ33A (PDF local), Littelfuse 451 (I²t y R). Leídos desde las extracciones de texto del scratchpad compartido, ya descargadas por el autor, más PDF propio para SMBJ33A.
- LCSC (JSON `wmsc`): 9 piezas, stock y tramos coinciden.
- KiCad 10: símbolos y huellas citados existen (incluidos `L_Changjiang_FXL0650`, `TPS26632RGE`, `SOT-583-8`).
- Sin MCP, sin `verificar.py`: el diff contra `main` no toca KiCad.
- Logs 01 y 02 contrastados: coinciden con los artefactos. «Verificación: LIMPIO» es cierta por no haber cambios.

## Resultado

5 hallazgos: 0 C, 0 A, 1 M, 4 B. Veredicto APROBADO_CON_OBSERVACIONES. Informe: `gestion/informes/VAL-0017-01.md`.

## Pendiente

- Coordinador: corregir el hueco de JP1 (01) antes de SPEC-0018; el resto, a mantenimiento o a SPEC-0018/0019.
- La guardia bloquea `python` con código en línea que escribe archivos: los cálculos se hicieron a mano y con scripts de solo lectura.
