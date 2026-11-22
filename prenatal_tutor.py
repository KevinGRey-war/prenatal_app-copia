"""Sequential spoken feedback. Only an ended queue unlocks the next activity."""
import base64
import hashlib
import json
import uuid
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from voice_feedback import clip_path


def show_tutor(cards, context, compact=False):
    if not cards:
        return False
    attempt = st.session_state.setdefault('tutor_attempt', uuid.uuid4().hex)
    token = hashlib.sha256((attempt + context + json.dumps(cards, ensure_ascii=False)).encode()).hexdigest()
    payload = []
    for card in cards:
        item = dict(card)
        path = clip_path(item['text'])
        if path.is_file():
            item['audio'] = base64.b64encode(path.read_bytes()).decode('ascii')
        payload.append(item)
    component = components.declare_component('prenatal_tutor', path=str(Path(__file__).parent / 'prenatal_tutor'))
    result = component(cards=payload, token=token, compact=compact, key='tutor_' + token, default=None)
    return isinstance(result, dict) and result.get('token') == token and result.get('completed') == len(cards)


def introduction():
    return {'title': 'Nia · Tu asistente de IA', 'text': 'Hola, soy Nia, tu asistente de inteligencia artificial de la aplicación prenatal. Te acompañaré a repasar lo aprendido, paso a paso. Soy una guía educativa y no sustituyo al personal de salud.'}
