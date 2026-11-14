---
spec: SPEC-0029
agente: ing-diseno
n: 02
fecha: 2026-11-14
estado: completado
---

# SPEC-0029 · 02 · ing-diseno

## Hecho

- `docs/diseno/sensores.md`: variante, dirección, eléctrico, modelo térmico de la isla, restricciones de AMB-02 (tabla del §0), firmware, piezas, trazabilidad y anexo de etiquetas.
- `hardware/v2/sensores.kicad_sch` (A4, nueva): U13 SHT40-AD1B-R3 y C47 100 nF. `esp-riego.kicad_sch`: hoja «Sensores» (página 6) unida a MCU con etiquetas `I2C_SDA`/`I2C_SCL`; quitadas las 2 no conexiones provisionales de esos pines; texto de la raíz al día.
- `hardware/v2/esp-riego.kicad_pcb`: sincronizada; U13 y C47 nuevas sin colocar; U13 enlaza el 3D de respaldo de la ficha.
- `hardware/componentes/campos-sensores.csv`: C46 → **C47**. C46 ya existe en Salidas (4,7 µF a granel); la spec y el paso 1 lo daban libre.
- `herramientas/kicad/`: `_comun.modelo_de_respaldo` (nueva); `sincronizar.py` la aplica al cargar una huella; `comprobar.py librerias.3d` acepta el respaldo y lo nombra; README al día. `hardware/v2/README.md`: fila de Sensores y no conexiones restantes.
- Usos de `herramientas/kicad/`: `hoja.py generar` (2), `hoja.py netlist`, `sincronizar.py`, `campos.py revisar`, `huella.py`, `hoja.py pines` (2), `vista.py hoja` (3), `vista.py placa`, `colocar.py --exportar` y `comprobar.py`. En la carpeta temporal, 1 script (`s29_raiz.py`: hoja y etiquetas en la raíz; `hoja.py` no lo hace). Sin MCP.

## Decisiones y desviaciones

- Se mantiene SHT40: ninguna variante cumple ± 3 % HR sin calibrar. Hace falta recalcular la HR con la T corregida (Magnus) y, si sale, un *offset* de HR (sensores.md §2 y §8). SHT41 queda como mejora (+1,41 $).
- Estimación térmica (sensores.md §5): la isla sigue al ≈ 29 % del calentamiento de la placa, ≈ 1,3 K en reposo y ≈ 3,0 K con 6 salidas a 0,25 A. Es previsible que haga falta la corrección según las salidas (ya prevista en AMB-02).
- I²C, +3V3 y GND por el puente a 0,25 mm (`Default`, FAB-03), sin regla nueva de anchura. Lo nuevo para la fase 4 es el área sin relleno en F.Cu y B.Cu y las ranuras.
- `I2C_SCL` es `input` en la hoja de sensores (SCL del sensor solo es entrada, p. 17); en MCU sigue bidireccional.

## Verificación

- `verificar.py hardware/v2`: ERC 0, DRC 0 errores (0 avisos), paridad 0; sin conectar 352 → 358 (+6: 4 pads de U13 y 2 de C47). `[auto]`: 16 OK; FALLAN solo `librerias.fichas` (MCU, ya en SPEC-0028) y `librerias.gitattributes` (ya estaba).
- `campos.py revisar`: 0 diferencias con la tabla. Netlist: `/I2C_SDA` = {U5-34, R24-2, U13-1}; `/I2C_SCL` = {U5-35, R25-2, U13-2}.
- `test_kicad.py Generales Comprobar Mutaciones Pcb`: 21/22. Falla `Mutaciones.test_librerias_fichas`, ajena a este cambio: C25804 está también en `bloque-salidas.md`, así que la mutación de `bloque-alimentacion.md` ya no lo hace fallar.

## Para validación

- Pinout y huella oficiales frente a §5.4 (p. 17) y Fig. 17 (p. 16): sensores.md §7. 3D de respaldo enlazado en la instancia (la ficha lo da como pendiente de verificar). Supuestos del §5 (h = 10 W/m²K, U5 0,33 W, buck 0,12 W): ± 50 %.

## Pendiente

- Coordinador: añadir a `test_kicad.py` la prueba de `modelo_de_respaldo` (oficial ausente con respaldo → ruta `${KIPRJMOD}`; oficial existente, sin respaldo, ruta ya del proyecto o `libs3d=None` → `None`) y un caso de `librerias.3d` con respaldo. Arreglar `test_librerias_fichas` (C25804). Está fuera de mi zona.
- `mcu.md` §8.2 da 61 mA para el calentador: el máximo del datasheet es 100 mA (p. 9). No cambia nada: el calentador no se usa.
