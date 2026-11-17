import json
import shutil
import subprocess
import unittest

from gestation_game import STAGES


class GameTests(unittest.TestCase):
    def test_stage_content_and_recipients(self):
        self.assertEqual([s['name'] for s in STAGES], ["Primer trimestre", "Segundo trimestre", "Tercer trimestre", "Preparación para el parto", "Posparto"])
        prenatal = [f for s in STAGES[:4] for f in s['foods']]
        self.assertEqual(len({f['name'] for f in prenatal if f['good']}), 20)
        self.assertTrue(all(f['recipient'] == 'Mamá' for f in prenatal))
        for s in STAGES:
            self.assertEqual(sum(f['good'] for f in s['foods']), 5)
            self.assertEqual(sum(not f['good'] for f in s['foods']), 4)
            self.assertTrue(all(f['explanation'] and f['detail'] for f in s['foods']))
        infant = [f for f in STAGES[-1]['foods'] if f['recipient'] == 'Bebé' and f['good']]
        self.assertEqual([f['name'] for f in infant], ['Leche materna', 'Fórmula infantil'])

    @unittest.skipUnless(shutil.which('node'), 'Node required for browser game logic tests')
    def test_game_state_transitions(self):
        result = subprocess.run(['node', 'tests/test_game.cjs'], input=json.dumps(STAGES), text=True,
                                encoding='utf-8', capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
