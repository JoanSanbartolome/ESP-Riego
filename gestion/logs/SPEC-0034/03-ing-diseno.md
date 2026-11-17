---
spec: SPEC-0034
agente: ing-diseno
n: 03
fecha: 2026-11-17
estado: completado
---

# SPEC-0034 · 03 · ing-diseno

Corrección de VAL-0034-01. Solo cambia `docs/diseno/salidas.md`; `hardware/v2` queda igual.

## Hecho

- **-01 (M):** en §5.3 y §13.9 sale la «conmutación térmica»: el BTT se enclava tras el apagado térmico y solo lo rearma una subida de IN (BTT6050 §6.5.2, p. 21; §7.3.5, p. 29). Da un impulso (≤ 56 A, ≤ 62,5 µs, ≤ 0,098 A²s) por cada subida de IN y por cada rearranque por subtensión si la fuente hunde el bus por debajo de V_S(UV) = 3–4,1 V (§6.2, p. 17; Tabla 4, p. 8). La prueba de prototipo de §13.9 cuenta esos impulsos, mira si el bus baja de V_S(UV) y mide la temperatura del diodo.
- **-02:** en la fila «Suma» de §0, «puede saltar desde ≈ 3,0 A». En §12, mensaje «suma de las salidas cerca o por encima de 3,5 A», el adelanto por I_GND y R_OL, y como opción calibrar la ganancia de IMON por placa.
- **-03:** en «Tipo de carga» de §0, consecuencia de conectar 230 V AC o una fuente externa: en el semiciclo negativo, corto por D12–D17; en el positivo, corriente inversa por el BTT (sin protecciones, §5.4, p. 14; el informe citaba §5.5) y más de 65 V (V_S(LD), Tabla 3, p. 6). Se destruyen el diodo y el BTT, y la tensión puede llegar al bus.
- **-04:** Z_th del M7 a 50 ms, 11–12 K/W (ΔT_J ≈ 13 K). R_θJA 75 K/W, con pads de 2 × 2″ (nota 2). La cota con τ → ∞ se quita: solo se daría con PWM, que está fuera de uso. Fuga típica ≈ 0,2 µA a 75 °C y 1–1,5 µA a 100 °C (Fig. 2). Aislamiento con la fuga típica: 163 / 242 / 314 kΩ (§3.3, §5.4). La cota de 50 µA y el límite de 400 kΩ no cambian.
- **-05:** «el corto lo prueba `docs/02` §6 con ≥ 10 m»; coste de §9 con `M7.md` del 2026-11-17 y ≈ 8,1 $ con 10 placas; carga baja, «por debajo de 30 mA».

## Decisiones y desviaciones

- **-06:** los 49 `(thickness 0.15)` añadidos en propiedades ocultas (F.Fab) de huellas que no son D12–D17 los añadió pcbnew al guardar, cuando `sincronizar.py` reescribió la PCB en el parte 01. No tienen efecto eléctrico ni de fabricación, y no se revierten.

## Verificación

- Grep en `salidas.md`: no queda «conmuta por temperatura», «31 mA», «143 °C» ni «corto probado». El archivo sigue en CRLF.
- No he tocado `hardware/v2`, así que no hace falta `verificar.py`; el resultado es el de VAL-0034-01 (ERC 0, DRC 0, paridad 0).
