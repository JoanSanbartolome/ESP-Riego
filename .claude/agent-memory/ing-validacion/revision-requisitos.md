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
- Fallos típicos de las protecciones escalonadas (VAL-0007-01, limitador común del bus de salidas):
  - un umbral con tolerancia («no actúa con 4 A» y «por debajo del límite de la fuente») deja una banda muerta. Una prueba de §6 «> 4 A» dentro de esa banda falla con un diseño correcto. Calculo la ventana: I_LIM,máx + lógica ≤ protección mínima de la fuente;
  - el límite de la fuente («de hasta 5 A») no está fijado como requisito: una fuente más pequeña invierte el orden de las protecciones;
  - el hueco entre la corriente de dimensionado de un canal (pista de 1 A) y el umbral de la protección siguiente (limitador de ≈ 4,5 A, *high-side* de 38 A): con IPC-2221, 4 A en una pista de 1 A dan ΔT ≈ 230 °C;
  - umbral de aviso igual al punto de prueba (16 V / 32 V);
  - cifras de la DEC distintas de las de docs/02 (REL-02: 36 V frente a 30 V).
- Fallos típicos al cerrar una ventana contra una fuente supuesta (VAL-0011-01, fuente LED de 5 A):
  - las fuentes conmutadas (MEAN WELL LRS) dan la sobrecarga en «% rated output power». En corriente, baja al subir el ajuste (a 25 V, 5,04 A). Recalculo la ventana en **todo** el rango de ajuste que admiten ALI-01 o la DEC, no solo a 24 V;
  - la carga resistiva (las válvulas) sube con V/R. Recalculo el total con la tensión máxima y la bobina fría. Si no cabe, el arreglo sin componentes es fijar el ajuste de la fuente como requisito de instalación;
  - los *drivers* LED de corriente constante (HLG: 95–108 %) no caben en una banda pensada para el 105 %: pido mirar la etiqueta real antes de elegir el limitador;
  - en las protecciones escalonadas también reviso el retorno GND, el fusible o PTC de entrada (con su reducción a 50 °C) y lo que hace el *high-side* (el BTT6050 se enclava y no se rearma solo);
  - márgenes de las pruebas de §6 frente a la precisión de la medida (31 V frente a 31,5 V = 1,6 %).
- Cuando una DEC sustituye la recomendación de un estudio de `docs/diseno/`, compruebo que alguna spec le pone un aviso. Busco términos obsoletos también en `.claude/agent-memory/` de los otros agentes.
- Cuando el usuario aclara un dato de entrada (tipo de carga, fuente), el commit suele tocar solo docs/02 y la DEC: busco el dato antiguo en las specs abiertas, como SPEC-0005 con «24 V AC (la instalada)».
- Con `python -I`, `PYTHONIOENCODING` se ignora: en el script uso `sys.stdout.reconfigure(encoding="utf-8")`.

Relacionado: [[comprobaciones-utiles]].
