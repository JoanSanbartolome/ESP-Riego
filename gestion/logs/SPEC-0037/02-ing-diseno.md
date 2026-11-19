---
spec: SPEC-0037
agente: ing-diseno
n: 02
fecha: 2026-11-19
estado: completado
---

# SPEC-0037 · 02 · ing-diseno (brazo B, solo texto)

## Hecho

- `docs/diseno/colocacion-b.csv`: 193 filas (todas menos H1–H4, que son fijas), cara F. La tabla la genera un script en la carpeta temporal a partir de un plano por bloques; cada iteración = regenerar el CSV + `evaluar` sobre la copia.
- `docs/diseno/colocacion-b.png`: la única imagen, sacada con `vista.py placa --todo` de la copia con `colocar.py` aplicado.
- Plano: U5 arriba a la izquierda (giro 90, la antena entera fuera del borde izquierdo, a 9,5 mm del borde superior), J3 en el borde superior. J4–J6 en el borde superior con los canales 1–3 debajo. Fila SW3–SW8 a y = 92, con paso de 12,7 mm. Abajo, J7 J8 J9 | J10 | J1 F1 Q1 (B10 se cumple: J10 queda entre J7 y J1), con los canales 4–6 encima. J2 en el borde izquierdo bajo U5. La alimentación, abajo a la derecha. U13 en la esquina superior derecha, con U18 cerca.
- 6 iteraciones (≈ 17 min, de 16:18 a 16:35), más la partida.

## Verificación (línea PUNTOS de `evaluar`)

- Partida (la PCB exportada; 193 huellas fuera del contorno): `PUNTOS 251669 = 1000×240 + 100×105 + 11693/10`.
- Iteración 1: `27742 = 1000×26 + 100×13 + 4423/10` (25 solapes).
- Iteración 3: `423 = 1000×0 + 100×0 + 4226/10`. Primera sin incumplimientos.
- Iteración 5: `380 = 0 + 0 + 3803/10`. La 4 dio 481: J3 quedaba a 10 mm de la antena (A04).
- Iteración 6, la final: `373 = 1000×0 + 100×0 + 3728/10`. Sin rutar: Default 2166 · Power_In 268×3 · Salidas 140×3 · Power 170×2.
- No quedan incumplimientos, ni obligatorios ni objetivos. Paré porque la última iteración mejoró menos de un 2 %.
- `verificar.py`: no aplica (no se toca `hardware/v2`; el trabajo se hizo en una copia de la carpeta temporal).

## Lo que la imagen muestra y `evaluar` no ve (propuestas, sin aplicar)

1. Densidad muy desigual: la esquina superior derecha está casi vacía (U13, TP3, TP4, R13, D4) y la alimentación y los canales de abajo, apretados. Propuesta: una métrica de ocupación por zona o un margen mínimo entre patios (0,25–0,5 mm). Ahora se aceptan patios que se tocan (huecos de 0,05 a 0,3 mm), que no dejan sitio para pistas ni vías.
2. Calor: los BTT6050 quedan pegados entre sí y a los bornes, sin superficie de cobre para el pad expuesto. Propuesta: una regla `libre`, o de separación mínima, entre U7–U12 y alrededor de U1, U2 y U4.
3. Buck: C11 y C12 (+5V_BUCK) quedan a unos 10 mm del pad 2 de L1, porque ninguna regla los acerca. Faltan reglas `cerca` para C11/C12 respecto a L1.2, para C19/C21 respecto a U4 y para C15–C17 respecto a U3.
4. Salida de pistas de U5: las filas de pasivos quedan a 0,3 mm de sus pines, sin sitio para sacar las pistas. Lo resuelve la misma separación mínima del punto 1.
5. LED de canal (D6–D11): quedan encajados entre el M7 y el canal vecino. Falta una regla de visibilidad o de distancia al borde.
6. Las referencias de serigrafía se pisan en toda la placa (es cosa de la serigrafía, no de la colocación).
7. Fallo menor de la herramienta: en `--detalle`, las líneas `red` muestran la clase de la PCB («Default») y no la de las reglas K01–K04 (BUS_24V aparece como Default). El resumen sí la aplica.

## Pendiente

- Coordinador: decidir si los puntos 1–3 y 7 pasan a reglas o a mejoras de `colocacion.py` antes del brazo A o de la fase 4.
