---
name: revision-calculos
description: Fallos de cálculo y de coherencia entre documentos que no recogen las checklists (huecos con Vc, tolerancias, ADC, costes, I²C, referencias, requisitos retirados)
metadata:
  type: feedback
---

- Huecos y puentes entre redes se calculan con la tensión de *clamping* (Vc), no con la continua. Por qué: fue el hallazgo VAL-0017-01-01. Fuente: VAL-0017-01.
- Tolerancias que el datasheet da solo en puntos (TPS2663: I_OL a 3, 4,02, 9 y 30 kΩ): se mira cómo las lleva el autor a la R elegida. Por qué: tomarlas sin interpolar ni acotar fue un fallo. Fuente: VAL-0017-01.
- Un filtro RC al ADC se compara con la condición de medida del datasheet (ESP32-S3: 100 nF en el pin). Por qué: otro filtro cambia el error. Fuente: VAL-0017-01.
- Costes: se reconstruye la lista por canal o por variante hasta cuadrar al céntimo; sin lista por variante, los totales solo se aproximan. Por qué: los totales ocultan piezas olvidadas. Fuente: VAL-0005-01, VAL-0006-01.
- Protección de salidas: además de lo de la checklist, si el diagnóstico sigue vivo con V_S colapsada (subtensión) y cuánto tarda el firmware en reaccionar. Por qué: el bus cae para todos los canales. Fuente: VAL-0005-01.
- Estudio con conector: térmica en fallo solo con el buck (falta el USB a 5,25 V), margen de I²C en un solo sentido y señales activas a nivel bajo colgadas de una línea con *pull-down* (OE del 74HC595). Por qué: salieron en VAL-0006-01. Fuente: VAL-0006-01.
- Caída en una resistencia serie de I²C: si el *pull-up* está en el lado del conector, el receptor no ve caída. Por qué: mi 0,25 V era 0,40 V. Fuente: VAL-0006-02.
- Inversores con 2N7002 a ≈ 2,4 V de puerta no conmutan con garantía (V_GS(th) máx. 2,1–2,5 V). Por qué: es un ejemplo habitual de los estudios. Fuente: VAL-0006-01.
- Fuentes LED de corriente constante (HLG: 95–108 %) no caben en una banda pensada para el 105 %, y una banda más estrecha de lo necesario deja fuera piezas (*hot-swap* de ± 12 %). Por qué: la protección de la fuente depende del modelo. Fuente: VAL-0011-01, VAL-0011-02.
- X5R de ± 20 %: la tolerancia se aplica además de la polarización, también en la τ de la red RC de EN. Por qué: el *derating* de la checklist solo nombra tensión y temperatura. Fuente: VAL-0020-01.
- Referencias provisionales o «libres» de una spec: se cruzan con los otros `docs/diseno/*.md` del HEAD tras traer `main` y con la netlist. Por qué: C22 y C46 estaban en uso. Fuente: VAL-0020-01, VAL-0029-01.
- Las fichas de jr-conformidad con «símbolo pendiente», el README de `hardware/v2` tras un paso de layout y las cifras de las notas de la raíz (BUS_24V ≠ 5,1 A de entrada) no se actualizan solas: se cotejan con `docs/diseno`. Por qué: ninguna spec las lista. Fuente: VAL-0022-01, VAL-0031-01, VAL-0032-01.
- Tabla de GPIO: se mapea U5 por `pinfunction` `IOn_pin` en la netlist, con los alias `USB_D-`, `USB_D+`, `TXD0` y `RXD0` = 19, 20, 43 y 44, y se compara pin, red y otros pines fila a fila. Por qué: esos cuatro no llevan número de GPIO. Fuente: VAL-0032-01.
- Si el coordinador hace commits en la rama durante la revisión (una DEC, un cambio de prioridad), se valida contra el último y se cita ese HEAD. Por qué: el informe tiene que citar el commit revisado. Fuente: VAL-0020-01, VAL-0030-01.
- Requisitos que retiran un ID: se comprueba cada sección que el historial dice haber cambiado y los recuentos derivados («3 libres», «GPIO35–37»); un ID retirado sigue siendo conocido para `gestion.py` y `commit_msg.py`, y SPEC-NNNN solo va en §10 de `docs/02`. Por qué: §9 afirmaba un cambio en §2 que no estaba. Fuente: VAL-0030-01; `herramientas/gestion.py` (`leer_retirados`).
