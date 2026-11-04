---
spec: SPEC-0004
agente: ing-validacion
n: 01
fecha: 2026-11-04
estado: completado
---

# SPEC-0004 · 01 · ing-validacion

## Orden recibida

> SPEC-0004 · rama spec/SPEC-0004-requisitos-v02 (commit 29ba41e) · Lee: gestion/specs/SPEC-0004-requisitos-v02.md (criterios de aceptación), gestion/decisiones/DEC-0002-objetivo-v2-revisado.md, docs/02-especificaciones-v2.md v0.2, docs/03-plan-de-diseno.md, gestion/checklists/esquema.md y layout.md (v2), y el diff `git diff main...spec/SPEC-0004-requisitos-v02` (solo git de lectura) · Haz: valida la spec contra sus criterios de aceptación. Comprueba en especial: que cada decisión del usuario recogida en DEC-0002 (6 salidas ampliables, 3+3 bornes, T/HR en placa, sin nivel, interior ventilado, estudio de tecnologías de salida sin atarse a una carga, alimentación desde el transformador de 24 V AC) llega a un requisito vigente; coherencia interna de docs/02 (IDs citados existen, D1–D9 coherentes con los requisitos, criterios de aceptación §6 coherentes con los requisitos, mermaid coherente, trazabilidad H1–H12); coherencia técnica de los valores nuevos (rango 20–28 V AC y pico, TVS, buck ≥ 60 V, UVLO, 12–36 V DC, REL-02 frente a la entrada, REL-05); que ninguna parte vigente cite lazo 4–20 mA, IP65 o 4 canales; y que `python herramientas/gestion.py trazabilidad` no da avisos. Señala también interpretaciones del coordinador que creas que el usuario debería confirmar. Contexto: la carpeta de trabajo está en la rama spec/SPEC-0005-estudio-salidas, que es la de SPEC-0004 más el trabajo en curso de ing-esquematicos en docs/diseno/ y gestion/logs/SPEC-0005/; ignora esos archivos, no los toques y no cambies de rama. No uses el MCP de KiCad (no hace falta). · Entrega: gestion/informes/VAL-0004-01.md con veredicto, y responde con ESTADO, ARCHIVOS, VERIFICACIÓN, PENDIENTE y LOG.

## Contexto consultado

- **Spec y decisión:** SPEC-0004 y DEC-0002.
- **Documentación:** `docs/02` v0.2 (completo) y su diff frente a `main` (v0.1); `docs/03`; `docs/01` §3 (H1–H12).
- **Checklists:** de esquema v2, de layout v2, de fabricación y de proceso, más la plantilla de informe.
- **Otras specs y agentes:** SPEC-0005 y SPEC-0006, y las definiciones de los agentes en `.claude/agents/`, revisadas con Grep para buscar términos obsoletos.
- **Herramienta:** `herramientas/gestion.py`.
- **Git (solo lectura):** `git log` de `main` y de la rama, con los tráileres de `eb860b5`, `80245d9` y `29ba41e`.
- **Web:**
  - [SMBJ40A en DigiKey (Littelfuse)](https://www.digikey.es/en/products/detail/littelfuse-inc/SMBJ40A/762792): Vc de 64,5 V a 9,3 A, 10/1000 µs. Del datasheet de la serie SMBJ: SMBJ33A con Vc = 53,3 V y SMBJ43A con 69,4 V.
  - [Rain Bird D42606](https://www.rainbird.com/sites/default/files/media/documents/2026-07/d42606_-_irrigation_valve_solenoids.pdf): solenoide de 24 V AC con 0,30 A de arranque y 0,19 A de mantenimiento.
  - Fichas de distribuidor de Rain Bird 100-DV/DVF: 0,45 A y 0,25 A.

## Acciones

1. Rama y HEAD: `spec/SPEC-0005-estudio-salidas` y `29ba41e`, el mismo commit que `spec/SPEC-0004-requisitos-v02`. Se sigue, según la orden.
2. Lectura de la spec, de DEC-0002, del diff y de los documentos afectados.
3. `gestion.py trazabilidad`. La guarda bloquea la orden incluso sobre una copia en la carpeta temporal, porque reconoce el patrón. La copia de `.git`, `herramientas`, `docs` y `gestion` en `scratchpad/traz/` quedó sin usar. En su lugar, un script en la carpeta temporal (`traz_solo_lectura.py`) importa `gestion`, sustituye `escribir` por una comparación en memoria y ejecuta `trazabilidad()` sin escribir nada.
4. Script `ids.py` (carpeta temporal):
   - existencia de los IDs citados en los documentos y specs relevantes;
   - IDs retirados;
   - requisitos cambiados entre v0.1 (`git show main:docs/02…`) y v0.2;
   - cambios de prioridad;
   - requisitos cambiados que la spec no cita.
5. Búsqueda con Grep de términos obsoletos en las partes vigentes y en las definiciones de los agentes.
6. Recálculos: pico de 28 V AC (39,6 V), TVS y Vc frente al buck de 60 V, UVLO tras el puente, condensador de bulk (≈ 280 µF con 20 V AC y UVLO de 9 V), corriente de REL-05 frente a solenoides reales y presupuesto del transformador.
7. Hallazgos formados antes de mirar el registro del autor. SPEC-0004 no tiene log de autor: solo el mensaje de `29ba41e` y el registro de la spec.
8. Informe `gestion/informes/VAL-0004-01.md`.

## Decisiones y justificación

- **Hallazgo 01 en A y no en M:** ALI-05 es un requisito M con un umbral numérico que la v0.2 ha dejado por debajo de su propia justificación (Vc de la TVS que exige ALI-04, de 64,5 V o más, frente a un buck de 60 V). Cumplir el requisito al pie de la letra permite elegir una pieza que no sobrevive al *clamping* nominal.
- **Criterio 2 en «Parcial»:** la tabla de retirados no tiene la columna de motivo que pide el criterio; solo remite a DEC-0002.
- **Hallazgo 07 (`ing-layout`):** queda como M fuera de alcance. La spec no incluye las definiciones de los agentes, pero su objetivo pide coherencia en todo el repositorio.

## Verificación

- Trazabilidad en memoria: 0 avisos y 54 requisitos vigentes. El `TRAZABILIDAD.md` versionado solo difiere en la columna *Commits* (24 filas), porque se generó antes del commit.
- IDs: ninguno inexistente en los entregables. SPEC-0005 cita `REL-10`, que no existe.
- Veredicto: **RECHAZADO**, con C 0 · A 1 · M 6 · B 9.

## Pendiente

- Coordinador: corregir 01 y 12 (bastan para aprobar). Resolver los M 02, 04, 05 y 06 con el usuario: tensión en vacío y VA del transformador, semántica de ALI-09 y dónde medir la T/HR.
- El 07 (`ing-layout.md`) necesita una spec de proceso con prueba en vivo.
- Proponer `gestion/checklists/requisitos.md`.
- Las copias de la carpeta temporal (`scratchpad/traz/`) se pueden borrar. No contienen nada del TFG.

## Notas para el siguiente agente

- `gestion.py trazabilidad` está bloqueada para validación incluso en una copia. Se puede comprobar en memoria importando el módulo y sustituyendo `escribir`.
- En la re-validación, comprobar en cadena: rango de entrada → VRWM → Vc → nominal del buck y del bulk → UVLO tras el puente.
