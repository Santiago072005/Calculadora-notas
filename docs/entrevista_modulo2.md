# Entrevista a una usuaria de la calculadora de nota final

**Fecha:** 2026-11-26
**Duración aproximada:** 6 minutos
**Entrevistadora:** Erik Marroquinal (autor del proyecto)
**Persona entrevistada:** una prima del autor, estudiante de Dibujo Arquitectónico en el SENA. Es una persona real; no se registra su nombre.
**Autorización para usar sus respuestas en el informe, sin su nombre:** <mark>PENDIENTE: confirmar que la persona aceptó</mark>
**Cuándo se hizo:** después de construir el proyecto. Sirve para contrastar los requisitos con una usuaria real, no los originó (los requisitos salen de la propuesta del módulo 1). Es una sola persona, así que no es una muestra representativa.

Las respuestas están copiadas tal como las dio, sin cambios.

## Preguntas y respuestas

**1. ¿Cómo calculas hoy tu nota final de una materia?**
Yo normalmente utilizo la calculadora del celular. Multiplico cada nota por el porcentaje que vale y después sumo los resultados para saber cuánto llevo en la materia.

**2. ¿Qué es lo que más te confunde cuando cada evaluación pesa un porcentaje distinto?**
A veces me confundo al calcular cuánto vale cada evaluación, porque unas actividades tienen más porcentaje que otras. También me cuesta recordar si los porcentajes suman el 100 %.

**3. ¿Te ha pasado que la nota que calculaste no era la que te puso el docente? Cuéntame qué pasó.**
Sí, una vez calculé que mi nota final era más alta de lo que realmente me puso el profesor. Después me di cuenta de que había multiplicado mal uno de los porcentajes y por eso el resultado fue diferente.

**4. ¿Alguna vez se te olvidó incluir una nota o un porcentaje? ¿Qué pasó?**
Sí, una vez olvidé incluir la nota de un trabajo. Cuando revisé el resultado, me di cuenta de que no coincidía con el que tenía el profesor. Tuve que volver a hacer todas las operaciones.

**5. Si el programa te avisa de un error, ¿en qué casos te gustaría que te avisara?**
Me gustaría que me avisara cuando los porcentajes no sumen el 100 %, cuando escriba una nota mayor a 5 o cuando deje algún espacio sin completar. Así podría corregir los errores antes de obtener el resultado.

**6. ¿Cómo escribes los decimales: con coma o con punto? ¿Con cuántos decimales ves tu nota?**
Normalmente utilizo el punto para escribir los decimales. Me gusta ver las notas con dos decimales, por ejemplo, 4.25, porque así puedo tener un resultado más preciso.

**7. ¿Te serviría ver cuánto aporta cada nota a la nota final? ¿Para qué?**
Sí, me serviría bastante porque así podría saber cuánto aporta cada evaluación y cuáles tienen más importancia. También podría saber qué nota necesito sacar en las siguientes actividades para aprobar la materia.

**8. ¿Dónde lo usarías: en el celular, en el computador, en la consola? ¿Necesitas que funcione sin internet?**
Lo usaría principalmente en el celular porque es el dispositivo que más utilizo y lo tengo casi siempre a la mano. También sería bueno poder usarlo en el computador. Me gustaría que funcionara sin internet para poder calcular mis notas en cualquier momento.

## Qué dice la entrevista frente a los requisitos

| Respuesta | Requisito relacionado | Resultado |
|---|---|---|
| 1, 2, 3 y 4 | N-01 y N-02 (equivocarse al calcular a mano; olvidar un porcentaje o una nota) | Confirma el problema con un caso real: multiplicó mal un porcentaje y olvidó una nota |
| 5 | HU-02 (porcentajes que no suman 100), HU-03 (nota mayor que 5) y un espacio sin completar | Cubierto: la consola vuelve a preguntar si el dato está vacío o no es un número |
| 6 | Decimales y redondeo | Coincide: ve 2 decimales con punto; el programa redondea a 2 y también acepta coma |
| 7 | HU-04 (aporte de cada nota) | Confirma la necesidad. Además pide saber qué nota necesita sacar para aprobar: no está construido |
| 8 | P-01 y RNF-03 (sin internet) | Sin internet: respaldado por una usuaria. Celular: la usaría sobre todo en el celular y la consola no corre ahí; queda como limitación |
