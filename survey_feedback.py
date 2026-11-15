"""Voice review appended to the original survey's result screen."""
import streamlit as st

from feedback_examples import final_narration, final_parts, test_risk
from voice_feedback import hablar


def reset_attempt():
    st.session_state.answers = []
    st.session_state.update(pts=0, idx=0, resp=False, fb="", correcto=False,
                            respuesta_seleccionada=None, ranking_guardado=False)
    for key in list(st.session_state):
        if key.startswith("r_"):
            del st.session_state[key]


def show_survey_review(stage):
    rows = st.session_state.get("answers", [])
    if len(rows) != 10:
        return
    score = sum(row["correct"] for row in rows)
    st.subheader("🔊 Retroalimentación final")
    if score < 10:
        st.write(f"**Preguntas por reforzar: {10 - score}.** Cada error aparece abierto abajo con la respuesta correcta, su explicación y un ejemplo.")
    else:
        st.success("¡Todas las respuestas son correctas! Puedes escuchar el repaso completo.")
    st.caption("Repaso de las diez preguntas con explicaciones y ejemplos. La clasificación es educativa, no un diagnóstico médico.")
    hablar(final_narration(rows, score, test_risk(score)), final_parts(rows, score, test_risk(score)))
    for number, row in enumerate(rows, 1):
        with st.expander(f"{'✅' if row['correct'] else '💡'} {number}. {row['question']}", expanded=not row["correct"]):
            st.write("**Tu respuesta:**", row["selected"])
            st.write("**Respuesta correcta:**", row["answer"])
            st.write(row["feedback"])
            st.write(row.get("example", ""))
