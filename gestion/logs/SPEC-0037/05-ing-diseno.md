---
spec: SPEC-0037
agente: ing-diseno
n: 05
fecha: 2026-11-19
estado: completado
---

# SPEC-0037 · 05 · ing-diseno (paso 4, brazo B')

## Hecho

- `docs/diseno/colocacion-b2.csv`: 193 huellas + fila `PLACA,100,100` + referencias (`rx…rtrazo`). Placa **100 × 100 mm**, PCB **2 $ / 5 uds** (Z01, sin aviso). `evaluar`: **0 obligatorias**, 46 objetivos, PUNTOS 5101; ida y vuelta con `colocar.py` sobre copia, mismo resultado.
- `docs/diseno/colocacion-b2.png` (`vista.py placa` de la copia).
- `docs/diseno/colocacion-reglas.csv` (instrucción del coordinador, decisión del usuario 2026-11-19): G02 «sale» borrada; A01 = `U5/zona` a ≤ 0,5 mm del borde lateral (zona entera dentro); F03 = 2,5 mm, `* !H1-H4` (Términos §2.3, incluye bornes y U5); B01–B04 y B12 de 1 a 3 mm de patio a borde para que sean compatibles con F03.
- 25 iteraciones en ≈ 50 min, sin MCP; una imagen al final. Generador: `scratchpad\b2\gen2.py`; mapa ASCII de patios: `scratchpad\b2\mapa.py`.

## PUNTOS

Partida `colocacion-b.csv` (100 × 70, reglas nuevas) 1 108 273 · it. 1 (100 × 100) 1 076 131 · it. 5 58 299 (primera con `referencias`) · it. 10 38 901 · it. 15 6703 · it. 19 5703 (0 obligatorias) · it. 25 5101.

## Decisiones y desviaciones

- 100 × 70 no basta: solo la zona de U5 dentro (21 × 48 mm) y el cobre de Q01–Q05 ocupan ≈ 4000 mm². Con 100 × 100 cumple con poco margen térmico: U10 307, U11 302, U12 305, U1 307, Q1 257/250 y U4 402/400 mm². No he probado tamaños menores: un alto menor no cumpliría Q01.
- Plano: U5 en el borde izquierdo con la zona entera dentro; J2 arriba a la izquierda; J10 y la expansión bajo la zona; BTT de abajo a 0/180° (salidas de lado) para que solapen menos los anillos de cobre.
- Referencias fijadas a mano en la tabla (el reparto voraz de `referencias` no encontraba hueco): R66, R70–R74 y D12–D14.
- Objetivos que no se pueden cumplir con esta disposición: A03 (antena en esquina: imposible con la zona dentro), P02 (paso de 12,7 entre pulsadores), O11 (solo caben 2 columnas a ≤ 5 mm de U5), B10, S03, E01, E05 y E06 (pasivos de potencia apartados para dejar cobre libre), F02, C02–C05 y T04 (texto de JP1 en la librería).

## Lo que muestra la imagen y `evaluar` no ve (propuestas, sin aplicar)

1. C1 (47 µF, VIN_PROT) queda arriba en el centro, a ≈ 60 mm de Q1/U1; D3 queda a 56 mm de U1 y D1/R1 (puerta de Q1) a 28 mm de Q1. Son malos lazos de potencia. Propuesta: una regla `cerca` obligatoria para C1, D1 y R1.
2. USB: J2 está arriba a la izquierda y los pines 13/14 de U5 abajo a la derecha del módulo (≈ 60 mm rodeando U5). Además, J2 queda 2,5 mm hacia dentro del borde: hay que comprobar que el conector entra con la caja.
3. La franja central (rejilla IS, U2/U3 y la fila de R9) queda densa, sin pasillos para pistas ni vías; los anillos de cobre de U10–U12 van al límite y las pistas se los comerán.
4. Los valores en F.Fab se solapan por todas partes (no se fabrica, pero estorba en la revisión). D9 queda entre J10 y J7 (L01).

## Pendiente

- Coordinador/usuario: aprobar 100 × 100 (FAB-08, DEC-0016) y el cambio de reglas de arriba; A03 debería quedar en N/A o reescribirse con la antena dentro.
- Mejoras para `colocacion.py` (no aplicadas): un modo de `referencias` que deshaga pasos o fije primero las columnas densas; que `--detalle` diga qué patios ocupan el anillo de cada fuente de calor; una regla de pasillos de rutado; mostrar que una cifra al límite (por ejemplo U11 300/300) incumple por redondeo.
