---
spec: SPEC-0024
agente: ing-validacion
n: 02
fecha: 2026-11-10
estado: completado
---

# SPEC-0024 · 02 · ing-validacion

## Orden recibida

Validar SPEC-0024 a nivel completo, en el commit `c2401d6` de la rama `spec/SPEC-0024-piezas-salidas`, sin abrir `hardware/v2` con el MCP ni con kicad-cli. Puntos 1–7 de la orden: huella del BTT6050, resto de huellas y 3D, símbolo y mapeo, fichas, JLCPCB, tabla de campos y cambios a `salidas.md`.

## Acciones

1. Rama y commit comprobados (`c2401d6`). Diff frente a `60cec8d`: 15 archivos, nada en `hardware/v2` ni en `docs/`.
2. Huella: cotas recalculadas desde el `.kicad_mod`. Placa de prueba con el `.kicad_pro` de v2, la huella nueva y la de `60cec8d` (control): DRC limpio. Gerber y Excellon analizados (pasta, máscaras, taladros).
3. Imagen del *land pattern* descargada con `curl` (`infineon-pg-tdso-14-11-png-footprint-en`): sin vías y con pasta al 85 %.
4. Capacidades de JLCPCB consultadas (pcb-capabilities): reglas de vías rellenas y distancia entre taladros de vías y de pads.
5. `verificar.py` sobre una copia de `hardware/v2` + `libraries`: ERC 0, DRC 0, paridad 0.
6. Existencia de los 10 modelos 3D y ausencia de `thru_hole` en las huellas oficiales, comprobadas por script.
7. Datasheets: BTT6050 (pp. 2, 4, 8, 9, 10, 22, 30, 48), BTT6030 (p. 4) y M7 (pp. 1 y 3, renderizadas).
8. API de JLCPCB: 20 códigos y búsqueda de Basic para las dos Extended pasivas.
9. Campos de `alimentacion.kicad_sch` y `mcu.kicad_sch` leídos por script, sin abrir el proyecto.
10. Contraste con el log del autor (después de formar los hallazgos).

## Resultado

Informe: `gestion/informes/VAL-0024-01.md`. Veredicto **APROBADO_CON_OBSERVACIONES**: 3 M y 4 B.

- **01 (M):** la pasta al 49,6 % no se demuestra suficiente con las vías abiertas por arriba. Hay una propuesta del 65 %.
- **02 (M):** el tapado de las vías por B.Cu no está garantizado por JLCPCB.
- **03 (M, afecta a SPEC-0025):** falta la l. 69 de `salidas.md` («sin vías»), y el cambio 1 omite D5.
- **04–07 (B):** cita de JLCPCB, fichas, forma de las propuestas e incoherencias de campos que vienen de antes.

## Pendiente

- Coordinador: corregir la 03 antes del merge (cambio 11 y D5 en el cambio 1). Decidir la pasta y el tratamiento de las vías (01 y 02) antes del layout de salidas.
