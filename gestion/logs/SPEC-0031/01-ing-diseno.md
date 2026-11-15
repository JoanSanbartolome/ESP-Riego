---
spec: SPEC-0031
agente: ing-diseno
n: 01
fecha: 2026-11-15
estado: completado
---

# SPEC-0031 · 01 · ing-diseno

## Hecho

- `docs/diseno/conectores.md` (nuevo): solo §1, la lectura de los 6 pulsadores. Tiene tres opciones (A, escalera en serie en GPIO10; B, PCA9554 en el bus de la placa con INT en GPIO39; C, mixta) y, por opción, piezas con LCSC, tipo, stock, coste a 5 y 10 uds con el cargo Extended, dos pulsaciones a la vez, ESPHome y pines libres. Termina con la recomendación (A).

## Decisiones y desviaciones

- Escalera en **serie**, no en paralelo: con dos pulsadores apretados se lee uno de ellos y nunca un tercer canal (§1.2).
- A, a 6 dB (ATTEN2): el nivel más alto (1,50 V en el peor caso) queda dentro de los 0–1,6 V calibrados (S tabla 5-6, p. 66).
- B, con el PCA9554 de TI como principal, porque es el único con el *pull-up* de 100 kΩ comprobado en su datasheet (SCPS128D p. 15) y el *chip* probado en ESPHome. El de NXP (C17230) es más barato, pero su datasheet no se ha podido bajar (nxp.com).
- B pide el bus de la placa a 100 kHz: t_r = 0,28 µs con ≈ 70 pF, en el límite de 400 kHz (§1.3).
- No se tocan `mcu.md`, las hojas ni las referencias (lo pide la orden del paso 1).

## Verificación

- No se ha tocado ningún proyecto KiCad ni el MCP: `verificar.py` no aplica.
- Peor caso de la escalera calculado con un script de la carpeta temporal (`s31_escalera.py`, `s31_niveles.py`): huecos de ≥ 173 mV, umbrales a ≥ 86 mV.
- Precios y stock con `jlc.py` (2026-11-15) a 5, 10, 30 y 60 uds. Las opciones de ESPHome, de su documentación 2026.10.2 (`pca9554`, `pcf8574`, `mcp230xx`, `tca9555`, `xl9535`).

## Para validación

- Supuestos de la escalera:
  - V_DD de 3,17 a 3,39 V;
  - ± 1,5 % por resistencia (tolerancia más TCR de 100 ppm/K en 50 K, que no he comprobado en la ficha de UNI-ROYAL);
  - ± 10 mV del ADC.
- Lectura de reposo a 6 dB con 3,3 V en el pin: se supone ≥ 1,6 V (ADC saturado). Se comprueba en el prototipo.
- B: C_bus de ≈ 70 pF estimado (≈ 10 pF del PCA9554 y ≈ 10 pF de pista), sin dato de layout.

## Pendiente

1. Usuario (DEC-0013): elegir A, B (o B') o C. Recomendación: A.
2. Si elige B': el paso 3 consigue el datasheet de NXP PCA9554PW,118 y confirma el *pull-up* y el pinout.
