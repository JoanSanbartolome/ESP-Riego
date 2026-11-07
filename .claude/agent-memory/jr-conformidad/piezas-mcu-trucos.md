---
name: piezas-mcu-trucos
description: Códigos LCSC/JLCPCB fiables del bloque MCU, 3D propios con SolidCraft y trampas de la guardia y de la API
metadata:
  type: reference
---

- Basic confirmado (2026-11-06): C14663 (100 nF, 34,7 M), C318884 (TS-1187A-B-A-B), C45783, C19666, C15849 (1 µF 50 V X5R, −18 % a 3,3 V), C2286 (LED rojo). Extended: módulo C2913198, J2 C165948, USBLC6 C7519/C2687116, tira C124378, LED C2289.
- El stock de LCSC no vale para JLCPCB (C14663: 0 en LCSC, 34 M en JLCPCB): usar la API.
- Código de pedido XKB TS-1187A-X-X-X: fuerza / altura H (A 1,5 … E 2,5 mm) / tecla. La alternativa C-E-B mide 2,5 mm.
- Los PDF de LCSC pueden ser de otro modelo (KT-0603YG → XL-0603QYGC).
- 3D propio: `hardware/libraries/3d/fuentes-solidcraft/gen_*.py` + `solidcraft-cli run x.json --out y.step`; `sketch.create` plano `XY` con `offset` para extruir polígonos.
- La guardia no admite `$VAR` en rutas de salida ni `cd` a rutas inexistentes: usar rutas literales; imprimir la URL firmada de la API satura el contexto (guardar en fichero).
- Sufijo de Uniroyal `…WAF220J…`: «J» es el multiplicador (22 Ω), no la tolerancia (WAF = 1 %).
