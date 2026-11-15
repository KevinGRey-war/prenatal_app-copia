"""Voice review appended to the original survey's result screen."""
import streamlit as st

from feedback_examples import final_narration, final_parts, test_risk
from voice_feedback import hablar


def reset_attempt():
    st.session_state.answers = []


def show_survey_review(stage):
    rows = st.session_state.get("answers", [])
    if len(rows) != 10:
        return
    score = sum(row["correct"] for row in rows)
    st.subheader("🔊 Retroalimentación final")
    st.caption("Repaso de las diez preguntas con explicaciones y ejemplos. La clasificación es educativa, no un diagnóstico médico.")
    hablar(final_narration(rows, score, test_risk(score)), final_parts(rows, score, test_risk(score)))
    for number, row in enumerate(rows, 1):
        with st.expander(f"{'✅' if row['correct'] else '💡'} {number}. {row['question']}"):
            st.write("**Tu respuesta:**", row["selected"])
            st.write("**Respuesta correcta:**", row["answer"])
            st.write(row["feedback"])
            st.write(row.get("example", ""))
