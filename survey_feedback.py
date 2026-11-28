"""Voice review appended to the original survey's result screen."""
import streamlit as st



def reset_attempt():
    st.session_state.answers = []
    st.session_state.update(pts=0, idx=0, resp=False, fb="", correcto=False,
                            respuesta_seleccionada=None, ranking_guardado=False)
    for key in list(st.session_state):
        if key.startswith("r_"):
            del st.session_state[key]


def show_survey_review(stage):
    from prenatal_tutor import show_tutor
    from final_review import survey_cards
    rows = st.session_state.get("answers", [])
    if len(rows) != 10:
        return False
    st.subheader("Retroalimentación final")
    st.caption("Nia explica solo los errores, uno por uno, con ejemplos para la vida diaria.")
    return show_tutor(survey_cards(rows), 'test-errors-final', compact=False, overlay=True)
