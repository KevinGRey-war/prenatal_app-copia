import json
import shutil
import subprocess
import unittest

from gestation_game import STAGES


class GameTests(unittest.TestCase):
    def test_stage_content_and_recipients(self):
        self.assertEqual([s['name'] for s in STAGES], ["Primer trimestre", "Segundo trimestre", "Tercer trimestre", "Preparación para el parto", "Posparto"])
        for stage in STAGES:
            self.assertTrue(stage['emergency']['situation'])
            self.assertEqual(len(stage['foods']), 9)
            self.assertEqual(sum(f['good'] for f in stage['foods']), 5)
            self.assertTrue(all(f['kind'] == 'obstetric' for f in stage['foods']))
            self.assertTrue(all(f['explanation'] and f['detail'] for f in stage['foods']))
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
