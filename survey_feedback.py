"""Voice review appended to the original survey's result screen."""
import streamlit as st

from feedback_examples import test_risk


def reset_attempt():
    st.session_state.answers = []
    st.session_state.update(pts=0, idx=0, resp=False, fb="", correcto=False,
                            respuesta_seleccionada=None, ranking_guardado=False)
    for key in list(st.session_state):
        if key.startswith("r_"):
            del st.session_state[key]


def show_survey_review(stage):
    from prenatal_tutor import show_tutor, introduction
    rows = st.session_state.get("answers", [])
    if len(rows) != 10:
        return False
    score = sum(row["correct"] for row in rows)
    st.subheader("Retroalimentación final")
    cards = [introduction()]
    for number, row in enumerate(rows, 1):
        if not row['correct']:
            cards.append({'title': f'Pregunta {number} · Vamos a reforzar',
                          'text': f"{row['question']}\nTu respuesta: {row['selected']}.\nRespuesta correcta: {row['answer']}.\n{row['feedback']} {row.get('example', '')}"})
    cards.append({'title': 'Repaso completado', 'text': f"Lograste {score} de 10 aciertos. {test_risk(score)}. Esta clasificación mide aprendizaje, no riesgo clínico. " + ('¡Todas tus respuestas fueron correctas! ' if score == 10 else 'Ahora puedes aplicar lo que acabas de repasar. ') + 'Continúa al juego cuando termine esta explicación.'})
    return show_tutor(cards, 'test-final')
