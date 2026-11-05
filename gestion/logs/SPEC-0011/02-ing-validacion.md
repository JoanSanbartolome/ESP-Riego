---
spec: SPEC-0011
agente: ing-validacion
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0011 · 02 · ing-validacion

## Orden recibida

SPEC-0011 · rama spec/SPEC-0011-requisitos-v04 (activa) · corrección en el commit siguiente a 4a0b771 (`git diff 4a0b771 HEAD`) · Haz: segunda validación → gestion/informes/VAL-0011-02.md + log 02. Comprueba uno a uno los 9 hallazgos de VAL-0011-01. Verifica también los cambios que no propuse:

- la carga instalada recalculada a −10 °C y 24,5 V (12 × 0,28 × 1,02 × 1,13 ≈ 3,9 A);
- la banda de 3,9–4,9 A (≈ 4,4 A ± 11 %);
- la lógica ≤ 0,2 A, con 4,9 + 0,2 = 5,1 < 5,15 A.

Además: que la banda sigue siendo alcanzable con piezas comunes, que 0,2 A de lógica es realista y que nada añade complejidad que el usuario descartó. Sin MCP; git solo de lectura.

## Contexto consultado

- El diff `4a0b771..0d6ab92` (10 archivos) y docs/02, DEC-0004 y las checklists en `0d6ab92`.
- Mi informe VAL-0011-01, y `estudio-salidas.md` §1.2–§1.3 (corriente de diseño de las válvulas).
- Las hojas ya extraídas en `scratchpad/val1101/` (LRS, BTT6050, LM5069) y la página del TPS2663.
- El consumo del ESP32-S3 en TX (≈ 340 mA), de una tabla reproducida en un buscador.
- Al final, el mensaje de `0d6ab92`.

## Acciones

1. He comprobado la rama y el commit (`0d6ab92`). No he usado ni el MCP ni `kicad-cli`.
2. He vuelto a ejecutar `traza.py`: 0 avisos y 13 IDs cambiados, que coinciden con la spec y con la DEC.
3. He escrito `scratchpad/val1101/calc2.py`:
   - la carga instalada, con la base del estudio;
   - 126 W / 24,5 V;
   - la banda frente al TPS2663 y el LM5069;
   - la potencia de la lógica;
   - las lecturas de ALI-09 con ± 3 %;
   - IPC-2221 a 3,8 A.
4. He buscado con Grep las cifras sustituidas (3,5 A, 0,25 A, 5,25 A, 16,5 V, 31,5 V, 3,4 A…).
5. He escrito el informe y este log.

## Decisiones y justificación

- **Doble corrección por frío (01) en B:**
  - el estudio y REL-05 tratan 0,28 A como valor en frío, así que 3,9 A aplica el frío dos veces; lo correcto son 3,43–3,47 A;
  - el error es conservador y la banda sigue siendo alcanzable (TPS2663), por eso no lo subo de B;
  - aun así, recomiendo corregirlo antes del merge: es la cifra de un requisito M que no se puede reproducir, deja fuera los *hot-swap* de ± 12 % y SPEC-0008 la llevaría al estudio.
- **5,15 frente a 5,14 A (02):** redondeo con 43 mA de margen. Sigue cerrando también a potencia constante con caída en el cable. B.
- **Prueba de un canal a 25 °C:** la equivalencia exacta sería 22,4 °C. Lo acepto sin hallazgo porque la diferencia queda dentro de la incertidumbre de la medida.
- **0,2 A de lógica:** con el ESP32-S3 transmitiendo, ≈ 0,1 A a 24 V. Quedan ≈ 0,4 A a 5 V para la expansión. Es realista.
- **Veredicto APROBADO_CON_OBSERVACIONES** (B 4): los tres criterios se cumplen.

## Verificación

- Trazabilidad en memoria: 0 avisos y 57 requisitos.
- Cifras de la DEC = cifras de docs/02, incluidos sus dos errores comunes (observaciones 01 y 02).

## Pendiente

- **Coordinador:** las observaciones 01–04, antes del merge (recomendado para la 01) o como spec propuesta. Pedir a ing-esquematicos que actualice su memoria (VAL-0011-01-08 c).
- **Merge:** regenerar `TABLERO.md` y `TRAZABILIDAD.md`.
