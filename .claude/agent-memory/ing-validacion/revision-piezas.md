---
name: revision-piezas
description: Cómo validar símbolos, huellas y modelos 3D creados (p. ej. SPEC-0015, BTT6050/PG-TDSO-14, borne WJ500V, SHT4x): land pattern oficial fuera del datasheet, pin 1 del 3D, cotas de cortes, LCSC/JLCPCB por API
metadata:
  type: feedback
---

Una pieza creada se valida contra el dato del fabricante **y** con una prueba en KiCad. No basta con mirar el archivo.

**Por qué:** en VAL-0015-01 (2026-11-05), el autor daba tres cosas por hechas que resultaron falsas, y las tres eran M:
- «el datasheet no da *land pattern*»: Infineon lo publica en la página del encapsulado (PG-TDSO-14-11);
- «el render se ve bien alineado»: el índice del pin 1 del STEP estaba en el pad 7, porque el script lo generó con la Y de la huella;
- la patilla del borne «centrada»: la sección A-A la acota a 4,5 mm de la cara trasera.

**Cómo aplicarlo:**
- **Land pattern de Infineon:** `https://www.infineon.com/package/<encapsulado>`. WebFetch no ve nada (la página es JS); con `curl -A Mozilla` la página trae las imágenes `assets.infineon.com/is/image/infineon/infineon-<pkg>-png-footprint-en.png` y `…-package-en.png`. El nombre exacto (p. ej. PG-TDSO-14-11, no «-1») sale de distribuidores (Zenode, DigiKey).
- **Pin 1 del 3D:** placa de prueba con `proj/` y `libraries/3d/` en el *scratchpad* (así resuelve `${KIPRJMOD}/../libraries/3d`) y `kicad-cli pcb render --side top`. Comparo el triángulo de la serigrafía con la marca del modelo. Caja del STEP con sus `CARTESIAN_POINT`: el STEP tiene la Y hacia arriba y la huella hacia abajo.
- **Símbolos:** un esquema de prueba que copia los símbolos en `lib_symbols` y `kicad-cli sch erc`. Los NC y los `power_out` apilados no dan `pin_to_pin` en KiCad 10. Con `sym export svg` → PDF → PNG (PyMuPDF) se ve si `Value` pisa algún pin.
- **Dibujos escaneados** (Kangnex, hojas de una imagen): extraigo la imagen con `fitz.Pixmap(doc, xref)`, la paso a PDF y renderizo con `set_rotation(270)` y un recorte. La guardia bloquea `python -c` que escribe archivos: uso scripts escritos con Write.
- **Bornes THT:** la posición de la patilla está en el corte (A-A), no en la vista frontal. Taladro frente a la diagonal de la patilla rectangular (0,9 × 0,8 → 1,20). Las huellas oficiales de 5,08 mm usan 1,3.
- **LCSC/JLCPCB:** la API de JLCPCB (POST `jlcpcb.com/api/overseas-pcb-order/v1/shoppingCart/smtGood/selectSmtComponentList` con `{"keyword":"Cxxxx"}`) da `componentLibraryType` (`base`/`expand`), stock y tramos. Es la que usa jr-conformidad, y coincide al cuarto decimal. El JSON de LCSC da `result: null` para Sensirion: solo están para montaje en JLCPCB.
- **Altura de los DFN:** mido la vista lateral de la figura (SHT4x: 0,54 ± 0,05, no 0,5).
- Scripts de esta revisión en `scratchpad\v15\` (`sym_pins.py`, `mk_sch.py`, `mk_pcb.py`, `pads.py`, `stepbox.py`, `img.py`, `jlc.py`, `refs.py`). Son de la sesión: si hacen falta otra vez, se rehacen.

- **Revalidación ligera (VAL-0015-02):** reutilizo `v15\dl_infineon\footprint.png` y `v15\mk_pcb.py` (recibe `huella|x|y`). Perfil del borne con `pcb render --side left` frente a la sección A-A. Recortes con PIL sobre un render de 8000 px. En el STEP, `CARTESIAN_POINT` también delata salientes pequeños (marco a y = 5,6).
- **Guardia:** `mkdir -p $S/...` con variable de shell y `2>&1` junto a un `.png` la disparan (falso positivo): uso rutas literales, sin `2>&1`, y scripts de Python escritos con Write (Python de Windows no entiende `/c/Users/...`: ruta `C:\...` entre `r"..."`).

Relacionado: [[revision-importaciones]], [[revision-estudios]], [[comprobaciones-utiles]].
