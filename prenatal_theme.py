"""Lilac palette layered over the preserved original layout."""
import streamlit as st


def apply_theme():
    st.markdown('''<style>
    .stApp{background:linear-gradient(135deg,#faf7ff,#eee5f7)!important;color:#342345}
    .screen-title,.screen-caption,.quiz-side p,.side-card p{color:#47265f!important}
    .side-card,.quiz-side{background:#f5edfc!important;border:1px solid #cbb2df!important}
    div.stButton>button{background:#704098!important;color:white!important;border:1px solid #653388!important;border-radius:16px}
    div.stButton>button p{color:inherit!important}
    div.stButton>button:hover{background:#573074!important}
    div.stButton>button:disabled{background:#e4d9ed!important;color:#6b5879!important;border-color:#c9b7d6!important}
    [data-testid="stExpander"] details{background:#f2eafa!important;border:1px solid #cbb2df!important}
    [data-testid="stRadio"] label{color:#39264b!important}
    </style>''', unsafe_allow_html=True)
