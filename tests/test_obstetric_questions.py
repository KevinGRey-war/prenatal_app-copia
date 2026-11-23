import unittest
from obstetric_questions import EVENTS, exam_pool
from feedback_examples import example_for


class ObstetricQuestionTests(unittest.TestCase):
    def test_quiz_event_matches_the_corresponding_game_stage(self):
        from gestation_game import STAGES
        for stage in STAGES:
            event_question = EVENTS[stage['name']][0]
            self.assertIn(stage['emergency']['situation'], event_question['q'])
            safe_action = next(f for f in stage['foods'] if f['icon'] == 'care')
            self.assertEqual(event_question['corr'], safe_action['name'])
            self.assertIn(event_question['bien'], safe_action['explanation'])
            self.assertIn('Ponlo en práctica:', safe_action['explanation'])

    def test_each_stage_has_three_required_event_questions(self):
        original = [dict(q=f'Original {i}', opts=['A', 'B'], corr='A') for i in range(10)]
        for stage in EVENTS:
            result = exam_pool(original, stage)
            self.assertEqual(len(result), 10)
            self.assertEqual(sum(q.get('topic') == 'Eventos obstétricos' for q in result), 3)
            self.assertEqual(len({q['q'] for q in result}), 10)
            for q in EVENTS[stage]:
                self.assertIn(q['corr'], q['opts'])
                self.assertTrue(example_for(q).startswith('Por ejemplo:'))
                self.assertTrue(q['bien'] and q['mal'])
        self.assertEqual(len(original), 10)
