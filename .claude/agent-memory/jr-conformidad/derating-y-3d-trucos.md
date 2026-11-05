---
name: derating-y-3d-trucos
description: Curvas de derating de MLCC de Samsung (SimSurfing), buscador de JLCPCB por palabra clave y 3D de fusible creado
metadata:
  type: reference
---

- Samsung SimSurfing: `curl -A Mozilla/5.0 https://product.samsungsem.com/mlcc/<MPN sin la última letra>.do` devuelve HTML con JSON embebido (`"graphType" : "DCBias"` y `"TCC"`, puntos x/y de ΔC). Se parsea balanceando llaves. Sirve para cualquier Samsung CLxx; una página de 21 603 bytes es «no existe». Para otros fabricantes (PSA), proxy Samsung de la misma tensión y tamaño: 4,7 µF 100 V 1210 = `CL32B475KCJZ4N`.
- `selectSmtComponentList` también busca por texto libre (`"RT0603BRD0724K9L"`, `"4.3k 0603 1%"`): sirve para hallar alternativas Basic o con stock. Código Basic de 100 nF 50 V 0603: C14663.
- KiCad 10.0.6 no trae `Fuse.3dshapes/Fuse_Littelfuse-NANO2-451_453.step`; hay un modelo propio en `hardware/libraries/3d/` (SolidCraft, `fuentes-solidcraft/gen.py`) y la huella `esp-riego:Fuse_Littelfuse-NANO2-451_453`.
- La huella oficial `Texas_HTSOP-8-1EP…` viene del DRV8870 y no coincide con el land pattern DDA0008B de TI (pads 2,2 × 0,5 frente a 1,55 × 0,6).
- Banco de pruebas de render: placa mínima en el scratchpad con `(footprint "esp-riego:…")` en línea y rutas 3D absolutas; `kicad-cli pcb render --side top`. La guardia exige rutas literales en `mkdir`.
