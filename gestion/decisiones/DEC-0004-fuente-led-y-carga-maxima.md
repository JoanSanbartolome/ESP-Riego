---
id: DEC-0004
titulo: Fuente LED de 24 V y 5 A como dato de entrada, y carga máxima por canal sin protección propia
fecha: 2026-11-05
estado: aceptada
decide: usuario
specs: [SPEC-0011]
requisitos: [ALI-04, ALI-09, ALI-12, ALI-13, REL-03, REL-05, REL-08, REL-10, FAB-01, FAB-09]
---

# DEC-0004 · Fuente LED de 24 V y 5 A, y carga máxima por canal

## Contexto

VAL-0007-01 dejó dos observaciones M en los requisitos v0.3:

- **01:** la ventana del limitador común (ALI-13) no está cerrada. Depende de la corriente a la que actúa la protección de la fuente, y ningún requisito la fija.
- **02:** una sobrecarga de un solo canal entre 1 A y el umbral del limitador no la corta ningún hardware. El BTT6050 limita a partir de 38 A y la pista de la clase `Salidas` estaba pensada para 1 A.

## Lo que decide el usuario

| # | Decisión | Requisitos afectados |
|---|---|---|
| 1 | **Fuente:** la que usa el usuario, una fuente de 24 V DC y 5 A para tiras LED, sin más datos. El coordinador asume los parámetros que hagan falta, sin complicar el circuito por ello. | ALI-04, ALI-09, ALI-12, ALI-13 |
| 2 | **Sin protección de sobrecarga por canal.** La carga máxima de cada canal es un parámetro de la placa (limitación por características), y el circuito se dimensiona correctamente para ella. | REL-05, REL-08, FAB-01 |

## Interpretación del coordinador

- **Fuente supuesta:** una fuente LED típica de 24 V y 5 A (120 W), como la serie Mean Well LRS-120-24:
  - salida ajustable ±10 % (21,6–28,8 V);
  - protección de sobrecarga del 105–150 % (5,25–7,5 A), en modo hipo con rearme automático;
  - protección de sobretensión (OVP) de 28,8–33,6 V.
  
  Si la fuente real es otra, solo cambian las cifras de esta lista y la banda del limitador.
- **Consumo de la lógica:** ≤ 0,25 A en la entrada, con el ESP32-S3 en ráfaga de Wi-Fi, los sensores, los LED y el 5 V de la expansión (≈ 4,5 W a 18 V).
- **Total de las salidas (ALI-12): 3,5 A**, en lugar de 4 A.
  - Cubre el máximo instalado: 6 canales con dos válvulas cada uno (6 × 0,56 A = 3,36 A).
  - Abre la banda del limitador lo bastante para que sirva una pieza normal, sin una tolerancia de corriente ajustada.
- **Banda del limitador (ALI-13): 3,5–4,9 A**, con la tolerancia de la pieza incluida, lo que equivale a 4,2 A ± 16 %.
  - No actúa con los 3,5 A de las salidas.
  - Con la lógica, 4,9 + 0,25 = 5,15 A, por debajo de los 5,25 A a los que puede empezar a actuar la fuente.
- **TVS (ALI-04): se mantiene la SMBJ33A.**
  - Su tensión de ruptura mínima, 36,7 V, está por encima de la OVP máxima supuesta (33,6 V).
  - El limitador y el resto del nodo siguen en ≥ 60 V (ALI-05).
- **Carga máxima por canal (REL-05): 1 A**, como parámetro de la placa. Figura en la serigrafía (FAB-09) y en la documentación.
- **Dimensionamiento correcto (REL-05, FAB-03):** una sobrecarga de un canal por encima de 1 A no se corta hasta que actúa el limitador. Por eso, la pista y el borne de cada salida soportan sin daño la corriente máxima de la banda (4,9 A) con ΔT ≤ 40 °C, lo que da ≈ 1,2 mm con 1 oz en capa externa (IPC-2221).
  - Con la corriente nominal se mantiene el criterio de ΔT ≤ 10 °C.
  - El *high-side* soporta esa corriente con su limitación térmica (apagado y rearme).
  - No se añade ningún componente. El firmware puede avisar en Home Assistant de una corriente por encima de 1 A con la IS (REL-10), sin cortar.
- **Avisos de VIN (ALI-09):** pasan a 17 V y 31 V, para que los puntos de prueba de §6 queden a los dos lados de cada umbral y dentro de la ventana en la que la placa funciona.
- **Carga abierta en OFF (REL-10) frente al corte general (ALI-13):**
  - el firmware habilita el bus de las salidas mientras algún canal riega;
  - también lo habilita durante la comprobación de carga abierta, con los canales apagados.

## Alternativas consideradas

- **Pistas solo para 1 A** (v0.3): una sobrecarga de 2–4 A calienta la pista entre ≈ 50 y ≈ 230 °C. Se descarta porque el dimensionamiento correcto no cuesta componentes.
- **Corte por firmware con IS:** depende del firmware y del error de ± 25 % de la IS. El usuario no quiere protección por canal.
- **PTC o fusible por canal:** añade 6 piezas. El usuario no quiere protección por canal.
- **Mantener 4 A de total:** obliga a una banda de 4,0–4,9 A (± 10 %) y a un limitador con una tolerancia de corriente más ajustada, sin ninguna ventaja para la carga instalada.

## Consecuencias

- `docs/02-especificaciones-v2.md` pasa a la v0.4 (SPEC-0011). Se redefinen ALI-04, ALI-09, ALI-12, ALI-13, REL-03, REL-05, REL-08, REL-10 y FAB-01, y se actualizan §6, §8 y §10.
- **Layout:** la clase `Salidas` pasa de ≈ 0,3 mm a ≈ 1,2 mm. Hay que tenerlo en cuenta en el presupuesto de los bordes (FAB-07).
- **Coste:** sin cambios. No se añaden componentes.
- **Prueba de sobrecarga del conjunto (§6):** se hace con la fuente LED, por encima de la banda.
