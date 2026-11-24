---
spec: SPEC-0039
agente: coordinador
n: 01
fecha: 2026-11-24
estado: completado
---

# SPEC-0039 · 01 · coordinador

## Hecho

- `superados.csv`: 23 términos (diff de `campos-*.csv` entre `v2.0-sch` y `main`, más DEC-0016 a DEC-0019). La columna `alcance` acota los que siguen vigentes en otras referencias (C513710 y 220n 100V en C3 y C8; C23162 fuera de R15; FAB-08 en `docs/02`).
- Frontmatter de los 19 DEC (`estado`, `modificada_por`) y `VIGENTES.md` (78 reglas). Plantilla `decision.md`, índice y «Registros» de `gestion/README.md` y `CLAUDE.md` apuntan a `VIGENTES.md`.
- `docs/02` v0.9: D5 y D6 según DEC-0019, con su línea en el historial. `docs/03`: fase 4 según DEC-0019, con la colocación en texto y el estudio de coste marcados.
- `gestion.py`: `integrar` deja el trailer `Agent-Id` y cuenta solo lo posterior a ese commit (también `registrar`); orden `comprobar` (`VIGENTES.md` y memorias). Pruebas G07, G08, K01–K04.
- `guardia.py`: lee el script de `python`/`node` que se ejecuta y bloquea las escrituras en rutas literales fuera de la zona. Pruebas Z01–Z04 en `test_gestion.py`.
- Memoria del coordinador (fuera del repositorio): 3 → 2 archivos, 20 afirmaciones; `memoria-coordinador.csv`.

## Decisiones y desviaciones

- **DEC-0020 (nuevo).** Leer los scripts contradice M9 de DEC-0009 («la guarda no se endurece más») y el «Límites conocidos» del manual, donde el usuario decidió el 2026-11-18 no cambiar la guarda. Lo registro como DEC aceptado por el usuario al mandar ejecutar SPEC-0039; DEC-0009 pasa a `modificada_por: [DEC-0010, DEC-0019, DEC-0020]`. El código en línea sigue sin analizarse (M9).
- Caso de VAL-0038-01-04 (auditoría del 2026-11-23, instancia ab5487, 16:42:31): `cd <scratchpad> && PYTHONUTF8=1 python -I estudio.py`, con `Path(r'C:/…/docs/diseno/estudio-coste.md').write_text(…)`.
- Ningún DEC queda `sustituido`: todos conservan alguna regla. Modificados: 0001, 0002, 0003, 0004, 0005, 0008, 0009, 0011, 0012 y 0016.
- La forma de las viñetas («… Por qué: … Fuente: …») y la ausencia de fechas relativas también las comprueba `comprobar`.

## Verificación

- `test_gestion.py` 38/38, `test_guardia.py` 270/273 (los 3 de `LIMITES`, que no fallan), `test_commit_msg.py` 26/26. `comprobar`: `VIGENTES.md` sin incidencias; memoria del coordinador sin incidencias; las de los agentes, pendientes de los pasos 2–4.

## Pendiente

- Ninguno. El push de `main` tras cada merge sigue sin DEC: el usuario no lo considera necesario (2026-11-24).
