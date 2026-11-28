import unittest
from final_review import review_cards, survey_cards


class FinalReviewTests(unittest.TestCase):
    def test_test_recap_excludes_correct_answers(self):
        rows = [dict(correct=True, question='No debe aparecer', selected='A', answer='A', feedback='', example='') for _ in range(10)]
        rows[4].update(correct=False, question='Error real', feedback='Motivo', example='Ejemplo útil')
        cards = survey_cards(rows)
        self.assertEqual(len(cards), 2)
        self.assertIn('Pregunta 5', cards[1]['title'])
        self.assertNotIn('No debe aparecer', str(cards))
        self.assertIn('Ejemplo útil', cards[1]['text'])
        rows[4]['correct'] = True
        self.assertEqual(len(survey_cards(rows)), 1)

    def test_overlay_completion_is_retained_after_rerun(self):
        from unittest.mock import patch
        from streamlit.testing.v1 import AppTest
        script = '''import streamlit as st
from prenatal_tutor import show_tutor
ready = show_tutor([dict(title='Repaso', text='Un error explicado.')], 'test-overlay', overlay=True)
st.button('Continuar', disabled=not ready)
'''
        app = AppTest.from_string(script)
        with patch('prenatal_tutor.components.declare_component', return_value=lambda **kw: None):
            app.run()
        self.assertTrue(app.button[0].disabled)
        with patch('prenatal_tutor.components.declare_component', return_value=lambda **kw: dict(token=kw['token'], completed=1)):
            app.run()
        self.assertFalse(app.exception)
        self.assertFalse(app.button[0].disabled)
        self.assertFalse(any('position:fixed' in m.value for m in app.markdown))
        with patch('prenatal_tutor.components.declare_component') as component:
            app.run()
            component.assert_not_called()

    def setUp(self):
        self.answers = [dict(correct=True, question=f'Pregunta {n}', selected='A', answer='A', feedback='Explicación', example='Ejemplo') for n in range(10)]
        self.actions = [dict(good=True, stage='Primer trimestre', name='Buscar ayuda', explanation='Pide atención.')]

    def test_only_recorded_errors_from_both_activities_are_reviewed(self):
        self.answers[2].update(correct=False, selected='B', feedback='Explicación específica')
        self.actions.append(dict(good=False, stage='Posparto', name='Esperar', explanation='No retrases la atención.'))
        cards = review_cards(self.answers, self.actions)
        self.assertEqual(len(cards), 4)
        self.assertIn('inteligencia artificial', cards[0]['text'])
        self.assertIn('Pregunta 3', cards[1]['title'])
        self.assertIn('Elegiste: B', cards[1]['text'])
        self.assertIn('correcta es: A', cards[1]['text'])
        self.assertIn('Explicación específica', cards[1]['text'])
        self.assertIn('Ejemplo', cards[1]['text'])
        self.assertIn('Posparto', cards[2]['title'])
        self.assertIn('No retrases', cards[2]['text'])
        self.assertIn('9 de 10', cards[-1]['text'])

    def test_incomplete_data_does_not_invent_success(self):
        self.assertEqual(review_cards([], self.actions), [])
        self.assertEqual(review_cards(self.answers, []), [])

    def test_perfect_attempt_and_risk_boundaries(self):
        cards = review_cards(self.answers, self.actions)
        self.assertIn('Sin errores', cards[1]['title'])
        self.assertEqual(len(cards), 3)
        for count, risk in [(4, 'sin riesgo educativo'), (5, 'riesgo educativo leve'), (10, 'riesgo educativo leve'), (11, 'riesgo educativo alto')]:
            actions = [dict(good=False, stage='Etapa', name='Esperar', explanation='Busca ayuda.') for _ in range(count)]
            self.assertIn(f'{count} decisiones por reforzar: {risk}', review_cards(self.answers, actions)[-1]['text'])
