---
name: project-salidas-d8
description: D8 cerrada (DEC-0003/0004) — salidas high-side BTT6050 a 24 V DC con limitador común 3,5–4,9 A; valores de válvula y piezas descartadas del estudio SPEC-0005
metadata:
  type: project
---

**Estado vigente (2026-11-05), sustituye a la nota anterior con válvulas de 24 V AC y ≈ 4 A:**

- DEC-0003: las salidas son *high-side* inteligentes BTT6050-1ERA (C534868), con BTT6030-2ERA (C534865) como segunda fuente y BSP752R (C112644) de reserva de otro fabricante. Todo alimentado desde 24 V DC a través de un limitador común del bus de salidas. Sin relé, opto ni contacto libre (D2 cerrada).
- DEC-0004: fuente LED de 24 V y 5 A en su ajuste de fábrica. Carga instalada máxima de 3,5 A (12 válvulas de 0,25 A). Banda del limitador de 3,5–4,9 A con tolerancia (≈ 4,2 A ± 16 %). 1 A por canal como parámetro, sin protección por canal; pistas, bornes y retornos para 4,9 A. `Power_In` y fusible para 5,1 A.
- Las válvulas instaladas son de 24 V DC, ≈ 0,2 A (máximo 2 por canal).

**Why:** el usuario cambió los datos de partida varias veces durante SPEC-0005/0007/0011; lo vigente está en `docs/02-especificaciones-v2.md` v0.4 y en DEC-0003/0004.

**How to apply:** antes de diseñar salidas, limitador o alimentación, compruébalo con `docs/02` y `gestion/decisiones/`, porque estas cifras pueden haber cambiado otra vez.

Valores de diseño de las válvulas (estudio SPEC-0005):
- 24 V DC: 0,25 A (0,28 A en frío). La Bermad S-390-T 24 V DC da 0,18 A con 156 Ω.
- Inductancia: se mide o se toma del fabricante antes de cerrar el esquema (REL-03).

Piezas descartadas, y por qué:
- BTS4140N: solo 0,2 A y entrada activa baja.
- VN7 y TPS1HC100: son de 12 V.
- NCV8460A: V_IH de 3,25 V.
- VN5 y BSP762T: 41 V, menos que los 53,3 V de la SMBJ33A.
- BTS428L2: V_IN(T+) hasta 3,2 V (> 2,64 V del ESP32-S3) y protección de corto solo hasta V_bb = 24 V; además 2,42 $ (VAL-0005-01-02).
- BTT6030-2ERA (segunda fuente): 4 A por canal con los dos activos y k_ILIS 2240 (no 1500); con 5 placas se compran 15 chips, al tramo de 10 uds.
- AO3400A y SS14 en el bus: 30/40 V, menos que la Vc de 53 V.
- Z0109MN, IPS160HFTR, ISP752R y LT925: sin stock.
- G3VM-61HR: sin stock.

LED de canal: excitarlo con un transistor desde 3,3 V, no desde el GPIO (el ESP32-S3 no garantiza V_OH con carga). No debe enmascarar la carga abierta (REL-10).

Relacionado: [[reference-fuentes-piezas]], [[reference-trucos-esquema]]
