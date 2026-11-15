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

El inicio solicita únicamente el nombre de la persona. Después se abre un menú con dos tarjetas: Test de conocimientos sobre gestación y Aprende a dar de comer a tu bebé. La selección de etapa aparece al entrar al test; al volver al menú se conserva el nombre y cada nuevo test reinicia su puntaje y respuestas. El juego tiene una entrada independiente reservada para su próxima implementación. Solo el test muestra el selector de las cinco etapas. Al seleccionar una respuesta y pulsar **SIGUIENTE**, aparece la corrección y su audio; **CONTINUAR** avanza a la siguiente pregunta. Al finalizar, todos los errores quedan desplegados con explicación y ejemplo, junto al repaso hablado completo.

Se conserva el diseño original de la encuesta: logo, fondo, tarjetas, colores de respuesta, indicadores y navegación. El selector incorpora **Preparación para el parto** y **Posparto**, con diez preguntas cada uno, además de los tres trimestres originales. El nombre visible pasa a Cuidado Materno Infantil.

Cada error incluye explicación hablada y un ejemplo. Al terminar, se ofrece el repaso hablado de las diez preguntas y tarjetas desplegables con respuestas y ejemplos. Los audios MP3 en español están incluidos en `voice_assets/`; no necesitan un servicio externo de voz. Si el navegador bloquea el inicio automático, pulsa Reproducir en el control de audio.

Las categorías aprobadas para el aprendizaje son 0–6 aciertos: riesgo educativo alto; 7–8: leve; 9–10: sin riesgo educativo. No son categorías clínicas ni descartan problemas de salud.

Validación: `python -m unittest discover -s tests -v`. Las pruebas comprueban conservación exacta de estilos y preguntas originales, cinco etapas, diez preguntas en cada sección nueva, explicaciones con ejemplos y audios completos.

Para regenerar los audios en Windows, se necesita una voz SAPI española e instalar `lameenc==1.9.0` solo para desarrollo; ejecutar `python scripts/build_voice_assets.py`. El despliegue no necesita Windows ni lameenc.

Esta ampliación se publica únicamente en `KevinGRey-war/prenatal_app-copia`. No modifica el repositorio ni el despliegue originales.
