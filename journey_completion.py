"""Guided game review before the combined ranking."""
import streamlit as st
from prenatal_tutor import show_tutor
from final_review import review_cards


def show_game_review():
    rows = st.session_state.get('game_review')
    st.subheader('Repaso final · Test y juego')
    cards = review_cards(st.session_state.get('answers', []), rows)
    if not cards:
        st.error('No se recuperaron todas las respuestas de las dos actividades. No podemos preparar el repaso todavía.')
        return False
    return show_tutor(cards, 'combined-final', compact=False, overlay=True)
