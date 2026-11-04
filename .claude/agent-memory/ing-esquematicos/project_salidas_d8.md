---
name: project-salidas-d8
description: Conclusiones del estudio de salidas (SPEC-0005) con la entrada única de 24 V DC, valores de diseño de las válvulas y piezas descartadas
metadata:
  type: project
---

El estudio de SPEC-0005 (`docs/diseno/estudio-salidas.md`, 2026-11-04) se rehízo dos veces durante el encargo. Contexto final:

- La placa se alimenta **solo con 24 V DC** (fuente de 5 A, 18–30 V, TVS SMBJ33A).
- 6 salidas a la vez, con ≈ 4 A en total.
- Las válvulas instaladas son de 24 V AC: solo se pueden usar con contacto libre y su propio transformador (≤ 32 V AC, 45,3 V de pico) o cambiándolas a DC o *latch*.

Propuesta para D8: relé subminiatura G5NB-1A-E / HF46F (cubre AC con contacto libre y DC alimentada, canal a canal). Alternativa: 4c (2× IRLML0100 + VOM1271T). Si se abandona la AC: BTT6050-1ERA (PROFET+ 24 V, con medida de corriente IS). Lo decide el usuario: antes de diseñar el bloque de salidas, comprobar en `docs/02` y `gestion/decisiones/` qué se eligió.

**Why:** el usuario quiere salidas que no dependan del tipo de válvula (DEC-0002 §6), y cambia los datos de entrada sobre la marcha.

**How to apply:**
- Valores de diseño:
  - válvula AC: 0,23 A de mantenimiento y 0,41 A de *inrush*;
  - válvula de 24 V DC: 0,25 A (0,28 A en frío; Bermad S-390-T 24 V DC = 0,18 A y 156 Ω);
  - *latch*: 6–9 V, ≈ 2 A de impulso (Hunter 458200 de 4,8 Ω; Rain Bird TBOS de 4,5 Ω).
- Una válvula de AC en DC sin PWM se quema.
- El triac no se apaga en DC.
- Con una fuente de 5 A, un corto en campo hace caer la lógica si no hay protección por canal.
- *Low-side*: un corto del cable a tierra abre la válvula. Preferir *high-side*.
- LED de control (H5): excitarlo desde 3,3 V con una R fija y un AO3400A, no desde el GPIO, porque el ESP32-S3 no garantiza V_OH con carga.
- Piezas descartadas:
  - BTS4140N (0,2 A);
  - Z0109MN (57 en stock);
  - IPS160HFTR (1);
  - ISP752R (89);
  - LT925 de 100 V (3);
  - G3VM-61HR (sin stock);
  - AO3400A y SS14 en el bus (30/40 V < 53 V de la SMBJ33A).
- AQV252G (60 V): sin margen de TVS con 45,3 V de pico.

**Adenda del 2026-11-04 (§11 del estudio):** las válvulas instaladas son en realidad de 24 V DC (≈ 0,2 A) y el usuario eligió *high-side*. Propuesta: BTT6050-1ERA (C534868) como principal, BTT6030-2ERA (C534865) como segunda fuente y BSP752R (C112644) como reserva de otro fabricante.
- Es el chip válido más barato en LCSC: los más baratos son de 12 V (VN7, TPS1HC100), tienen la entrada activa baja (BTS4140N) o una V_IH de 3,25 V (NCV8460A).
- Los VN5 y el BSP762T se quedan en 41 V, por debajo de los 53,3 V de la SMBJ33A.
- El BTS428L2 cuesta 2,42 $.

Relacionado: [[reference-fuentes-piezas]]
