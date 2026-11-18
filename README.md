# Cajón flamenco · Cuaderno de ejercicios (BARRI)

App para practicar el cajón con los ejercicios del cuaderno: partitura, sonido, tapa del cajón animada y metrónomo.

## Prototipo (fase 1)

- Se edita `src/app.html`; `python3 build.py` genera `index.html` (se abre tal cual en el navegador).
- Ejercicios como datos (`EJ` en el script): cada golpe es la letra del sonido (`g` grave, `a` agudo, `p` platillo,
  `c` caja, `f` fantasma), la mano (`D`/`I`) y `^` si lleva acento; `-` es silencio. `compas` = pulsos por compás,
  `sub` = golpes por pulso (1 negra, 2 corchea, 3 tresillo, 4 semicorchea).
- Metrónomo con el audio del navegador (se programa por delante, preciso), acentos de la soleá en el compás de 12,
  cuenta de entrada, huecos de silencio y subida automática de tempo.
- Escalera de tempo guardada en el navegador.
- Niveles: en el prototipo se simulan con «Entrar como».

## Siguientes fases

1. Transcribir todo el cuaderno (rumbas, tangos, bulerías, sevillanas, chirigota, rellenos, lectura a primera vista…) y editor de ejercicios.
2. Inicio de sesión y niveles de verdad (ejercicios en el servidor, con reglas por nivel), panel del profesor y tarea semanal.
3. Sonidos grabados de un cajón real.
4. Escuchar al alumno por el micrófono para medir el ritmo.
