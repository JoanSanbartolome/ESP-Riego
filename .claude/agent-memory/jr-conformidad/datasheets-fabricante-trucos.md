---
name: datasheets-fabricante-trucos
description: Donde bajar datasheets y land patterns de fabricante (Infineon, Sensirion, TI) y que sitios bloquean
metadata:
  type: reference
---

- Infineon: `infineon.com/package/<encapsulado>` trae la imagen "footprint" (land pattern): `assets.infineon.com/is/image/infineon/infineon-<pkg>-png-footprint-en.png`. Datasheets: `infineon.com/assets/row/public/documents/10/49/infineon-<mpn>-datasheet-en.pdf` (el PDF de LCSC era identico).
- Sensirion: la URL de la ficha daba 404; la vigente sale de `sensirion.com/products/catalog/SHT40` (V7.3, jun 2026). Mirar siempre la pagina de producto.
- ST (timeout), Littelfuse (403), HRO y Kangnex (sin acceso) no responden desde curl ni WebFetch: dejar nota de "revision no confirmada".
- La guardia confunde variables de shell en rutas de mkdir y rm: usar rutas literales del scratchpad; rm esta bloqueado fuera de la zona.
- En .kicad_mod la sangria es una tabulacion para los hijos directos; con dos tabulaciones un replace no encaja y falla en silencio.
