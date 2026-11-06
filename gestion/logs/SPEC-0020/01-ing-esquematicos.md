---
spec: SPEC-0020
agente: ing-esquematicos
n: 01
fecha: 2026-11-05
estado: completado
---

# SPEC-0020 · 01 · ing-esquematicos

## Orden recibida

SPEC-0020 · rama spec/SPEC-0020-calculos-mcu, en el worktree C:\Users\josan\proyectos\KICAD_mcp-SPEC-0020 (trabaja SOLO dentro de esa carpeta; todas las rutas de la spec son relativas a ella) · Lee: gestion/specs/SPEC-0020-calculos-mcu.md + las entradas que lista · Haz: todo el alcance · Entrega: docs/diseno/mcu.md + log gestion/logs/SPEC-0020/01-ing-esquematicos.md. NO uses el MCP de KiCad ni kicad-cli (otra spec lo tiene en uso); lee los .kicad_sch como texto si te hace falta. Brevedad: solo contrato de salida; log telegráfico.

## Contexto consultado

- Spec SPEC-0020; `docs/02` v0.4; `docs/diseno/alimentacion.md` (§3.8–3.13, §4, §6); `docs/diseno/estudio-salidas.md` (S7, §1.6, §2.5, §11).
- Fichas: ESP32-S3-WROOM-1, USBLC6-2SC6, TYPE-C-31-M-12, SHT4x y BTT6050-1ERA.
- Checklists `requisitos.md` v3 y `esquema.md` v5. DEC-0005.
- Datasheets:
  - WROOM-1 v1.8 (local): pp. 3, 10-16, 27-28, 41, 45-46;
  - ESP32-S3 v2.2: tablas 2-1/2-2 (pp. 16-19), §4.2.2.1 (p. 59), tabla 5-4 (p. 65);
  - HDG *release master*: pp. 5-9, 13-19, 28-31;
  - BTT6050: §6.4 (p. 19), §6.5.2 (p. 21), tabla 8 (p. 24 del PDF), tabla 10 (p. 34);
  - TLV1117LV SBVS160C: p. 5, Fig. 6-16/6-18 (p. 8), §7.3.1-7.3.2;
  - LMR36520 SNVSBF0C: p. 7 (t_SS); TPS2116 SLVSFG1A: §8.2.2 (p. 15).
- Stock y precio: JSON de LCSC del 2026-11-05.
- Librerías oficiales de KiCad 10 (solo lectura): símbolos, huellas, *keepout* de `ESP32-S3-WROOM-1.kicad_mod` y carpetas de 3D.
- `hardware/v2/mcu.kicad_sch`: solo texto pendiente, sin piezas que aprovechar.

## Acciones

- Selección y cálculos de todo el alcance → borrador `docs/diseno/mcu.md`.
- Simulación de la red RC de EN frente a la rampa de 3,3 V (script en el *scratchpad*, `s20_en.py`).
- **No se pudo escribir en el worktree:** la guardia bloquea `docs/diseno/mcu.md` del worktree («está fuera del repositorio»). Los entregables quedan como borradores en el *scratchpad*, con la misma ruta relativa:
  - `…/scratchpad/s20_entrega/docs/diseno/mcu.md`
  - `…/scratchpad/s20_entrega/gestion/logs/SPEC-0020/01-ing-esquematicos.md`

## Decisiones y justificación

- **N8:** de 85 °C frente a 65 °C de las R8/R16V (WROOM-1 p. 3), con GPIO35–37 libres. Alternativa: N16.
- **DEN común a los 6 canales** (propuesta: desviación de «DEN por canal» de la spec):
  - con IS por canal en ADC1, el DEN por canal no aporta diagnóstico;
  - libera 5 GPIO; con DEN por canal no queda ningún pin libre (variante B, §9.3).
- **Pines excluidos para salidas:** 18 (pulso alto), 39 (WPU), 40 (alto en la descarga OTG), 43 y 44. GPIO40 se usa para el LED.
- **Dos buses I²C** (placa y expansión).
- **EN de 10 kΩ / 1 µF:** EN ≤ 0,13·VDD cuando VDD llega a 3,0 V en el peor caso real. Sin supervisor.
- **TLV1117LV:** cumple; no se cambia.
- **REL-04 con OTA y `esp_restart()`:** se cubre en el firmware (`on_begin`, `on_shutdown`). Es una interpretación del autor; se prueba en el prototipo.

## Verificación

- `verificar.py`: **no ejecutado**. Usa `kicad-cli` y la orden lo prohíbe. Sin cambios en KiCad.
- MCP: no usado, así que no hay `save_project` ni `close_project`.

Repaso de `gestion/checklists/esquema.md` v5:

- **Estructura, campos de cada símbolo, ERC:** no aplica (sin hoja; SPEC-0022). Los campos están preparados en §11.
- **Cálculos:**
  - fórmula, datos con fuente y margen: cumple (§5, §7, §8, §10.2 y §11);
  - recálculo del revisor: pendiente (validación);
  - tensiones nominales frente a Vc: no aplica (bloque de 3,3/5 V; VBUS lo protege U6);
  - *derating* de cerámicos: cumple (C24, C23; estimado, §8.1, §5.1);
  - E_AS y *hold-up*: no aplican;
  - disipación a 60 °C: cumple (TLV, §8.3).
- **Microcontrolador:**
  - pines de arranque sin cargas: cumple (§5.2, §9);
  - analógicas solo en ADC1: cumple (§9);
  - GPIO19/20 solo para el USB; GPIO35–37 en uso porque no hay PSRAM octal: cumple;
  - red RC en EN y pulsadores: cumple (§5);
  - desacoplo según Espressif: cumple (§8.1);
  - YAML: pendiente (no hay hoja; Anexo B).
- **Salidas (lo que toca a este bloque):** desactivadas en el reset y el flasheo: cumple en hardware (§10); OTA, por firmware. IS a ADC1: cumple en pines; la cota ≤ 3,1 V es del bloque de salidas.
- **Interfaces:** pull-ups del I²C de la placa: cumple. Conector de expansión y ESD: pendiente de SPEC-0006.
- **Entregables para layout:** tabla de §12: cumple.
- **Requisitos v3, estudios:** coste con el tramo real: cumple; descartes con su parámetro: cumple (R8, KT-0603G, GPIO excluidos).

## Pendiente

- **Coordinador:** (cerrado) entregables copiados al worktree; DEN común fijado por DEC-0007.
- **jr-conformidad (SPEC-0021):**
  - modelo 3D de `SW_Push_1P1T_XKB_TS-1187A` (falta en KiCad 10.0);
  - fichas del TS-1187A-B-A-B, el KT-0603YG y la tira B-2100S04P-A110;
  - actualizar la ficha del ESP32-S3-WROOM-1 (N8);
  - tipo Basic/Extended de todas las piezas.
- **SPEC-0018:** (cerrado) C15849 ya tiene stock; C10 pasó a C28323.
- **SPEC-0006:** pines y pasivos de EXP-02 (provisionales en §9.2).
- **Bloque de salidas:** R_PD de 100 kΩ en IN1–6 y OUT_DEN (§10.2).

## Notas para el siguiente agente

- La tabla de GPIO de §9.2 es fija. Las etiquetas jerárquicas están en el Anexo C. Las referencias siguen a las de alimentación (U5, U6, J2, J3, SW1, SW2, D5, R16–R25, C23–C26 (sin chocar con alimentación: máx. C22, R15, D4)).
- C23 = 1 µF de C106248 (EN); C24 22 µF, C25 100 nF (C14663, DEC-0007), C26 VBUS.
