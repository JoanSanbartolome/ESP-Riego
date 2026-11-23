---
spec: SPEC-0038
agente: ing-diseno
n: 01
fecha: 2026-11-23
estado: completado
---

# SPEC-0038 · 01 · ing-diseno

## Hecho

- **U4 → Diodes AP2114H-3.3TRG1** (C150716; 2 300 uds en JLCPCB el 2026-11-23; 0,2386 $ con 5 uds y 0,1899 $ con 50). Mismo patillaje que el TLV1117LV, así que no cambian el símbolo, la huella ni la PCB. Ficha y PDF: `hardware/componentes/AP2114H-3.3TRG1.md` y `datasheets/AP2114H-3.3TRG1.pdf`. Cálculo: `alimentacion.md` §3.9.
- **Campos** (`campos.py aplicar` y `campos-*.csv`): C3 y C27–C38 pasan a C28233; C8 sigue en 220 nF. J10 pasa a BH254R-10P, con la huella oficial `IDC-Header_2x05_P2.54mm_Horizontal`.
- **JP1:** se quita el «1» de serigrafía de 0,8 mm (el puente no tiene polaridad); los textos de F.Fab, a 0,15 mm de trazo. El punto l. 27 de `librerias` (pin 1 en serigrafía) no aplica: el «1» queda en F.Fab.
- **PCB:** `sincronizar.py --actualizar JP1` recarga J10 y JP1 en su sitio (84 campos, paridad 0). Solo se mueve la referencia de J10, a la posición por defecto de su huella.
- **Documentos:** `alimentacion.md`, `salidas.md` (§0, §3.3, §4.3, §4.4, §5.3 y §9), `conectores.md` y `arquitectura.md`. Fichas de bloque, `BH254R-10P.md` y `BTT6050-1ERA.md`. Títulos de las hojas de U4 y J10. El Value de U4, bajo su GND: pisaba el cable de C19.

Huellas que cambian frente a `main`: C3, C27–C38, U4, J10, JP1.

## Decisiones y desviaciones

- **U4:** TPTLV1117LV33DCYR descartado: es un 1117 clásico, con 1,25 V de caída máx. a 500 mA (LCSC, p. 2).
- **AP2114H:** caída ≤ 0,41 V a 0,45 A y 125 °C (p. 12 y Fig. 32, p. 21), así que necesita 3,71 V, por debajo de los 3,9 V. Estable con 4,7 µF cerámicos (pp. 1 y 12), y C19 es de 10 µF. Precisión de ± 2,3 %; T_J de 109 °C con 0,81 W. El símbolo sigue siendo el `TLV1117-33` oficial, con el mismo patillaje.

## Verificación

- **`verificar.py`:** ERC 0, DRC 0 (448 sin conectar) y paridad 0; `campos.py revisar`, 0. `esquema.pcb_main` falla solo con las 16 referencias declaradas arriba.
- **`hoja.py netlist` frente a `main`:** 0 diferencias de red; J10 tiene las mismas redes pin a pin.
- **`evaluar` de `colocacion-b4.csv` sobre una copia:** PUNTOS 6151, **0 obligatorias**, 57 objetivos (T04 de JP1 ya se cumple), 0 solapes y serigrafía sin fallos.

## Para validación

- **U4:** la R_θJA con cobre no está publicada (128 °C/W sin disipador, p. 7, daría 164 °C); los 60 °C/W con ≥ 4 cm² son una suposición. El arranque con *fold-back* (50 mA, p. 12, nota 2) queda como prueba del prototipo.
- **C_VS y C3 efectivos:** 80 / 73 nF a 24 / 30 V y 60 °C (SimSurfing), frente a los 85–90 nF que supone DEC-0018.

## Pendiente

- **Usuario, C3:** 73–80 nF efectivos frente al «0,1 µF o más» de TPS2663 p. 27. Se propone dejarlo en 220 nF (C513710 sigue por C8), +0,014 $/placa (§10.8).
- **jr-conformidad:** P4 ahorra 0,16 / 0,08 $/placa (5 / 50 uds) frente al TLV1117LV. `estudio-coste.md` §0, §2 y §9 siguen con «por determinar».
