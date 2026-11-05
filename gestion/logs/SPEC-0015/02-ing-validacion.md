---
spec: SPEC-0015
agente: ing-validacion
n: 02
fecha: 2026-11-05
estado: completado
---

# SPEC-0015 · 02 · ing-validacion

## Orden recibida

SPEC-0015 · rama `spec/SPEC-0015-recopilacion-componentes` · commit `8503def` (base `bf917f9`). Validar criterio a criterio. Lo principal es la sección «Requiere verificación de validación»:

- los símbolos BTT6050-1ERA, BTT6030-2ERA y BSP752R, y su mapeo con la huella;
- la huella PG-TDSO-14, frente al encapsulado y a un posible *land pattern* oficial de Infineon;
- la huella WJ500V;
- los modelos 3D propios, el SHT4x (altura) y el USB-C de los demos.

Además: las referencias a la librería oficial, las rutas absolutas, LCSC (al menos 4 muestras), los datasheets (oficiales y ≤ 5 MB), que no cambien `hardware/v2`, la v1 ni el TFG, y que el MCP no haya cargado ningún proyecto.

## Protocolo

- Rama: `spec/SPEC-0015-recopilacion-componentes` (`git branch --show-current`). Commit revisado: `8503def`.
- Orden de independencia: spec, decisiones y checklist → artefactos y pruebas → hallazgos → log del autor (leído al final).
- MCP: solo `get_jlcpcb_part` (consulta). Sin `open_project`. `kicad-cli` solo sobre archivos de prueba en `…\scratchpad\v15\`. Git, solo para leer.

## Acciones

1. `git diff --stat bf917f9 8503def`: 31 altas; ninguna en `hardware/v2` ni en `hardware/v1-tfg`. `integridad_tfg.py verificar`: «TFG intacto: 337 archivos».
2. Referencias oficiales (`refs.py`): 16 símbolos y 8 huellas existen en KiCad 10.0.6. Faltan 2 modelos 3D oficiales (USB-C HRO y SHT4x), como declaran las fichas.
3. Símbolos (`sym_pins.py`) frente a la Tabla 2 de la p. 4 del BTT6050 y del BTT6030 (texto) y a la p. 2 del BSP752R (imagen): todos los pines coinciden en número, nombre y tipo. ERC de un esquema de prueba (`mk_sch.py`): sin conflictos por los pines apilados.
4. PG-TDSO-14:
   - Figura 53, p. 49, renderizada.
   - Página de Infineon del encapsulado PG-TDSO-14-11: tiene el *mounting footprint* oficial (pads de 0,65 × 1,34, filas a 5,46 mm, EP de 2,65 × 6,4 y pasta de 2 × 2,95 × 2,45). Es el mismo dibujo de encapsulado que la Figura 53.
   - Cálculo IPC-7351B nominal propio: Z = 6,92, G = 3,55, X ≈ 0,56.
5. WJ500V: imagen del dibujo extraída y rotada (`img.py`). La sección A-A da la patilla a 4,50 ± 0,20 de la cara trasera, no centrada.
6. Modelos 3D:
   - Caja envolvente con `stepbox.py`.
   - PCB de prueba con la estructura `proj/` + `libraries/3d/` (`mk_pcb.py`), `pcb render` desde arriba y de frente, y DRC.
   - El índice del pin 1 del TDSO-14 sale en el pad 7.
   - El SHT4x mide 0,5 de alto frente a 0,54 ± 0,05 (Figura 15, p. 14).
   - El USB-C es idéntico (`cmp`) al de la demo, y la huella de la demo tiene los mismos pads que la oficial.
7. LCSC y JLCPCB:
   - 13 códigos consultados con la API de JLCPCB (`jlc.py`): tipo y tramos coinciden con las fichas, y recalculé los precios a 5 y 10 placas.
   - El JSON y la ficha web de LCSC no encuentran los códigos de Sensirion.
   - Ninguna alternativa Basic ni Preferred para SMBJ33A, USBLC6 ni el USB-C de 16 pines.
8. Comprobaciones complementarias: pinouts del TPS2663 (Tabla 5-1 del PDF de TI, descargado al *scratchpad*) y del LM5069 (p. 3); V_IN(T+) del BSP752R (p. 6). Comprobé también la API de EasyEDA (403, como dice el autor).
9. Auditoría del 2026-11-05: jr-conformidad, con las líneas etiquetadas con la rama de SPEC-0014, no cargó ningún proyecto. Los `open_project` son de ing-layout.
10. Log del autor contrastado:
    - afirma que no hay *land pattern* de Infineon, y sí lo hay (01);
    - afirma que el render muestra el modelo «bien alineado», y la marca del pin 1 está en el pad 7 (02);
    - supone la patilla del borne centrada, y está a 4,5 mm de la cara trasera (03).

## Resultado

- Informe: `gestion/informes/VAL-0015-01.md`.
- Veredicto: **APROBADO_CON_OBSERVACIONES**.
- Hallazgos: C 0 · A 0 · M 3 · B 7.
  - M 01: *land pattern* oficial de Infineon PG-TDSO-14-11.
  - M 02: índice del pin 1 del 3D del TDSO-14 en el pad 7.
  - M 03: WJ500V con el cuerpo desplazado 0,5 mm.
  - B 04–10: pin 1 del borne, 3D del SHT4x, precio del borne, fuente de datos del BSP752R, URL de los datasheets, taladro de 1,2 y cosmética de los símbolos.
- 6 propuestas para la checklist de librerías.

## Pendiente

- Las M conviene corregirlas antes de que una spec de bloque coloque el BTT6050 o los bornes en la PCB.
- Las specs de los bloques MCU y de sensores deben enlazar los 3D de respaldo del USB-C y del SHT4x.
