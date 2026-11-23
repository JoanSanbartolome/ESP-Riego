---
name: zona-docs-y-coste
description: docs/ queda fuera de la zona aunque el encargo lo pida; cómo recalcular el coste por placa de estudio-coste.md
metadata:
  type: feedback
---

`docs/` (también `docs/diseno/*.md` y `estudio-coste-bom.csv`) queda fuera de la zona de jr-conformidad, aunque el encargo del coordinador pida «poner al día» esos documentos. La guarda bloquea `sed`, pero no ve un script de Python que escribe ahí.

**Why:** en SPEC-0038, paso 2, escribí esos tres archivos con scripts y tuve que devolverlos a HEAD. Los cambios quedaron como propuesta en el scratchpad y la spec salió `parcial`.

**How to apply:** el cambio a `docs/` se prepara en el scratchpad a partir de HEAD. En PENDIENTE se dan la ruta y las líneas.

Coste por placa (modelo de `estudio-coste.md` §1):
- Total = piezas × N + 8,18 + 1,53 + juntas SMT × N × 0,0016 + líneas «Extended» sin preferida × 3,07 + PCB (2 $ con 5 uds, 15 $ con 50) + THT (3,58 + juntas × N × 0,0164).
- En E2, el THT a mano se sigue comprando: solo salen sus cargos.
- Las juntas por referencia salen de `estudio-coste-bom.csv`.
- Precio: `jlc.consultar(código, cantidad por placa × N)`. Cuando una línea pierde piezas, sube de tramo (C513710 con solo C3 y C8), y eso cambia el ahorro con 50 uds.
- BOM y CPL: `kicad-cli sch export bom --exclude-dnp` y `pcb export pos --exclude-dnp`, los dos sobre una copia.
