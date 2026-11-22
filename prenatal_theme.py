"""Preserve the original interface, with a readable expander heading."""
import streamlit as st


def apply_theme():
    st.markdown('<style>\n    [data-testid="stExpander"] summary{background:#FCE0ED!important;color:#24324B!important}\n    [data-testid="stExpander"] summary:hover{background:#F8CEE2!important;color:#24324B!important}\n    [data-testid="stExpander"] summary p,[data-testid="stExpander"] summary span{color:#24324B!important}\n    [data-testid="stExpander"] summary svg{color:#24324B!important;fill:currentColor!important}\n    </style>', unsafe_allow_html=True)
