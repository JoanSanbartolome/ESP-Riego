---
id: DEC-0004
titulo: Fuente LED de 24 V y 5 A como dato de entrada, y carga máxima por canal sin protección propia
fecha: 2026-11-05
estado: aceptada
decide: usuario
specs: [SPEC-0011]
requisitos: [ALI-01, ALI-04, ALI-06, ALI-09, ALI-12, ALI-13, REL-03, REL-05, REL-08, REL-10, FAB-01, FAB-03, FAB-09]
---

# DEC-0004 · Fuente LED de 24 V y 5 A, y carga máxima por canal

## Contexto

VAL-0007-01 dejó dos observaciones M en los requisitos v0.3:

- **01:** la ventana del limitador común (ALI-13) no está cerrada. Depende de la corriente a la que actúa la protección de la fuente, y ningún requisito la fija.
- **02:** una sobrecarga de un solo canal entre 1 A y el umbral del limitador no la corta ningún hardware. El BTT6050 limita a partir de 38 A y la pista de la clase `Salidas` estaba pensada para 1 A.

La primera redacción de la v0.4 (VAL-0011-01, RECHAZADO) solo cerraba la banda a 24 V. VAL-0011-02 corrigió además una doble corrección por frío en la carga instalada. La protección de sobrecarga de una fuente LED va en porcentaje de la potencia: si se sube el ajuste hasta 28,8 V, actúa con menos corriente, y además la carga de las válvulas crece.

## Lo que decide el usuario

| # | Decisión | Requisitos afectados |
|---|---|---|
| 1 | **Fuente:** la que usa el usuario, una fuente de 24 V DC y 5 A para tiras LED, sin más datos. El coordinador asume los parámetros que hagan falta, sin complicar el circuito por ello. | ALI-01, ALI-04, ALI-09, ALI-12, ALI-13 |
| 2 | **Sin protección de sobrecarga por canal.** La carga máxima de cada canal es un parámetro de la placa (limitación por características), y el circuito se dimensiona correctamente para ella. | REL-05, REL-08, FAB-01, FAB-03 |

## Interpretación del coordinador

- **Fuente supuesta:** una fuente LED típica de 24 V y 5 A (120 W) de tensión constante, como la serie MEAN WELL LRS-120-24:
  - salida ajustable entre 21,6 y 28,8 V (−10 / +20 %);
  - protección de sobrecarga en porcentaje de la potencia, del 110 al 150 % según la hoja. Se supone un 105 %, que da margen;
  - protección de sobretensión (OVP) de 28,8 a 33,6 V.
- **Ajuste de la fuente (ALI-01):** se deja en su ajuste de fábrica de 24 V (± 2 %).
  - El total de las salidas y la banda del limitador se calculan con esa tensión.
  - Con 24,5 V, la protección de la fuente actúa como pronto a 126 W / 24,5 V = 5,14 A.
  - La placa sigue funcionando entre 18 y 30 V para cubrir la caída en el cable y la tolerancia, pero subir el ajuste de la fuente queda fuera de lo previsto.
- **Consumo de la lógica:** ≤ 4,8 W en la entrada (≤ 0,2 A a 24 V; con 22 V en el borne serían 0,22 A, y la ventana sigue cerrando). Incluye el ESP32-S3 con el Wi-Fi transmitiendo, los sensores, los LED y el 5 V de la expansión. Tiene prueba en §6.
- **Carga instalada máxima (ALI-12): 3,5 A.** Corresponde a 12 válvulas (dos por canal) de 0,25 A a 24 V y 20 °C (estudio de salidas), con dos correcciones que dan 3,47 A:
  - a 24,5 V, un 2 % más;
  - con la bobina a −10 °C, un 13 % más, porque el cobre tiene menos resistencia en frío. Los 0,28 A por válvula del estudio y de REL-05 ya son el valor en frío.
- **Banda del limitador (ALI-13): 3,5–4,9 A**, con la tolerancia de la pieza incluida (≈ 4,2 A ± 16 %).
  - No actúa con la carga instalada máxima.
  - Con la lógica, 4,9 + 0,2 = 5,1 A, por debajo de 5,14 A.
  - Se puede cumplir con piezas comunes, por ejemplo un eFuse de 60 V como el TPS2663 (± 7 %) o un controlador *hot-swap* como el LM5069. La pieza se elige en el esquema.
- **TVS (ALI-04): se mantiene la SMBJ33A.**
  - Su tensión de ruptura mínima, 36,7 V, está por encima de la OVP máxima supuesta (33,6 V).
  - El limitador y el resto del nodo siguen en ≥ 60 V (ALI-05).
- **Fusible y `Power_In` (ALI-12, FAB-03):** se dimensionan para la corriente máxima de entrada, 5,1 A continuos a 50 °C, sin actuar.
- **Carga máxima por canal (REL-05): 1 A**, como parámetro de la placa. Figura en la serigrafía (FAB-09) y en la documentación.
- **Dimensionamiento correcto (REL-05, FAB-03):** una sobrecarga de un canal por encima de 1 A no se corta hasta que actúa el limitador. Por eso, la pista, el borne y el retorno GND de cada salida soportan sin daño la corriente máxima de la banda (4,9 A) con ΔT ≤ 40 °C, lo que da ≈ 1,2 mm con 1 oz en capa externa (IPC-2221).
  - Con la carga máxima se mantiene el criterio de ΔT ≤ 10 °C.
  - A 4,9 A, el *high-side* (I_L(NOM) de 4,5 A) puede llegar a su apagado térmico. Si lo hace, se enclava sin dañarse hasta que su entrada vuelve a conmutar.
  - El firmware lo detecta, avisa y no lo reintenta en el mismo riego (REL-08).
  - No se añade ningún componente. El firmware puede avisar en Home Assistant de una corriente por encima de 1 A con la IS (REL-10), sin cortar.
- **Avisos de VIN (ALI-09):** 17 V y 31 V, con la medida a ± 3 %.
  - Las pruebas de §6 se hacen fuera de la banda de cada aviso: a 16 V (bajando desde 24 V) y 18 V, y a 29,5 V y 32,5 V.
  - La placa arranca en frío desde 17 V y, una vez en marcha, funciona hasta 15,5 V (ALI-06).
- **Carga abierta en OFF (REL-10) frente al corte general (ALI-13):** el firmware habilita el bus de las salidas mientras algún canal riega, y también durante la comprobación de carga abierta, con los canales apagados.
- **Expansión (SPEC-0006):** el bus limitado de la placa apenas tiene margen sobre su carga instalada.
  - Las salidas del módulo llevan su propio limitador o su propia alimentación.
  - Su consumo por el 5 V de la placa entra en los 0,2 A de la lógica.

## Alternativas consideradas

- **Pistas solo para 1 A** (v0.3): una sobrecarga de 2–4 A calienta la pista entre ≈ 50 y ≈ 230 °C. Se descarta porque el dimensionamiento correcto no cuesta componentes.
- **Corte por firmware con IS:** depende del firmware y del error de ± 25 % de la IS. El usuario no quiere protección por canal.
- **PTC o fusible por canal:** añade 6 piezas. El usuario no quiere protección por canal.
- **Permitir el ajuste de la fuente hasta 28,8 V:** a esa tensión la fuente protege desde 4,38 A, y 12 válvulas frías consumen ≈ 4,0 A, así que no cabe ninguna banda. Habría que cambiar de fuente o reducir la carga instalada.
- **Fuente LED de corriente constante** (p. ej. de la serie HLG con limitación al 95–108 %): no deja sitio a la banda. Se descarta, y la fase 2 comprueba que la fuente real es de tensión constante.

## Consecuencias

- `docs/02-especificaciones-v2.md` pasa a la v0.4 (SPEC-0011):
  - se redefinen ALI-01, ALI-04, ALI-06, ALI-09, ALI-12, ALI-13, REL-03, REL-05, REL-08, REL-10, FAB-01, FAB-03 y FAB-09;
  - se actualizan §2, §6, §7, §9 y §10.
- **Layout:**
  - la clase `Salidas` pasa de ≈ 0,3 mm a ≈ 1,2 mm, y lo mismo los retornos GND de las salidas;
  - hay que tenerlo en cuenta en el presupuesto de los bordes (FAB-07).
- **Coste:** sin cambios. No se añaden componentes.
- **Fase 2:** comprobar la etiqueta o el modelo de la fuente real antes de elegir el limitador.
