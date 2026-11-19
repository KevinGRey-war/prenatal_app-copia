import sqlite3
import tempfile
from pathlib import Path
import unittest

from gestation_game import STAGES
from learning_score import ranking, save_score, validated_game_score


class LearningScoreTests(unittest.TestCase):
    def test_unified_score_best_attempts_and_pending_activity(self):
        with tempfile.TemporaryDirectory() as folder:
            db = str(Path(folder) / 'scores.db')
            save_score(db, 'Ana', 'test', 80)
            self.assertFalse(ranking(db)[0]['complete'])
            save_score(db, ' ANA ', 'game', 100)
            save_score(db, 'Ana', 'test', 60)
            rows = ranking(db)
            self.assertEqual(len(rows), 1)
            self.assertTrue(rows[0]['complete'])
            self.assertEqual(rows[0]['puntos'], 90)

    def test_legacy_results_are_preserved_and_imported_once(self):
        with tempfile.TemporaryDirectory() as folder:
            db = str(Path(folder) / 'scores.db')
            with sqlite3.connect(db) as con:
                con.execute('CREATE TABLE ranking(nombre TEXT,puntos INTEGER)')
                con.executemany('INSERT INTO ranking VALUES (?,?)', [('Ana', 60), ('Ana', 90)])
            con.close()
            self.assertEqual(ranking(db)[0]['test'], 90)
            self.assertEqual(len(ranking(db)), 1)
            with sqlite3.connect(db) as con:
                self.assertEqual(con.execute('SELECT COUNT(*) FROM ranking').fetchone()[0], 2)
            con.close()

    def test_browser_result_recalculated_and_incomplete_duplicate_rejected(self):
        history = [dict(stage=s, index=i) for s, stage in enumerate(STAGES)
                   for i, food in enumerate(stage['foods']) if food['good']]
        self.assertEqual(validated_game_score({'history': history}, STAGES), 100)
        self.assertIsNone(validated_game_score({'history': history[:-1]}, STAGES))
        self.assertIsNone(validated_game_score({'history': history + [history[-1]]}, STAGES))
        all_choices = [dict(stage=s, index=i) for s, stage in enumerate(STAGES)
                       for i in range(len(stage['foods']))]
        self.assertEqual(validated_game_score({'history': all_choices, 'score': 100}, STAGES), 55.56)
        self.assertIsNone(validated_game_score({'history': list(reversed(history))}, STAGES))


if __name__ == '__main__':
    unittest.main()
