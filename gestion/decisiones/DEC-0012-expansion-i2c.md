---
id: DEC-0012
titulo: D9, módulo de expansión por I²C con TCA9535 y ADS1115
fecha: 2026-11-15
estado: aceptada
decide: usuario
specs: [SPEC-0006, SPEC-0031]
requisitos: [EXP-02, EXP-04, ALI-12, ALI-13, REL-04, REL-10, AMB-03]
---

# DEC-0012 · D9, módulo de expansión por I²C con TCA9535 y ADS1115

## Contexto

D9 (arquitectura del módulo de expansión, EXP-02 y EXP-04) quedó para el usuario con el informe de SPEC-0006 (DEC-0011). El informe, `docs/diseno/viabilidad-expansion.md` (VAL-0006-02, APROBADO_CON_OBSERVACIONES), compara cinco arquitecturas con los mismos criterios y define el conector EXP-02 (§10). Con cualquiera de ellas, el módulo necesita su propia entrada de 24 V y su propio limitador: con la fuente común de 5 A, el limitador de la placa más la lógica llegan a 4,77 A frente a los 5,14 A a los que actúa la fuente (§0, §2.2).

## Opciones consideradas

Coste por módulo de 8 canales con 5 / 10 uds, montaje JLCPCB incluido (§8, consulta del 2026-11-15):

1. **I²C, TCA9535 + ADS1115** (recomendada): 30,9 / 24,9 $. ≤ 3 m de cable plano (≤ 50 m con P82B715), diagnóstico de REL-10, estado seguro por hardware (EXP_EN con *pull-down*), todo en el YAML de la placa.
2. **RS-485 / Modbus:** 31,3 / 25,4 $ más adaptador; esclavo sin ESPHome.
3. **74HC595:** 27,2 / 22,1 $; sin diagnóstico.
4. **Nodo ESP32-S3 propio** (alternativa): 37,5 / 29,9 $; por Wi-Fi, no usa EXP-02; estado seguro por firmware.
5. **CAN:** 32,5 / 26,0 $ más adaptador; esclavo sin ESPHome.

## Decisión

Decidida por el usuario el 2026-11-15: **arquitectura 1, I²C con TCA9535 + ADS1115**, la recomendada por el informe (§9).

## Consecuencias

- **Conector EXP-02:** el de `viabilidad-expansion.md` §10, sin cambios: IDC 2 × 5 a 2,54 mm polarizado (BH254V-10P, C492442) con 5 V y 3,3 V por sendos TPS2553, I2C_EXP (GPIO47/48), EXP_INT (GPIO35), EXP_EN (GPIO36, antes EXP_IO2) y 4 GND; ESD con dos USBLC6-2SC6; *pull-ups* de 2,2 kΩ en el lado del conector. Lo pasa SPEC-0031 a `conectores.md`, a `mcu.md` (§9.2, §10.1, §10.2, Anexo B y §14.2) y a la hoja. ALI-12 no cambia y GPIO10, 18, 37 y 39 quedan para EXP-03.
- **Requisitos:** el texto de EXP-02 no cambia (EXP_EN es uno de los «al menos 2 GPIO»). Falta un requisito para el módulo: entrada de 24 V y limitador propios, sin pasar 24 V por EXP-02 (VAL-0006-01, punto a). Va en EXP-04 o con un ID propio, y es un cambio de requisitos con su propia spec; no cambia ALI-01, ALI-12 ni ALI-13. D9 pasa a decidida en `docs/02` §8 en esa misma spec.
- **Firmware (fase 6):** componentes `pca9554` (16 pines) y `ads1115`; EXP_EN a bajo en `on_boot`, `ota: on_begin` y `on_shutdown`, y el expansor a 0 antes (REL-04 se extiende al módulo).
- **Pendiente:** la corriente de las válvulas instaladas (DEC-0011) fija R_ILIM y la fuente del módulo (§2.3). El diseño del módulo queda fuera de la v2.
