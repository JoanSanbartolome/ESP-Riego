---
id: SPEC-0032
titulo: Integración y revisión global del esquema
fase: 3
estado: propuesta
responsable: ing-diseno
revisor: ing-validacion
rama: spec/SPEC-0032-integracion-esquema
requisitos: [KIC-02, KIC-03, ALI-12, MCU-05, REL-04, FAB-05]
depende_de: [SPEC-0028, SPEC-0029, SPEC-0031, SPEC-0033, SPEC-0034, SPEC-0035]
creada: 2026-11-13
cerrada:
validacion:
---

# SPEC-0032 · Integración y revisión global del esquema

<!-- Objetivo, restricciones y criterios: sin pasos ni números de línea. Unas 60 líneas. Una spec de bloque o de hito de layout lleva sus pasos en «Alcance». -->

## Objetivo

El esquema v2 queda cerrado para el layout: raíz completa, ERC 0, campos completos y revisión global hecha. Es la base de la etiqueta `v2.0-sch`.

## Alcance

- Incluye:
  - raíz: todas las hojas unidas, sin no conexiones provisionales;
  - la hoja raíz `esp-riego.kicad_sch` con el estilo de DEC-0015 (KIC-06, `gestion/checklists/esquema.md` v17);
  - el orden de las páginas comprobado con `hoja.py paginas`;
  - `docs/diseno/arquitectura.md` (el `docs/04-arquitectura.md` del plan, en la zona de `ing-diseno`): diagrama de bloques, presupuesto de potencia por raíl con todos los bloques (ALI-12) y tabla de GPIO contrastada con la netlist (base de FW-02);
  - revisión global de la fase 3 del plan: pines de arranque, estado de las salidas en el reset, polaridades, ESD en todos los conectores de campo y test points;
  - salidas con los límites de uso de SPEC-0034 (DEC-0014), que ya actualiza `salidas.md`, `estudio-salidas.md` y la memoria de ing-diseno: aquí solo se comprueba que la hoja integrada los conserva. La etiqueta no depende de medir la válvula;
  - BOM preliminar con coste y stock (`jr-conformidad`) y PDF del esquema;
  - casillas de las fases 2 y 3 de `docs/03-plan-de-diseno.md` (coordinador);
  - las 5 B de VAL-0028-01: casos de `test_kicad.py` que no detectan su mutación, orden de `jlc.resultados` (-01) y `is_file` de `_comun.modelo_de_respaldo` (-02), de `ing-diseno` (la batería la lleva el coordinador a `herramientas/pruebas/`); notación de los condensadores entre tablas, `4.7uF`/`22uF` frente a `4.7u`/`22u` (-03), y `verificado_por` de `BTT6050-1ERA.md` con VAL-0028-01 por la pasta del EP (-04), de `jr-conformidad` con la BOM; I²t del TA10 igual en `alimentacion.md` §3.2 y en `0451010.MRL.md` (-05), de `ing-diseno`.
- Excluye: el layout; cambios de requisitos, de decisiones o de coste (se proponen en PENDIENTE); la etiqueta `v2.0-sch`, que el coordinador propone al usuario al cerrar.

## Entradas

- `docs/02-especificaciones-v2.md` v0.8: ALI-12, ALI-13, MCU-05, REL-04, REL-10, REL-11, FAB-05, KIC-02, KIC-03, KIC-06 y FW-02.
- `docs/03-plan-de-diseno.md`, fases 2 y 3 (las casillas que cierra esta spec).
- `gestion/decisiones/DEC-0015-esquema-legible.md` (reglas de estilo) y DEC-0014 (límites de uso de las salidas).
- `gestion/checklists/esquema.md` v17 entera, en especial «Estructura», «Microcontrolador», «Salidas e interfaces de campo» y «Estilo».
- `docs/diseno/<bloque>.md`: la sección de consumo de cada bloque (presupuesto), `mcu.md` (asignación de GPIO y pines de arranque), `salidas.md` §0 (REL-11) y `conectores.md` (ESD de los conectores de campo); `alimentacion.md` §3.2 para VAL-0028-01-05.
- `gestion/informes/VAL-0028-01.md`, hallazgos -01 a -05 (cada uno dice qué cambiar).
- `herramientas/kicad/README.md`: `hoja.py` (`generar`, `paginas`, `netlist --grupos`), `vista.py`, `comprobar.py`, `campos.py`, `sincronizar.py` y `jlc.py`.
- `hardware/componentes/campos-*.csv`, `stock-*.csv` y las fichas de pieza, para la BOM.

## Entregables

- `ing-diseno` (paso 1):
  - `hardware/v2/esp-riego.kicad_sch` con el estilo de DEC-0015 y las páginas en el orden del árbol; las hojas que cambie la revisión global, y `esp-riego.kicad_pcb` resincronizado si cambia la netlist.
  - `docs/diseno/arquitectura.md`: diagrama de bloques, presupuesto por raíl (24 V, 5 V, 3,3 V) con todos los bloques y las 6 salidas activas, tabla de GPIO contrastada con la netlist y la revisión global (punto, evidencia, resultado).
  - `docs/diseno/alimentacion.md` §3.2 (VAL-0028-01-05).
  - VAL-0028-01-01 y -02: el cambio de `test_kicad.py` como parche en la carpeta temporal, con su ruta en el parte y la mutación que ahora falla; lo aplica el coordinador en `herramientas/pruebas/`.
  - Imagen de la raíz (ruta en el parte) y parte `NN-ing-diseno.md`.
- `jr-conformidad` (paso 2, después del 1):
  - `fabricacion/v2.0-sch/bom.csv` (BOM preliminar: referencias, cantidad, Value, MPN, `LCSC Part#`, tipo *Basic*/*Extended*, stock con fecha, precio unitario y coste por placa) con el coste total por placa en el parte.
  - `fabricacion/v2.0-sch/esquema.pdf`, exportado del proyecto integrado.
  - VAL-0028-01-03 (notación de condensadores en `campos-mcu.csv` y `campos-conectores.csv`, aplicada al esquema y a la PCB) y -04 (`verificado_por` de `BTT6050-1ERA.md`).
  - Parte `NN-jr-conformidad.md`.
- Coordinador: casillas de las fases 2 y 3 de `docs/03-plan-de-diseno.md` y la ruta del documento de arquitectura.

## Criterios de aceptación

- [ ] `verificar.py hardware/v2`: ERC 0, paridad 0 y ningún `[auto]` en FALLA; `campos.py revisar` sin diferencias.
- [ ] La raíz une las cinco hojas sin no conexiones provisionales y cumple las reglas 1–6 de DEC-0015 a la vista de su imagen.
- [ ] `hoja.py paginas hardware/v2` sale con código 0.
- [ ] Netlist idéntica por grupos de pines a la de `main` al abrir (`hoja.py netlist --grupos`), salvo los cambios que justifique la revisión global, cada uno anotado en el parte con su motivo.
- [ ] Presupuesto: la lógica ≤ 4,8 W en la entrada con el 5 V de la expansión a su carga máxima, y la entrada ≤ 5,1 A con el limitador en su límite superior (ALI-12); cada raíl, con margen frente a su regulador.
- [ ] Tabla de GPIO igual a la netlist pin a pin; cumple MCU-05 (ADC solo en ADC1, nada de salidas en GPIO0/3/45/46, GPIO19/20 al USB).
- [ ] Revisión global con evidencia por punto: pines de arranque, salidas y limitador apagados en el reset y el flasheo (REL-04), polaridades, ESD en cada conector de campo y test points.
- [ ] Salidas conservan lo de SPEC-0034: D12–D17 montados y la tabla REL-11 de `salidas.md` §0 sin cambios.
- [ ] BOM con todas las piezas montadas, cada una con `LCSC Part#` (FAB-05), stock con fecha y coste; coste total por placa en el parte.
- [ ] PDF con todas las páginas en el orden del árbol.
- [ ] Los 5 hallazgos de VAL-0028-01 cerrados; `test_kicad.py` en verde con las mutaciones de -01 y -02 detectadas.

## Plan de validación

Nivel **completo** (esquema; DEC-0005), con `esquema.md` v17.

- Reproducir de forma independiente: `verificar.py hardware/v2`; `hoja.py paginas`; la comparación de netlists frente a `main`; la tabla de GPIO contra la netlist, pin a pin, y contra MCU-05; el presupuesto de potencia (sumas y márgenes de cada raíl); el estado de las salidas y del limitador en el reset (pull-down y polaridad de la entrada de control); las mutaciones de -01 y -02.
- Por muestreo: tres líneas de la BOM (stock y precio en LCSC), dos conectores de campo con su ESD, la imagen de la raíz frente a DEC-0015 y dos páginas del PDF.

## Registro

| Fecha | Agente | Acción | Referencia | Tokens | Acciones | Min |
|---|---|---|---|---|---|---|
| 2026-11-13 | coordinador | Crea la spec (propuesta) | | | | |
