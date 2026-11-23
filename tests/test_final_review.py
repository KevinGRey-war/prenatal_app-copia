import unittest
from final_review import review_cards


class FinalReviewTests(unittest.TestCase):
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
        self.assertIn('Diez aciertos', cards[1]['title'])
        self.assertIn('Todas las acciones', cards[2]['text'])
        for count, risk in [(4, 'sin riesgo educativo'), (5, 'riesgo educativo leve'), (10, 'riesgo educativo leve'), (11, 'riesgo educativo alto')]:
            actions = [dict(good=False, stage='Etapa', name='Esperar', explanation='Busca ayuda.') for _ in range(count)]
            self.assertIn(f'{count} decisiones por reforzar: {risk}', review_cards(self.answers, actions)[-1]['text'])
