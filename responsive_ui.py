"""Responsive layout refinements; no changes to the questionnaire's logic."""
import streamlit as st


def apply_responsive_layout():
    st.markdown("""<style>
    /* Keep the original palette and controls; adapt spacing and text to screens. */
    .stApp {overflow-x:hidden}
    .block-container {width:100%;min-width:0}
    [data-testid="stColumn"] {min-width:0}
    [data-testid="stButton"] button {white-space:normal;overflow-wrap:anywhere}
    .st-key-abrir_panel_admin button p {color:white!important}
    [data-testid="stSelectbox"] [data-baseweb="select"] {max-width:100%}
    .question-title,.screen-title,.brand-title {overflow-wrap:break-word}
    .stRadio div[role="radiogroup"] > label {box-sizing:border-box;max-width:100%}
    .stRadio div[role="radiogroup"] > label p {line-height:1.5}
    .st-key-preguntas_finales summary {padding:15px 18px;line-height:1.5}
    @media(min-width:769px){
        .screen-caption {max-width:760px}
        .quiz-side {position:sticky;top:20px}
    }
    @media(max-width:768px){
        [data-testid="stHorizontalBlock"] {flex-direction:column!important;gap:12px!important}
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important;flex:1 1 auto!important;min-width:0!important}
        .block-container {padding:18px 14px 30px}
        .login-logo {width:170px}
        .stApp .brand-title {font-size:clamp(1.7rem,7vw,2.25rem)!important;line-height:1.15!important}
        .stApp .brand-subtitle {font-size:1.08rem!important}
        .stApp .screen-title {font-size:clamp(1.65rem,6.5vw,2.1rem)!important}
        .screen-caption {margin-bottom:16px;font-size:.93rem}
        [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {flex-direction:row!important;flex-wrap:nowrap!important;gap:8px!important}
        [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) > [data-testid="stColumn"] {width:calc(33.333% - 6px)!important;min-width:0!important;flex:1 1 0!important}
        [data-testid="stMetric"] {padding:10px 8px;border-radius:15px}
        [data-testid="stMetricLabel"] {font-size:.75rem}
        [data-testid="stMetricValue"] {font-size:1.35rem}
        .question-title {font-size:1.25rem;line-height:1.45;margin-bottom:16px}
        .quiz-instruction {font-size:.85rem;padding:9px 12px}
        .stRadio div[role="radiogroup"] > label {padding:12px!important;margin-bottom:8px;min-height:54px}
        .stRadio div[role="radiogroup"] > label p {font-size:.94rem}
        .quiz-side {padding:13px 16px;font-size:.85rem}
        .quiz-side p {margin:4px 0}
        div.stButton > button {min-height:54px!important;font-size:.95rem!important}
        .st-key-preguntas_finales summary {padding:13px 12px}
        .st-key-preguntas_finales p {font-size:.94rem;line-height:1.6}
        .admin-access-copy {padding:13px;margin-top:12px}
    }
    @media(prefers-reduced-motion:reduce){
        .stApp * {scroll-behavior:auto!important;transition:none!important;animation:none!important}
    }
    </style>""", unsafe_allow_html=True)
