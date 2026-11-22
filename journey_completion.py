"""Guided game review before the combined ranking."""
import streamlit as st
from prenatal_tutor import show_tutor


def show_game_review():
    rows = st.session_state.get('game_review')
    st.subheader('Retroalimentación del juego')
    if not rows:
        st.error('No se recuperó el detalle del juego. No podemos confirmar sus respuestas todavía.')
        return False
    mistakes = [row for row in rows if not row['good']]
    count = len(mistakes)
    risk = 'Riesgo educativo alto' if count >= 11 else 'Riesgo educativo leve' if count >= 5 else 'Sin riesgo educativo'
    cards = [{'title': 'Nia · Repasemos el juego', 'text': f'Completaste las cinco etapas. Vamos a reforzar tus decisiones. Registraste {count} errores. {risk}. Esta categoría mide aprendizaje, no la salud de mamá ni del bebé.'}]
    for row in mistakes:
        cards.append({'title': row['stage'] + ' · ' + row['name'], 'text': row['explanation']})
    cards.append({'title': '¡Felicitaciones por tu aprendizaje!', 'text': ('Todas tus elecciones fueron adecuadas. ' if not mistakes else 'Cada error es una oportunidad para aprender. ') + 'Practicaste cómo reconocer señales de alarma y buscar ayuda. Las complicaciones no son culpa de la madre ni dependen de los puntos. Ahora puedes consultar tu puntaje conjunto.'})
    return show_tutor(cards, 'game-final')
