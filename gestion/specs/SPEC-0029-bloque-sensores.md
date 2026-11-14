---
id: SPEC-0029
titulo: Bloque de sensores
fase: 3
estado: cerrada
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0029-bloque-sensores
requisitos: [AMB-01, AMB-02, KIC-02]
depende_de: []
creada: 2026-11-13
cerrada: 2026-11-14
validacion: VAL-0029-01
---

# SPEC-0029 · Bloque de sensores

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

El bloque de sensores de la v2 queda completo: `docs/diseno/sensores.md`, la pieza del SHT4x y la hoja `hardware/v2/sensores.kicad_sch` unida a la raíz, con ERC 0 y paridad 0.

## Alcance

- Incluye:
  - selección y cálculos: variante del SHT4x a partir de `hardware/componentes/SHT4x.md`, dirección I²C, desacoplo y consumo a 3,3 V;
  - restricciones de layout de AMB-02 (borde lateral según FAB-07, ranuras, sin cobre debajo, puente térmico), listas para `docs/diseno/restricciones.csv`;
  - símbolo, huella y modelo 3D, si no valen los oficiales;
  - hoja nueva y su hoja en la raíz, unida a `I2C_SDA` e `I2C_SCL` de la hoja MCU (GPIO41 y 42; R24 y R25 ya están en la hoja MCU);
  - campos (`hardware/componentes/campos-sensores.csv`), stock y fichas; PCB sincronizada con las huellas sin colocar.
- Excluye: colocación, ranuras y rutado (fase 4); el I²C de expansión (SPEC-0031).

## Entradas

- `hardware/componentes/SHT4x.md` entera (variantes, pinout, recomendaciones de layout, modelo 3D de respaldo) y su datasheet local `hardware/componentes/datasheets/SHT4x.pdf` (V7.3).
- `docs/diseno/mcu.md`: §8.2 (presupuesto de +3V3), §9.2 (filas de GPIO41 y 42), §11 (R24 y R25, cálculo de los *pull-ups*, C25 como referencia del 100 nF), §12 (fila I2C_SDA/SCL y antena) y Anexo C (forma de las etiquetas jerárquicas).
- `docs/02-especificaciones-v2.md`: AMB-01, AMB-02, FAB-07 y KIC-02; FW-03 para la corrección.
- `herramientas/kicad/README.md` (herramientas, formatos y límites conocidos; `hoja.py` no toca los pines de hoja de la raíz).
- Checklists `gestion/checklists/esquema.md` y `gestion/checklists/librerias.md`.
- Modelo de bloque cerrado: `docs/diseno/salidas.md` (estructura del documento y del Anexo B) y `hardware/componentes/campos-salidas.csv`.
- Referencias libres: U13 y C46 en adelante (las mayores en uso son U12 y C45).
- Punto de partida (`main` en `e33e1f0`): `verificar.py hardware/v2` da ERC 0, DRC 0 con 352 sin conectar, paridad 0, y FALLA solo en `librerias.fichas` y `librerias.gitattributes` (SPEC-0028).

## Entregables

- Paso 1, `jr-conformidad`: `hardware/componentes/campos-sensores.csv` (SHT40-AD1B-R3, C2848306, salvo que el stock aconseje otra variante, y el 100 nF C14663), `hardware/componentes/stock-sensores.csv` con las tres variantes de la ficha y el 100 nF, la fila de stock de `SHT4x.md` al día y parte `gestion/logs/SPEC-0029/01-jr-conformidad.md`.
- Paso 2, `ing-diseno`: `docs/diseno/sensores.md` (variante, dirección, desacoplo, consumo, restricciones de layout en formato de fila de `restricciones.csv`, trazabilidad y anexo de etiquetas), `hardware/v2/sensores.kicad_sch`, `hardware/v2/esp-riego.kicad_sch` (hoja nueva), `hardware/v2/esp-riego.kicad_pcb` sincronizada, y parte `gestion/logs/SPEC-0029/02-ing-diseno.md`, que cuenta los scripts escritos en la carpeta temporal y los usos de `herramientas/kicad/`. Si fija otra variante que la del paso 1, lo dice en PENDIENTE.
- Paso 3, `ing-validacion`: `gestion/informes/VAL-0029-01.md`.

## Criterios de aceptación

- [ ] Cada pieza, valor, huella y pin de la hoja coinciden con `sensores.md` y con el datasheet (pinout de §5.4, p. 17): SDA, SCL, VDD y VSS en I2C_SDA, I2C_SCL, +3V3 y GND.
- [ ] `verificar.py hardware/v2`: ERC 0, DRC 0 errores, paridad 0, y ningún punto `[auto]` nuevo en FALLA. Los «sin conectar» suben solo por las huellas nuevas, y el parte da la cifra.
- [ ] `campos.py revisar hardware/v2`: 0 diferencias con `campos-sensores.csv`.
- [ ] La raíz tiene cinco hojas (alimentación, MCU, salidas, sensores y conectores); `I2C_SDA` e `I2C_SCL` de la hoja de sensores llegan a GPIO41 y GPIO42 de U5, sin *pull-ups* duplicados (R24 y R25 siguen en la hoja MCU) y sin no conexiones en pines de hoja ya unidos.
- [ ] La huella no tiene pad central, la instancia enlaza el modelo 3D de respaldo de la ficha y ninguna pieza usa una librería de la v1.
- [ ] La dirección I²C de la variante elegida no choca con nada del bus de la placa; el calentador queda fuera de uso y el consumo cuadra con `mcu.md` §8.2.
- [ ] `sensores.md` da las restricciones de AMB-02 (borde lateral según FAB-07, ranuras, sin cobre debajo, puente térmico, distancia a buck, LDO, módulo y salidas) listas para `restricciones.csv`, sin colocar ni rutar nada.

## Plan de validación

Nivel **completo**. Se reproduce de forma independiente: el mapeo de pines del símbolo y de la huella frente al datasheet (§5.4, p. 17, y Figura 15, p. 15: pads, paso 0,8 y sin pad central), la dirección I²C de la variante, la unión de la raíz con GPIO41 y 42 en la netlist exportada, y el modelo 3D enlazado en la instancia. Por muestreo: las filas de `campos-sensores.csv` y de `stock-sensores.csv` frente a LCSC, y dos restricciones de AMB-02 frente al requisito.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-13 | coordinador | Crea la spec (propuesta) | | | | |
| 2026-11-14 | coordinador | Abre la spec |  |  |  |  |
| 2026-11-14 | jr-conformidad | campos-sensores.csv (U13, C46) y stock del 2026-11-14 | 01-jr-conformidad | 49358 | 9 | 1 |
| 2026-11-14 | ing-diseno | sensores.md, hoja de sensores (U13, C47), raíz con cinco hojas, PCB sincronizada y modelo 3D de respaldo en sincronizar.py | 02-ing-diseno | 239919 | 76 | 17 |
| 2026-11-14 | ing-validacion | Validación completa: 1 M y 3 B | VAL-0029-01 | 173217 | 47 | 8 |
| 2026-11-14 | coordinador | Cierra la spec | VAL-0029-01 (APROBADO_CON_OBSERVACIONES) |  |  |  |
