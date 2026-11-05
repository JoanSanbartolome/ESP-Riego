---
spec: SPEC-0018
agente: ing-validacion
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0018 · 02 · ing-validacion

## Orden

Validación completa de SPEC-0018. Revisar sobre todo el símbolo LMR36520FADDA, JP1, el fusible NANO2 y su 3D, la huella del LMR36520 frente a DDA0008B, y el *derating* de C7, C3 y C10.

## Hecho

- Rama correcta; HEAD 52e574f, entregable en 1d68288. MCP sin proyecto cargado y sin `.lck`; no se ha hecho `open_project`.
- `verificar.py` sobre una copia en el *scratchpad* (`v18\hw`): LIMPIO.
- Símbolo: es igual que el oficial LMR36510ADDA salvo BOOT (pasivo) y coincide con la Tabla 5-1 (p. 4). `validate_symbol_library` sobre la copia: válida.
- Pines de las oficiales (`v18\refs.py`): SUD50P06-15, TLV1117-33, TPS2116DRL y TPS26632RGE coinciden con sus datasheets. Huellas de TO-252-2, SOT-223 y SOT-583: coinciden. Los 22 `.step` existen.
- JP1, fusible y STEP: cotas comprobadas. Placa de prueba (`v18\mk_pcb.py`): DRC con 1 `silk_overlap`; el render del fusible y de U2 es correcto.
- DDA0008B en las pp. 38-40: se aparta de la oficial en la anchura y la longitud del pad, en la máscara y la pasta del EP y en las vías abiertas.
- API de JLCPCB: 16 códigos coinciden. SimSurfing (`v18\ss.py`): ΔC reproducidos. C28323 da −2,5 % a 5 V.
- Por último, el log 01: le faltan la polaridad de D2 y la serigrafía de JP1, y la salida «C2 junto a U2» no encaja con §8.

## Resultado

RECHAZADO. Hallazgos: 1 A (D2 con `D_TVS` bidireccional), 4 M (huella de U2, C7, C10, `zone_connect` de JP1) y 3 B (C3, serigrafía de JP1, restos en las tablas). Bloquean SPEC-0019 el 01 y el 03; el 02 se recomienda corregirlo con ellos. Informe: `gestion/informes/VAL-0018-01.md`.
