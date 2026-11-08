---
spec: SPEC-0022
agente: ing-esquematicos
n: 05
fecha: 2026-11-07
estado: completado
---

# SPEC-0022 · 05 · ing-esquematicos

## Orden recibida

SPEC-0022 · rama spec/SPEC-0022-hoja-mcu (activa en C:\Users\josan\proyectos\KICAD_mcp) · Lee: gestion/informes/VAL-0022-01.md (hallazgos 01, 02 y 03) + docs/diseno/mcu.md (§7, §11) + hardware/v2/README.md + gestion/logs/SPEC-0022/02-ing-layout.md (salida de verificar.py tras sincronizar) · Haz: solo texto, sin KiCad: (01) en mcu.md §11 sustituye la frase falsa «sus datos están en bloque-alimentacion.md (D4)» por una referencia a la nueva ficha hardware/componentes/KT-0603R.md (la está creando jr-conformidad en paralelo; no la crees tú) e indica la polaridad (② del datasheet = cátodo = pad 1 de LED_0603); (02) en §7 añade la I_mín de D5 en el peor caso (VDD mínimo, V_F máx., R23 +1 %) ≈ 0,12 mA y comprueba que sigue visible o anótalo; (03) actualiza hardware/v2/README.md con el estado tras el paso 2 (paridad 0, 172 sin conectar por no rutar, 21 huellas fuera del contorno). No toques otros archivos. · Entrega: mcu.md + README.md + log gestion/logs/SPEC-0022/05-ing-esquematicos.md. Brevedad: en tu respuesta solo el contrato de salida; log telegráfico.

- Rama `spec/SPEC-0022-hoja-mcu` ✔. Sin `.lck`. MCP no usado.

## Contexto consultado

- `gestion/informes/VAL-0022-01.md` (-01, -02, -03; recálculo de §7).
- `docs/diseno/mcu.md` §1 (VDD 3,211–3,389 V), §7, §11, Anexo A.
- `gestion/logs/SPEC-0022/02-ing-layout.md` (Verificación, Notas).
- Datos del KT-0603R tomados de VAL-0022-01 (PDF de LCSC C2286, pp. 2–5); no reabierto.

## Acciones

- `docs/diseno/mcu.md`:
  - §7: I_mín peor caso = (0,8 × 3,211 − 2,45)/1,01 k ≈ 0,12 mA; cota realista ≈ 0,66 mA (V_F 1,90 V, curva p. 5); viñeta de visibilidad.
  - §11: frase falsa sustituida por referencia a `hardware/componentes/KT-0603R.md` + polaridad (② = cátodo = pad 1; ① = ánodo = pad 2; p. 2; no aplica la regla de la «T»).
  - Anexo A, fila KT-0603YG: misma frase falsa («ficha en `bloque-alimentacion.md`») → ficha KT-0603R. Mismo hallazgo -01, mismo archivo.
  - Cabecera: línea «Rev. VAL-0022-01».
- `hardware/v2/README.md`: §PCB (80 huellas; H1–H4 dentro; 55 de Alimentacion y 21 de MCU fuera, con coordenadas) y párrafo de verificación (ERC 0, DRC 0, 172 sin conectar, paridad 0).

## Decisiones y justificación

- Visibilidad a 0,12 mA no garantizada (I_V solo a 20 mA, p. 3); MCU-07 no fija brillo → se acepta. Remedio sin cambiar huella: R23 = 470 Ω (I_máx (3,389 − 1,6)/470 = 3,8 mA ≪ 25 mA; P_R 6,8 mW). Anotado en §7, no aplicado.

## Verificación

- Sin cambios en KiCad: `verificar.py` no ejecutado (orden «sin KiCad»). Último estado (log 02): ERC 0, DRC 0 (172 sin conectar), paridad 0.
- Checklist `esquema.md`: solo afectan los ítems de documentación de cálculos (§7 con fórmula, fuente y margen: cumple) y campos/polaridad de piezas (polaridad KT-0603R documentada: cumple, pendiente de la ficha). Resto: no aplica (sin cambios en el esquema).

## Pendiente

- **jr-conformidad:** `hardware/componentes/KT-0603R.md` aún no existe (2026-11-07); `mcu.md` §11 y Anexo A ya la citan.
- **Coordinador:** VAL-0022-01-04 (constancia de la conformidad del usuario con D5 rojo) sigue abierto; no es de mi zona.

## Notas para el siguiente agente

- Spec de Salidas (D6–D11, KT-0603R): pad 1 = cátodo = ② del datasheet.
