"""Sequential spoken feedback. Only an ended queue unlocks the next activity."""
import base64
import hashlib
import json
import uuid
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from voice_feedback import clip_path


def show_tutor(cards, context, compact=False, overlay=False):
    if not cards:
        return False
    attempt = st.session_state.setdefault('tutor_attempt', uuid.uuid4().hex)
    token = hashlib.sha256((attempt + context + json.dumps(cards, ensure_ascii=False)).encode()).hexdigest()
    completed_key = 'review_finished_' + token
    if overlay and st.session_state.get(completed_key):
        st.success('Repaso terminado. Ya puedes continuar.')
        return True
    payload = []
    for card in cards:
        item = dict(card)
        path = clip_path(item['text'])
        if path.is_file():
            item['audio'] = base64.b64encode(path.read_bytes()).decode('ascii')
        payload.append(item)
    component = components.declare_component('prenatal_tutor', path=str(Path(__file__).parent / 'prenatal_tutor'))
    if overlay:
        st.markdown('''<style>
        .st-key-animated_review_overlay {position:fixed!important;inset:0;z-index:999990;
        background:rgba(43,26,48,.62);backdrop-filter:blur(7px);overflow:auto;
        padding:clamp(12px,4vh,40px) max(12px,calc((100vw - 1050px)/2));}
        .st-key-animated_review_overlay iframe {border-radius:28px;box-shadow:0 24px 80px #23142655;}
        </style>''', unsafe_allow_html=True)
        with st.container(key='animated_review_overlay'):
            result = component(cards=payload, token=token, compact=False, key='tutor_' + token, default=None)
    else:
        result = component(cards=payload, token=token, compact=compact, key='tutor_' + token, default=None)
    ready = isinstance(result, dict) and result.get('token') == token and result.get('completed') == len(cards)
    if overlay and ready:
        st.session_state[completed_key] = True
        st.rerun()
    return ready


def introduction():
    return {'title': 'Nia · Tu asistente de IA', 'text': 'Hola, soy Nia, tu asistente de inteligencia artificial de la aplicación prenatal. Te acompañaré a repasar lo aprendido, paso a paso. Soy una guía educativa y no sustituyo al personal de salud.'}
