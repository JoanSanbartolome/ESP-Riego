---
id: SPEC-0020
titulo: Selección y cálculos del bloque MCU
fase: 2
estado: cerrada
responsable: ing-esquematicos
revisor: ing-validacion
rama: spec/SPEC-0020-calculos-mcu
requisitos: [MCU-01, MCU-02, MCU-03, MCU-04, MCU-05, MCU-06, MCU-07, ALI-07]
depende_de: []
creada: 2026-11-05
cerrada: 2026-11-06
validacion: VAL-0020-01
---

# SPEC-0020 · Selección y cálculos del bloque MCU

## Objetivo

`docs/diseno/mcu.md` fija cada pieza del bloque MCU con su valor y su cálculo, y la tabla de GPIO de toda la placa, de modo que SPEC-0021 pueda crear las piezas y SPEC-0022 dibujar la hoja sin decidir nada.

## Alcance

- Incluye:
  - variante del módulo ESP32-S3-WROOM-1 (flash, PSRAM y su efecto en GPIO35–37), con LCSC y stock (MCU-01);
  - zona libre de la antena según la guía hardware de Espressif, como restricción para el floorplan (MCU-02);
  - USB-C nativo con ESD y CC de 5,1 kΩ, coherente con la unión al raíl de 5 V de `alimentacion.md` (TPS2116) (MCU-03);
  - BOOT y RESET con red RC en EN y su tiempo frente al arranque del raíl de 3,3 V (MCU-04);
  - UART de programación (MCU-06) y LED de estado (MCU-07);
  - desacoplo del módulo y consumo de 3,3 V con los picos de WiFi; comprobación del TLV1117LV de `alimentacion.md` (corriente, disipación, caída con 5 V mínimos) (ALI-07);
  - **tabla de GPIO de toda la placa** (MCU-05): los pines que pide alimentación (VIN_SENSE, LIM_IMON, LIM_EN, LIM_FLT), los de las 6 salidas (IN e IS a ADC1 por canal y DEN común, DEC-0007; `estudio-salidas.md` S7), I²C del SHT4x y de la expansión (AMB-01, EXP-02), la entrada de EXP-01, el LED y el USB. Si no caben las entradas analógicas en ADC1, se proponen alternativas (multiplexar IS con DEN, mux analógico, etc.) con su coste;
  - estado de cada pin durante el arranque, el reset y el flasheo, y los *pull-down* que exige REL-04;
  - lista de piezas del bloque (referencia, valor, encapsulado, LCSC) y marca de las que necesitan símbolo o huella nuevos, con los datos de sus fichas en un anexo.
- Excluye:
  - crear símbolos, huellas o fichas, y editar KiCad;
  - cambiar requisitos: una cifra que no cuadre con `docs/02` se propone al coordinador.

## Entradas

- `docs/02-especificaciones-v2.md` (MCU-01…MCU-07, ALI-07, REL-04, REL-10, AMB-01, EXP-01, EXP-02).
- `docs/diseno/alimentacion.md` (raíl de 3,3 V, TPS2116, pines propuestos al MCU) y `docs/diseno/estudio-salidas.md` (S7, excitación del LED).
- Fichas `hardware/componentes/` (ESP32-S3-WROOM-1, USBLC6-2SC6, TYPE-C-31-M-12, SHT4x, BTT6050-1ERA, BTT6030-2ERA) y `datasheets/`.
- `hardware/v2/mcu.kicad_sch` (v1, solo lectura, como referencia; sin abrirla con el MCP: SPEC-0018 lo usa).
- Checklists `gestion/checklists/requisitos.md` y `esquema.md` (sección «Cálculos»).

## Entregables

- `docs/diseno/mcu.md`.
- Log `gestion/logs/SPEC-0020/01-ing-esquematicos.md` con el repaso de la checklist.

## Criterios de aceptación

- [x] Cada requisito MCU-01…MCU-07 tiene en el documento la pieza o el cálculo que lo cumple, con datasheet y página.
- [x] Tabla de GPIO completa: cada pin con su señal, bloque, dirección, ADC1 sí o no y estado en el arranque; cumple MCU-05 sin excepciones o las justifica.
- [x] Todas las entradas analógicas en ADC1, o una alternativa propuesta con coste para decisión del usuario.
- [x] Ninguna salida ni el limitador se activan durante el arranque, el reset o el flasheo (REL-04).
- [x] Presupuesto de 3,3 V con el pico de WiFi y margen frente al TLV1117LV, o cambio propuesto.
- [x] Lista de piezas con LCSC y stock, y marca de las que necesitan pieza nueva.

## Registro

| Fecha | Agente | Acción | Referencia |
|---|---|---|---|
| 2026-11-05 | coordinador | Crea la spec (propuesta) | |
| 2026-11-05 | coordinador | Abre la spec (aprobada por el usuario) | |
| 2026-11-06 | coordinador | DEN común a los 6 canales (usuario) | DEC-0007 |
| 2026-11-06 | coordinador | Cierra la spec; M de VAL-0020-01 corregida (C23–C26) y comprobada con Grep | VAL-0020-01 (APROBADO_CON_OBSERVACIONES) |
