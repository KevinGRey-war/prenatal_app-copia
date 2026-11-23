import ast
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from additional_questions import ADDITIONAL
from feedback_examples import example_for, final_narration, test_risk
from voice_feedback import clip_path, voice_markup, audio_markup


def original_bank():
    tree = ast.parse(Path("app.py").read_text(encoding="utf-8"))
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == "BANCO" for t in n.targets))


class SurveyTests(unittest.TestCase):
    def test_original_styles_and_questions_unchanged(self):
        source = Path("app.py").read_text(encoding="utf-8")
        css = source[source.index('st.markdown("""'):].split('# =========================================================\n# 🔊 VOZ')[0]
        self.assertEqual(hashlib.sha256(css.encode()).hexdigest(), "2035775b110ca12746276971347b6ca8bca66bc77202c4ce37cb8b1961255912")
        self.assertEqual(hashlib.sha256(json.dumps(original_bank(), sort_keys=True, ensure_ascii=True).encode()).hexdigest(),
                         "231f7f69376dba3f580d8722c6e4a646a4d3c9acb9aae0104ff5529d340e8093")

    def test_five_stages_and_ten_new_questions_each(self):
        self.assertEqual(len(original_bank() | ADDITIONAL), 5)
        for stage, questions in ADDITIONAL.items():
            self.assertEqual(len(questions), 10, stage)
            self.assertEqual(len({q["q"] for q in questions}), 10)
            for q in questions:
                self.assertEqual(q["opts"].count(q["corr"]), 1)
                self.assertTrue(q["bien"] and q["mal"])

    def test_specific_examples_for_every_question(self):
        for questions in (original_bank() | ADDITIONAL).values():
            for q in questions:
                self.assertTrue(example_for(q).startswith("Por ejemplo:"), q["q"])

    def test_all_score_boundaries(self):
        for score in range(11):
            self.assertIn("alto" if score <= 6 else "leve" if score <= 8 else "Sin", test_risk(score))

    def test_final_voice_includes_all_answers_and_examples(self):
        rows = [dict(question=q["q"], selected=q["opts"][1], answer=q["corr"], correct=False,
                     feedback=q["mal"], example=example_for(q)) for q in ADDITIONAL["Posparto"]]
        text = final_narration(rows, 0, test_risk(0))
        for row in rows:
            for key in ["question", "selected", "answer", "feedback", "example"]:
                self.assertIn(row[key], text)
        self.assertIn("Pregunta 10.", text)

    def test_audio_assets_cover_every_possible_explanation(self):
        from scripts.build_voice_assets import texts
        manifest = json.loads(Path("voice_assets/manifest.json").read_text(encoding="utf-8"))
        for text in texts():
            path = clip_path(text)
            self.assertTrue(path.is_file(), text)
            self.assertGreater(manifest[path.stem]["seconds"], .1)
            self.assertGreater(path.stat().st_size, 500)
            self.assertFalse(path.read_bytes().startswith(b"ID3"))

    def test_browser_voice_fallback_escapes_text(self):
        output = voice_markup("'Texto' </script><script>alert(1)</script>")
        self.assertNotIn("</script><script>alert", output)
        self.assertNotIn("<button", output)

    def test_voice_embeds_recording_without_media_route(self):
        import base64
        data = clip_path(ADDITIONAL["Posparto"][0]["q"]).read_bytes()
        markup = audio_markup(data)
        self.assertIn("hidden autoplay", markup)
        self.assertNotIn("controls", markup)
        self.assertIn("audio.play()", markup)
        payload = markup.split("data:audio/mpeg;base64,", 1)[1].split('"', 1)[0]
        self.assertEqual(base64.b64decode(payload), data)
        self.assertNotIn("/media/", markup)

    @patch("prenatal_tutor.show_tutor", return_value=True)
    def test_complete_original_quiz_flow_and_final_audio(self, tutor):
        from streamlit.testing.v1 import AppTest
        with tempfile.TemporaryDirectory() as directory:
            os.environ["RANKING_DB_PATH"] = str(Path(directory) / "ranking.sqlite3")
            app = AppTest.from_file(str(Path("app.py").resolve())).run()
            self.assertFalse(app.exception)
            self.assertEqual([b.label for b in app.button], ["COMENZAR EXPERIENCIA", "🔐 ENTRAR AL PANEL ADMINISTRATIVO"])
            app.text_input[0].set_value("Prueba local")
            self.assertEqual(len(app.selectbox), 0)
            app.button[0].click().run()
            self.assertEqual(app.session_state["fase"], "etapa")
            app.selectbox[0].select("Posparto")
            next(b for b in app.button if b.label == "COMENZAR TEST").click().run()
            self.assertEqual(app.session_state["fase"], "test")
            # Rebind the session: AppTest 1.57 retains removed widgets after a
            # st.rerun inside the original login's column.
            keys = ["fase", "user", "examen", "trimestre", "pts", "idx", "resp", "fb", "correcto",
                    "respuesta_seleccionada", "ranking_guardado", "ranking_storage_version", "answers"]
            state = {key: app.session_state[key] for key in keys}
            app = AppTest.from_file(str(Path("app.py").resolve()))
            for key, value in state.items():
                app.session_state[key] = value
            app.run()
            self.assertEqual(len(app.get("iframe")), 0, "No se debe narrar al comenzar")
            for i in range(10):
                self.assertTrue(next(b for b in app.button if b.label == "VERIFICAR").disabled)
                question = app.session_state["examen"][i]
                answer = question["corr"] if i < 7 else next(o for o in question["opts"] if o != question["corr"])
                app.radio[0].set_value(answer).run()
                self.assertFalse(app.session_state["resp"])
                self.assertEqual(len(app.session_state["answers"]), i)
                next(b for b in app.button if b.label == "VERIFICAR").click().run()
                self.assertFalse(app.exception)
                self.assertTrue(app.session_state["resp"])
                for block in app.markdown:
                    self.assertNotIn("<div class='error-box'>", block.value)
                    self.assertNotIn("<div class='success-box'>", block.value)
                self.assertTrue(tutor.called)
                self.assertTrue(clip_path(app.session_state["fb"]).is_file())
                if i >= 7:
                    self.assertIn("Por ejemplo:", app.session_state["fb"])
                next(b for b in app.button if b.label == "CONTINUAR").click().run()
                self.assertFalse(app.exception)
            self.assertEqual(app.session_state["fase"], "final")
            self.assertEqual(app.session_state["pts"], 70)
            self.assertEqual(len(app.session_state["answers"]), 10)
            self.assertTrue(any("Retroalimentación final" in h.value for h in app.subheader))
            self.assertEqual(len(tutor.call_args.args[0]), 1)
            self.assertTrue(tutor.call_args.kwargs["compact"])
            self.assertEqual(len(app.expander), 10)
            self.assertTrue(app.session_state["test_completed"])
            self.assertTrue(any(b.label == "CONTINUAR AL JUEGO" for b in app.button))
            self.assertFalse(any("un solo puntaje" in h.value for h in app.subheader))
            self.assertFalse(any(b.label == "VOLVER AL MENÚ" for b in app.button))
            next(b for b in app.button if b.label == "CONTINUAR AL JUEGO").click().run()
            self.assertEqual(app.session_state["fase"], "juego")
            self.assertFalse(app.exception)

    def test_game_requires_test_and_ranking_requires_game(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(Path("app.py").resolve())).run()
        app.button[0].click().run()
        self.assertEqual(app.session_state["fase"], "login")
        app.text_input[0].set_value("Prueba directa")
        app.button[0].click().run()
        self.assertEqual(app.session_state["fase"], "etapa")
        self.assertFalse(any(b.label == "ENTRAR AL JUEGO" for b in app.button))
        app.session_state["fase"] = "juego"
        app.run()
        self.assertEqual(app.session_state["fase"], "etapa")
        app.session_state["fase"] = "ranking"
        app.run()
        self.assertEqual(app.session_state["fase"], "etapa")
        app.session_state["test_completed"] = True
        app.session_state["journey_test_score"] = 70
        app.session_state["fase"] = "ranking"
        app.run()
        self.assertEqual(app.session_state["fase"], "juego")
        self.assertFalse(any("un solo puntaje" in h.value for h in app.subheader))

    def test_game_completion_goes_directly_to_ranking_and_finish_resets(self):
        from streamlit.testing.v1 import AppTest
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as directory:
            os.environ['RANKING_DB_PATH'] = str(Path(directory) / 'scores.sqlite3')
            app = AppTest.from_file(str(Path('app.py').resolve())).run()
            for key, value in dict(fase='juego', user='Recorrido', test_completed=True,
                                   journey_test_score=70, answers=[dict(correct=True, question='Pregunta', selected='A', answer='A', feedback='Correcto', example='Ejemplo') for _ in range(10)], game_review=[dict(good=False, stage='Posparto', name='Esperar', explanation='Buscar atención inmediata.')]).items():
                app.session_state[key] = value
            with patch('gestation_game.show_game', return_value=80):
                app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state['fase'], 'repaso_juego')
            self.assertTrue(next(b for b in app.button if b.label == 'VER RANKING').disabled)
            with patch('prenatal_tutor.show_tutor', return_value=True):
                app.run()
                next(b for b in app.button if b.label == 'VER RANKING').click().run()
            self.assertEqual(app.session_state['fase'], 'ranking')
            self.assertEqual(app.session_state['journey_game_score'], 80)
            self.assertTrue(any('75.0/100' in metric.value for metric in app.metric))
            self.assertFalse(any(h.value == 'Retroalimentación del juego' for h in app.subheader))
            next(b for b in app.button if b.label == 'FINALIZAR Y VOLVER AL INICIO').click().run()
            self.assertEqual(app.session_state['fase'], 'login')
            self.assertEqual(app.session_state['user'], '')
            self.assertFalse(app.session_state['test_completed'])
            self.assertFalse(app.session_state['game_completed'])


if __name__ == "__main__":
    unittest.main()
