---
id: SPEC-0023
titulo: Selección y cálculos del bloque de salidas
fase: 2
estado: abierta
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0023-calculos-salidas
requisitos: [REL-01, REL-03, REL-04, REL-05, REL-06, REL-07, REL-08, REL-09, REL-10]
depende_de: [SPEC-0020, SPEC-0017]
creada: 2026-11-06
cerrada:
validacion:
---

# SPEC-0023 · Selección y cálculos del bloque de salidas

## Objetivo

`docs/diseno/salidas.md` fija cada pieza del bloque de salidas (6 canales de *high-side* BTT6050-1ERA y sus bornes) con su valor y su cálculo, de modo que SPEC-0024 pueda crear las piezas y SPEC-0025 dibujar la hoja `salidas.kicad_sch` sin decidir nada.

## Alcance

- Incluye:
  - **Etapa por canal** con BTT6050-1ERA (DEC-0003), alimentada desde `BUS_24V` (`alimentacion.md`), con los pines fijos de `mcu.md` §9.2: IN1–IN6, IS1–IS6 (ADC1) y **OUT_DEN común** en GPIO38 (DEC-0007).
  - **Entradas (REL-03, REL-04):** R_IN = 10 kΩ por canal y **R_PD = 100 kΩ** (C25803) a GND en el lado del GPIO de cada IN; 6 × R_DEN = 10 kΩ desde OUT_DEN y una sola R_PD de 100 kΩ en OUT_DEN (`mcu.md` §10.2). Comprobar V_IN(H) y V_IN(L) con los datos del BTT.
  - **Medida IS (REL-10):** R_IS a GND, R_SENSE = 10 kΩ en serie hasta el ADC1, *clamp* y condensador de filtro. Cálculo de k_ILIS, rango de corriente útil y atenuación del ADC, y **V_ADC ≤ 3,1 V también en fallo**: con I_IS(FAULT) máxima, V_IS hasta V_S − 1 V (BTT p. 30), el peor caso de `BUS_24V` (≤ 30 V, ALI-01) y la corriente que entra al pin del ESP32-S3 por el *clamp* (máximo VDD + 0,3 V, S tabla 5-4).
  - **Carga abierta en OFF (REL-10):** *pull-up* R_OL de `BUS_24V` a OUT, con el canal apagado y el bus habilitado (ALI-13). Fuga por la válvula ≤ 1 mA y sin activarla; detección frente al umbral de carga abierta del datasheet (§7.3.3.2, p. 27) con la tolerancia de la válvula (0,2–0,56 A, 1–2 válvulas por canal) y del cable; consumo de los 6 R_OL; efecto con JP1 cerrado (DEC-0006).
  - **Corto y sobrecarga (REL-05, REL-08):** lectura de I_IS(FAULT); umbral de aviso de sobrecarga a 1 A; comportamiento con el limitador común (banda 3,5–4,9 A, 4,21 A nominal, `alimentacion.md`).
  - **Carga inductiva (REL-03):** energía de desmagnetización con 2 válvulas por canal frente a la curva E_AS(I_L) del BTT, con la inductancia del fabricante de la válvula o un valor justificado y marcado para medir en el prototipo.
  - **Térmica:** disipación y T_J de cada BTT a 60 °C de ambiente con 1 A continuo y con la carga del ensayo térmico de `docs/02` §6; R_DS(on) en caliente.
  - Condensadores de VS y de OUT, red de GND del chip y protección de la salida que pida el datasheet para un cable largo (≥ 10 m), justificados con página.
  - **LED por canal (REL-07, S):** propuesta (en OUT a 24 V o desde el GPIO) con su corriente, su efecto en la detección de carga abierta y su coste; se puede proponer descartarlo, justificándolo.
  - **Bornes:** WJ500V-5.08-2P (ficha existente), 2 polos por canal (OUT_n y GND), canales 1–3 en el borde superior y 4–6 en el inferior, con el mismo orden de pines (REL-06, REL-09, FAB-07); corriente de 4,9 A (REL-05).
  - **Restricciones de layout:** anchos de `Power_In` hasta cada *high-side* y de `Salidas` hasta cada borne (REL-05: ≈ 1,2 mm con 1 oz para 4,9 A y ΔT ≤ 40 °C; ΔT ≤ 10 °C con la carga máxima), retornos de GND (FAB-03), cobre del EP, R_IN/R_DEN junto al BTT y R_PD en el lado del GPIO.
  - **Referencias:** siguen a las del MCU sin chocar (`mcu.md` §11 llega a U6, R25, C26, D5, J3 y SW2): las de esta hoja empiezan en U7, R26, C27, D6 y J4. **Choque aparente:** en `estudio-salidas.md` «U5» y «U6» son IDs de observaciones (tabla de la línea 31), no referencias; `salidas.md` no los usa como designadores y lo aclara en una nota.
  - Segunda fuente BTT6030-2ERA: qué cambiaría (DSEL, k_ILIS, *routing*), sin diseñarla.
  - Lista de piezas con LCSC y stock, Anexo A con los datos de las fichas nuevas, notas para el firmware (constantes y umbrales de IS, secuencia de carga abierta) y tabla de etiquetas jerárquicas de la hoja.
- Excluye:
  - abrir KiCad (ni el MCP ni `kicad-cli`): SPEC-0021 lo usa en paralelo;
  - crear símbolos, huellas o fichas;
  - cambiar requisitos: una cifra que no cuadre con `docs/02` se propone al coordinador;
  - modificar archivos existentes: solo se crean `docs/diseno/salidas.md` y el log (los cambios a otros documentos se proponen en el log).

## Entradas

- `docs/02-especificaciones-v2.md`: REL-01…REL-10, ALI-01, ALI-12, ALI-13, FAB-03, FAB-07, FAB-09 y §6 (pruebas).
- `docs/diseno/estudio-salidas.md` (§1.2 cargas; §11: S7, §11.4 y §11.5).
- `docs/diseno/mcu.md` §9.2 (pines), §10.2 (R_PD de 100 kΩ) y Anexo C (etiquetas).
- `docs/diseno/alimentacion.md` (`BUS_24V`, limitador TPS26632, banda 3,5–4,9 A, JP1, restricciones de `BUS_24V`).
- `gestion/decisiones/DEC-0003`, `DEC-0004`, `DEC-0006` y `DEC-0007`.
- Fichas `hardware/componentes/BTT6050-1ERA.md`, `BTT6030-2ERA.md`, `WJ500V-5.08-2P.md` y `datasheets/BTT6050-1ERA.pdf`.
- Checklists `gestion/checklists/requisitos.md` y `esquema.md` (v6, sección «Cálculos»).

## Entregables

- `docs/diseno/salidas.md`.
- Log `gestion/logs/SPEC-0023/01-ing-esquematicos.md` con el repaso de la checklist.

## Criterios de aceptación

- [ ] Cada requisito REL-01…REL-10 tiene en el documento la pieza o el cálculo que lo cumple, con datasheet y página.
- [ ] V_ADC ≤ 3,1 V en todos los casos de fallo de IS, con el peor caso de tensión y tolerancias, y la corriente de *clamp* dentro del límite del pin.
- [ ] Carga abierta en OFF: R_OL con fuga ≤ 1 mA, sin activar la válvula, y detección con margen frente al umbral del datasheet.
- [ ] R_PD y R_IN/R_DEN coherentes con `mcu.md` §10.2 (REL-04).
- [ ] E_AS con 2 válvulas por canal por debajo de la curva del datasheet, con la inductancia justificada.
- [ ] T_J de cada BTT con margen a 60 °C de ambiente.
- [ ] Referencias sin choque con alimentación ni MCU, y nota sobre U5/U6 de `estudio-salidas.md`.
- [ ] Lista de piezas con LCSC y stock, y marca de las que necesitan pieza nueva.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-06 | coordinador | Crea la spec (propuesta) | |
| 2026-11-06 | coordinador | Abre la spec (encargo del usuario), en paralelo con SPEC-0021 (solo texto) | |
