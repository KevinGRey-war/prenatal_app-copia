"""Quiet original music for the quiz, paused underneath voice feedback."""
from pathlib import Path
import streamlit.components.v1 as components


def show_test_music(narrating=False):
    music = (Path(__file__).parent / 'gestation_game' / 'music.js').read_text(encoding='utf-8').replace('vida-music', 'vida-test-music')
    component = components.declare_component('prenatal_test_music', path=str(Path(__file__).parent / 'test_music'))
    component(music=music, narrating=bool(narrating), key='test_background_music', default=None)
