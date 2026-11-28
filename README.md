# Vida Nueva - Cuidado Prenatal Inteligente

Aplicación educativa en Streamlit con preguntas por trimestre, retroalimentación inmediata, ranking local y panel administrativo protegido.

## Ejecutar localmente

1. Crea y activa un entorno virtual de Python.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. En Windows, ejecuta `run_app.bat`. El acceso administrativo usa el secreto
   `ADMIN_PASSWORD` cuando existe o el verificador seguro de respaldo.

La aplicación se abre en `http://127.0.0.1:8501`.

## Panel administrativo

El botón **Entrar al panel administrativo** aparece en la pantalla inicial y abre
la verificación en la misma pestaña. Después de validar la contraseña, el panel
permite consultar registros, revisar el ranking y descargar reportes en Excel,
CSV compatible con Excel y PDF. El panel usa la variable o secreto
`ADMIN_PASSWORD` cuando está configurada.

Para un despliegue en Streamlit, configura `ADMIN_PASSWORD` como secreto del servicio. No guardes contraseñas, bases de datos de participantes ni claves de Supabase en GitHub.

Puedes usar `.streamlit/secrets.toml.example` como guía de configuración, reemplazando todos los valores de ejemplo en el administrador de secretos del despliegue.

Mientras el secreto del despliegue no exista, el panel utiliza un verificador PBKDF2 de respaldo sin almacenar la contraseña original. Al configurar `ADMIN_PASSWORD`, el secreto de Streamlit reemplaza automáticamente ese acceso de respaldo.


## Ampliación de la encuesta en prenatal_app-copia

El inicio solicita únicamente el nombre de la persona. Después se abre un menú con dos tarjetas: Test de conocimientos sobre gestación y Cuidar una vida, paso a paso. La selección de etapa aparece al entrar al test; al volver al menú se conserva el nombre y cada nuevo test reinicia su puntaje y respuestas. Al seleccionar una respuesta y pulsar **VERIFICAR**, se marca la respuesta y se reproduce la corrección automáticamente, sin recuadro de explicación escrito; **CONTINUAR** avanza sin leer la siguiente pregunta; al terminar reproduce el repaso final. Al finalizar, todos los errores quedan desplegados con explicación y ejemplo, junto al repaso hablado completo.

El juego de `gestation_game/` recorre cinco etapas con eventos obstétricos: sangrado durante el embarazo, cefalea con visión borrosa, disminución de movimientos fetales, dificultad respiratoria con dolor torácico y sangrado posparto. No contiene un segundo cuestionario: se toca o arrastra una de nueve tarjetas hacia mamá. En cada etapa hay cinco acciones adecuadas y cuatro inadecuadas, con explicación automática por voz y repaso final. Los alimentos/bebidas se contextualizan como distracciones que no sustituyen la atención médica. Las señales no son exclusivas de la etapa donde aparecen. La ilustración muestra a mamá durante la gestación y con el bebé en brazos al finalizar, sin asociar complicaciones a culpa ni a puntajes. Las fuentes clínicas están enlazadas en el juego. Se mantienen pausa, música, teclado, persistencia, reinicio y los intervalos educativos: 0–4 errores sin riesgo educativo, 5–10 leve y 11 o más alto. El test independiente conserva su interfaz y preguntas.


Para comprobar también la lógica JavaScript del juego, instala Node.js y ejecuta las mismas pruebas Python; sin Node se omite esa prueba de desarrollo. El despliegue del juego no necesita Node ni servicios externos.

Se conserva el diseño original de la encuesta: logo, fondo, tarjetas, colores de respuesta, indicadores y navegación. El selector incorpora **Preparación para el parto** y **Posparto**, con diez preguntas cada uno, además de los tres trimestres originales. El nombre visible pasa a Cuidado Materno Infantil.

Cada error incluye explicación hablada y un ejemplo. Al terminar, se ofrece el repaso hablado de las diez preguntas y tarjetas desplegables con respuestas y ejemplos. Los audios MP3 en español están incluidos en `voice_assets/`; se insertan directamente en el reproductor para evitar fallos de la ruta `/media/` y no necesitan un servicio externo de voz. La voz se reproduce automáticamente al verificar, sin reproductor ni controles visibles; no se narran preguntas al iniciar o avanzar.

Las categorías aprobadas para el aprendizaje son 0–6 aciertos: riesgo educativo alto; 7–8: leve; 9–10: sin riesgo educativo. No son categorías clínicas ni descartan problemas de salud.

Validación: `python -m unittest discover -s tests -v`. Las pruebas comprueban conservación exacta de estilos y preguntas originales, cinco etapas, diez preguntas en cada sección nueva, explicaciones con ejemplos y audios completos.

Para regenerar los audios en Windows, se necesita una voz SAPI española e instalar `lameenc==1.9.0` solo para desarrollo; ejecutar `python scripts/build_voice_assets.py`. El despliegue no necesita Windows ni lameenc.

Esta ampliación se publica únicamente en `KevinGRey-war/prenatal_app-copia`. No modifica el repositorio ni el despliegue originales.


## Puntaje conjunto y nueva identidad visual

El menú y el juego usan la paleta de la pantalla de inicio y emblemas propios. Los personajes y alimentos ilustrados están en `gestation_game/assets/`, generados con la herramienta integrada ImageGen (procedencia y especificaciones en `ARTWORK.md`). Se conserva la transparencia y se animan mediante CSS; no se requieren servicios de generación durante el uso.

El ranking conjunto local guarda el mejor test (hasta 50 puntos) y la mejor precisión del juego (hasta 50 puntos). La precisión del juego es `100 × aciertos / elecciones realizadas`. Solo entran al ranking quienes completan ambas actividades; los resultados parciales se muestran al participante. Se incorporan los resultados locales anteriores del test sin borrarlos. El total no sustituye las categorías educativas: test 0–6 alto, 7–8 leve, 9–10 sin riesgo; juego 0–4 errores sin riesgo, 5–10 leve, 11+ alto. La tabla conjunta reside en la misma base SQLite; no se sincroniza con Supabase. Como el sistema existente, identifica al participante por nombre, por lo que personas con el mismo nombre comparten registro.

Al finalizar el juego se envía el historial al servidor, que comprueba etapas, duplicados y finalización y recalcula el puntaje. Las explicaciones de todos los errores se incluyen en el repaso visual y hablado. El test conserva sus preguntas, formato y audio automático originales.

### Recorrido obligatorio

Nombre → menú → test de 10 preguntas de la etapa elegida → repaso del test con voz → «CONTINUAR AL JUEGO» → cinco etapas del juego → repaso de errores con voz y ranking conjunto. La segunda tarjeta queda bloqueada hasta completar el test. El ranking no se presenta antes de terminar el juego. El resultado del recorrido actual se distingue del mejor resultado histórico del ranking. Cambiar de participante o iniciar otro test restablece el progreso del juego para evitar mezclar personas o intentos.

Ilustraciones maternas: `gestation_game/assets/maternal-stages-v3.png`; prompt y procedencia en `MATERNAL_ARTWORK.md`. Verificación de esta versión: 15 pruebas automatizadas, recorrido completo en navegador, clic/arrastre/teclado, repaso de cinco errores y puntaje conjunto; vista móvil de 390 píxeles sin desbordamiento horizontal.

## Test y juego complementarios
El menú distingue «Aprende y evalúa» y «Practica jugando», con contraste de colores, animación suave y adaptación móvil. Cada test mantiene diez preguntas: siete del banco original de la etapa seleccionada y tres obligatorias de eventos obstétricos (el evento de esa etapa, comunicación de síntomas y acompañamiento). `obstetric_questions.py` comparte los casos de `obstetric_learning.py`; una prueba comprueba que situación, respuesta y explicación coinciden con el juego. El banco original no se modifica. Antes de comenzar se ofrece una introducción breve con fuente clínica; se conserva la voz automática de corrección y repaso, con grabaciones incluidas para todas las nuevas respuestas. El juego continúa separado, sin cuestionario interno, después del test.

Verificación de esta revisión: 17 pruebas únicas aprobadas (suite de 16 más prueba de correspondencia añadida); audios completos, cuota 7+3, recorrido y puntajes. Menú revisado a 1280 y 390 píxeles, sin desbordamiento horizontal en móvil.


## Recorrido y presentación

Se restauraron los colores, botones, fondo y presentación del repaso del test anteriores al 22 de noviembre. Se conserva la corrección de contraste del encabezado desplegable. No se muestran las tarjetas ni el avatar añadidos ese día.

El flujo sigue siendo nombre → test → repaso → juego → repaso → ranking conjunto. La voz es automática y el avance permanece bloqueado hasta que termine. Los cambios visuales no alteran las preguntas, reglas educativas ni puntajes.

Validación: `python -m unittest discover -s tests -p "test_*.py"` y `node tests/test_tutor.cjs`.

## Ajuste del juego para escritorio y música del test

El tablero de escritorio usa dos columnas (animación y nueve tarjetas) y adapta su altura al espacio de la ventana; la distribución móvil anterior se conserva. Los encabezados de las tarjetas siguen disponibles mediante sus etiquetas accesibles. Las reglas educativas se consultan desde «Aprender sobre esta etapa» y las fuentes permanecen desplegables. En ventanas de muy poca altura o con ampliación del navegador puede ser necesario desplazarse para conservar la legibilidad.

El juego explica «Por qué» y «Ponlo en práctica» para cada acción, manteniendo la búsqueda de atención como prioridad. Sus iconos y logo materno utilizan ilustraciones SVG propias, con colores cálidos y trazos redondeados. Las preguntas del test no se cambian.

El test incorpora la melodía original «Jardín de vida», con preferencia independiente para silenciarla y pausa automática durante la retroalimentación. Si el navegador bloquea el sonido automático, aparece «Activar música».

Verificación de esta revisión: 19 pruebas Python y pruebas JavaScript de narración y música aprobadas. La revisión visual de escritorio y celular está pendiente: la apertura del navegador de pruebas quedó bloqueada por el límite de uso del sistema de aprobación automática. No se ha confirmado visualmente la ausencia de desplazamiento en esta revisión.

## Avatar del repaso conjunto final

Nia aparece únicamente después de completar el test y el juego, antes del ranking. Es un avatar femenino ilustrado de cuerpo completo, identificado como asistente de inteligencia artificial. El repaso usa las respuestas registradas: pregunta, elección, respuesta correcta, explicación y ejemplo del test; después, decisiones inadecuadas del juego. Si no hay errores, reconoce los aciertos sin inventar fallos.

La boca y los brazos acompañan los eventos de inicio, pausa y fin de la narración; los movimientos son ilustrativos y no constituyen sincronización fonética. Hay gestos suaves, parpadeo y respeto por la preferencia de movimiento reducido. La voz se inicia automáticamente y el ranking sigue bloqueado hasta terminar. La presentación del test y el tablero del juego permanecen iguales.

Verificación: 22 pruebas Python y pruebas JavaScript de narración y música aprobadas. La evaluación visual de la fluidez en el navegador sigue pendiente por el bloqueo de uso informado anteriormente.

## Repaso animado superpuesto (27 de noviembre)

Este comportamiento reemplaza las listas y desplegables de repaso descritos anteriormente. Al finalizar el test, Nia explica únicamente las respuestas incorrectas, una por una, con corrección, motivo y ejemplo. Después del juego, repasa los errores registrados en ambas actividades. Si no existen errores, ofrece una felicitación breve. El personaje ilustrado conserva los gestos de brazos y boca ligados al estado de la narración; no es sincronización fonética exacta.

El panel aparece sobre la pantalla y se retira al finalizar la narración. El avance permanece bloqueado hasta recibir la finalización de todas las explicaciones. Los puntajes y preguntas no cambian. Si el navegador bloquea el audio, aparece la opción de activarlo; no se simula una narración completada.

Verificado con 25 pruebas Python, la prueba JavaScript de narración secuencial y una vista aislada con datos ficticios en escritorio y 390 × 844. Las explicaciones de señales de alarma enlazan a CDC. Las capturas locales de la revisión están en `.test-data/repaso-animado.jpg` y `.test-data/repaso-movil.jpg` (no se publican datos de prueba).
