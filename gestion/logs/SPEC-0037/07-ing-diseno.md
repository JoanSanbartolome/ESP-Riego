---
spec: SPEC-0037
agente: ing-diseno
n: 07
fecha: 2026-11-20
estado: completado
---

# SPEC-0037 · 07 · ing-diseno (paso 6: estudio de coste y J10 horizontal)

## Hecho

- `docs/diseno/estudio-coste.md`: coste por bloque, montaje (E1/E2/S2), Q1, rieles, fallos abiertos y resumen por ahorro. BOM con precio y tipo del 2026-11-20 en `docs/diseno/estudio-coste-bom.csv`.
- J10: XFCN BH254R-10P (C492448, Extended, 10 286 uds; no hay IDC en ángulo recto básicas ni preferentes). Huella oficial `Connector_IDC:IDC-Header_2x05_P2.54mm_Horizontal`, sin cambios. Ficha `hardware/componentes/BH254R-10P.md` (cotas frente al dibujo) y `datasheets/BH254R-10P.pdf`.
- `colocacion-reglas.csv`: B04 `ras` inf 0,5; B07 `hacia` +x; F03 sin J10; R01 con J10; notas de P05, E08 y L01 (8,9 mm: la cifra no cambia).
- `docs/diseno/colocacion-b4.csv` (100 × 100) y `colocacion-b4.png`: 10 iteraciones en texto desde b3 (J10 cambiado en una copia con `sincronizar.py`), una imagen al final. Ida y vuelta con `colocar.py`: mismos PUNTOS.
- `colocacion.py` sin cambios. Parche de la batería (B04/B07 rompían `Colocacion` y `ColocacionPaso5`, que evalúan con la huella vertical de `hardware/v2`; clase nueva `ColocacionPaso6`): `C:\Users\josan\AppData\Local\Temp\claude\2c54f79e79dd3002\ad4da10c-a29b-4ee4-bc81-7ee404e64af6\scratchpad\p6\prueba\test_kicad.patch` (archivo entero en `…\p6\prueba\test_kicad.py`; `patch --binary`, CRLF). Con el parche, `Colocacion`, `ColocacionPaso5` y `ColocacionPaso6`: 11/11.

## evaluar (b4)

PUNTOS 6251 = 0 obligatorias + 58 objetivos (61 en b3) + 4507/10 de longitud. Placa 100 × 100, 2 $/5 uds; rieles (inf: J10 0,1 · izq: J2 0,2, U5 0,2): panel 110 × 110 sin tarifa. Solapes 0, fuera 0, zona de U5 dentro 298 mm². Serigrafía: alto de huella 1 (JP1). Cobre: U2 319/315, U10 330/330, U1 331/330, Q1 276/275, U11 332, U12 332. Sin rutar 4097 mm.

## Decisiones y desviaciones

- E02 resuelto: D2 entre U1 y Q1, a 0,1 mm del patio de Q1 y fuera del anillo de U1; D1 y R1 junto a la puerta de Q1 (W03). E05 se queda con C3, R3, R5 y JP1 lejos: el anillo de U1 solo admite 68 mm² ocupados (Q13 manda).
- C46 (O13) sin solución en 100 × 100: cualquier sitio a ≤ 10 mm de U10–U12 cae en su anillo. Propuesta en el estudio §8.2.
- J10 horizontal no libera sitio: su patio tiene 15,1 mm de fondo (9,9 el vertical + 2,5 al borde).
- Q1: U1 solo rechaza la polaridad inversa con un N-MOSFET externo en B_GATE (SLVSE94G §8.3.5, pp. 20-21). Recomendación: mantener Q1 (ALI-03 sin cambios). Quitarlo ganaría ≈ 370 mm² (3,7 %).

## Para validación

- U4: TLV1117LV33DCYR de TI con stock 0 (C15578); la alternativa JSMSEMI C48937499 necesita revisar su ficha.
- Equivalencia de las preferidas de P1 (C19077586, C19077412, C7420364) y de ZHOURI C5156674 para J10.
- Precio de la PCB de 50 uds: 15 $ estimados (JLCPCB no publica tarifa).

## Pendiente

- Usuario: decisiones del estudio §9 (P2 THT a mano, P3, P5, O13, margen +10/+5, rieles: preguntar a JLCPCB, U1 RGET).
- Coordinador: aplicar el parche de la batería; checklist l. 44 y l. 46 (§8.7); reescritura de objetivos (§8.3).
- Otra spec: J10 BH254R-10P en `hardware/v2` (DEC-0017), textos de JP1, zona de U5 de un solo lado (Fig. 26, D5), mínimo de 0,3 mm en `ras`.

## Corrección VAL-0037-01 (2026-11-23)

- Estudio: P4 pasa a «LDO a elegir en SPEC-0038», con los requisitos y los candidatos C150716 y C52146079 (-01). P3 sin C8 (cita de la p. 20; la línea C513710 se queda, ahorro de 0,18 / 0,05 $) (-02). P5 retirada (-03). §0 y §9: P1 + P2 + P3 → 42,02 $/placa con 5 uds y 24,00 $ con 50. §8.10: cómo reproducir b4 y el criterio de SPEC-0038 (-04).
- Recuento de reglas: el parte 06 dice ahora 116 reglas + 4 clases (-06). Con E09 son 117 + 4 clases. Ni este parte ni el README citaban el 119.
- `BH254R-10P.md`: codo a ≈ 6,0 mm y pinout marcado como inferido; nota de P05 y estudio §5 corregidos (-08).
- README: la clase `ColocacionPaso6` (-10).
- Regla E09 (`lejos` R14 R15 de U2 L1 U7-U12, ≥ 5 mm, objetivo, `alimentacion.md` §8) (-11). `evaluar` de b4 (copia con J10 horizontal): 117 reglas, PUNTOS 6251, 0 obligatorias y 58 objetivos; E09 se cumple.
- `hardware/v2` sin cambios; la batería no cambia (ninguna prueba cuenta las reglas).
