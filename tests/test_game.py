import json
import shutil
import subprocess
import unittest

from gestation_game import STAGES


class GameTests(unittest.TestCase):
    def test_review_preserves_errors_after_component_completion(self):
        from unittest.mock import patch
        from streamlit.testing.v1 import AppTest
        from pathlib import Path
        import tempfile
        import os
        history = [dict(stage=s, index=i) for s, stage in enumerate(STAGES)
                   for i, food in enumerate(stage['foods']) if food['good'] or i == next(j for j, f in enumerate(stage['foods']) if not f['good'])]
        with tempfile.TemporaryDirectory() as folder:
            os.environ['RANKING_DB_PATH'] = str(Path(folder) / 'review.db')
            app = AppTest.from_file(str(Path('app.py').resolve())).run()
            for key, value in dict(fase='juego', user='Review test', test_completed=True, journey_test_score=80).items():
                app.session_state[key] = value
            with patch('gestation_game.components.declare_component', return_value=lambda **kwargs: {'history': history}):
                app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state['fase'], 'repaso_juego')
            self.assertEqual(len(app.session_state['game_review']), 30)
            self.assertEqual(sum(not row['good'] for row in app.session_state['game_review']), 5)
            self.assertTrue(next(b for b in app.button if b.label == 'VER RANKING').disabled)

    def test_stage_content_and_recipients(self):
        self.assertEqual([s['name'] for s in STAGES], ["Primer trimestre", "Segundo trimestre", "Tercer trimestre", "Preparación para el parto", "Posparto"])
        for stage in STAGES:
            self.assertTrue(stage['emergency']['situation'])
            self.assertEqual(len(stage['foods']), 9)
            self.assertEqual(sum(f['good'] for f in stage['foods']), 5)
            self.assertTrue(all(f['kind'] == 'obstetric' for f in stage['foods']))
            self.assertTrue(all(f['explanation'] and f['detail'] for f in stage['foods']))
            self.assertTrue(all(f['why'] and f['practice'] for f in stage['foods']))
            self.assertEqual(len({f['explanation'] for f in stage['foods']}), 9)
            self.assertFalse(next(f for f in stage['foods'] if f['icon'] == 'fruit')['good'])
            self.assertFalse(next(f for f in stage['foods'] if f['icon'] == 'tea')['good'])
        html = __import__('pathlib').Path('gestation_game/index.html').read_text(encoding='utf-8')
        self.assertNotIn('emergencyChoices', html)
        self.assertIn('eventSituation', html)

    @unittest.skipUnless(shutil.which('node'), 'Node required for browser game logic tests')
    def test_game_state_transitions(self):
        result = subprocess.run(['node', 'tests/test_game.cjs'], input=json.dumps(STAGES), text=True,
                                encoding='utf-8', capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
