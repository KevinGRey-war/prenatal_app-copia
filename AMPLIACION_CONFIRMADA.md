# Próxima ampliación confirmada — alimentación y emergencias obstétricas

Solicitud confirmada: combinar ambos temas, sin sustituir la encuesta original ni cambiar su interfaz.

- Mantener nombre → test → retroalimentación → juego → retroalimentación y puntaje conjunto.
- Conservar las cinco etapas y los intervalos de riesgo EDUCATIVO existentes.
- Añadir situaciones de alarma y decisiones seguras en cada etapa; toda respuesta errada debe explicar por qué y cuál es la acción adecuada, con voz automática.
- Representar a la misma mamá durante el embarazo, con evolución de la pancita y del bebé de forma ilustrativa; finalizar con mamá y bebé en brazos.
- Felicitar por el aprendizaje y la búsqueda oportuna de ayuda; nunca prometer un parto sano por puntos ni atribuir complicaciones a culpa de la madre.
- No usar alimentos como tratamiento de emergencias. Ante señales de alarma, atención médica inmediata.
- Verificar persistencia, reinicio, bloqueo de etapas, puntaje conjunto, voz y vista móvil/escritorio antes de presentar la aplicación.

Fuente clínica inicial: https://www.cdc.gov/hearher/maternal-warning-signs/index.html

Estado: alcance confirmado; implementación y verificación en curso. La versión anterior funcional permanece en el commit 9270a3c.

## Ajuste confirmado el 20 de noviembre
El juego ya NO lleva un cuestionario interno ni se centra en alimentar. Se convierte en acciones interactivas sobre eventos obstétricos. Las opciones de alimentos/bebidas quedan contextualizadas como distracciones que no sustituyen atención médica. El test independiente se conserva intacto. Mantener la mamá por etapas, el cierre con bebé en brazos, voz automática, riesgos educativos y ranking conjunto. Estado: implementación local en curso; pendiente prueba visual final y publicación de esta ampliación.

## Resultado verificado
Implementación final: eventos obstétricos mediante tarjetas interactivas, sin cuestionario interno; 25 aciertos posibles en cinco etapas. Test original intacto y ranking conjunto comprobado (test 20/100 + juego 83,33/100 = 51,7/100). Pasaron 15 pruebas. Clic, arrastre real y teclado verificados; cierre con mamá y bebé revisado en móvil sin desbordamiento. Pendiente únicamente guardar esta revisión en GitHub.
