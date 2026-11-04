---
name: revision-requisitos
description: Cómo validar specs que cambian docs/02 (requisitos) en ESP-Riego: trazabilidad sin escribir, comparación v_anterior/v_nueva, fallos típicos en cadena (entrada → TVS → polaridad → buck → UVLO → presupuesto) y aclaraciones del usuario que no llegan a las specs abiertas
metadata:
  type: feedback
---

Para validar una spec de requisitos (`docs/02`), no basta con buscar términos: hay que recalcular **en cadena** los valores que dependen unos de otros.

**Por qué:** en VAL-0004-01 (2026-11-04), la v0.2 cambió la entrada a 24 V AC (28 V AC, pico de 39,6 V), pero dejó el buck de VIN ≥ 60 V de la v0.1, que estaba pensado para la SMBJ33A (Vc = 53,3 V). La TVS nueva (SMBJ40A) tiene Vc = 64,5 V: el resultado fue un hallazgo A. El UVLO también estaba referido a la entrada y no a la tensión tras el puente (−2·Vf). Y un criterio de §6 pedía que la placa informara de la pérdida de su única fuente de alimentación.

**Cómo aplicarlo:**
- Cadena que reviso: tensión máxima de entrada (tolerancia de red +10 % y tensión en vacío del transformador) → VRWM de la TVS → Vc → tensión nominal del buck, del bulk y de las piezas del nodo. UVLO ≤ mínimo DC − puente − fusible.
- Compruebo que cada criterio de §6 se puede verificar con la arquitectura de alimentación descrita.
- Compruebo el presupuesto de la fuente frente a las cargas simultáneas.
- `gestion.py trazabilidad` está bloqueada para mí, incluso en una copia. La ejecuto en memoria: importo `gestion` desde la carpeta temporal, sustituyo `gestion.escribir` y comparo con el `TRAZABILIDAD.md` versionado. La columna *Commits* siempre difiere en el commit que la generó, y es normal.
- Comparo las tablas de `git show main:docs/02…` con las actuales: IDs cambiados, prioridades cambiadas, IDs que la spec no cita y lista de redefiniciones de §9.
- Busco términos obsoletos también en `.claude/agents/*.md` (en VAL-0004-01, `ing-layout.md` seguía pidiendo «conectores en un borde» y «anclajes DIN») y en las specs hijas (`REL-10` inexistente en SPEC-0005).
- Más fallos típicos de la cadena (VAL-0004-02, entrada de 24 V DC):
  - TVS unidireccional sin orden fijado frente a la protección de polaridad: incumple «polaridad invertida sin daños»;
  - un límite global (4 A en las salidas) sin mecanismo ni prueba;
  - puntos de prueba de §6 fuera de la ventana UVLO–VRWM;
  - VRWM ≥ Vmáx sin margen frente a la OVP de la fuente;
  - una prueba térmica «repartida» que no comprueba la corriente por canal.
- Cuando el usuario aclara un dato de entrada (tipo de carga, fuente), el commit suele tocar solo docs/02 y la DEC: busco el dato antiguo en las specs abiertas, como SPEC-0005 con «24 V AC (la instalada)».
- Con `python -I`, `PYTHONIOENCODING` se ignora: en el script uso `sys.stdout.reconfigure(encoding="utf-8")`.

Relacionado: [[comprobaciones-utiles]].
