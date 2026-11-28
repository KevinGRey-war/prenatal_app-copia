"""Complete application route with real scoring and simulated browser boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
from gestation_game import STAGES


class JourneyTests(unittest.TestCase):
    def test_name_quiz_game_combined_review_ranking_and_reset(self):
        engine_script = '''const E=require('./gestation_game/engine.js');
        const stages=JSON.parse(require('fs').readFileSync(0,'utf8'));
        let state={...E.fresh(),started:true};
        for(let s=0;s<stages.length;s++){
          if(s===0)state=E.choose(state,stages,stages[s].foods.findIndex(f=>!f.good));
          stages[s].foods.forEach((f,i)=>{if(f.good)state=E.choose(state,stages,i);});
          state=E.next(state,stages);
        }
        if(!state.done)throw Error('Game incomplete');
        process.stdout.write(JSON.stringify({history:state.history.map(({stage,index})=>({stage,index}))}));'''
        payload = json.loads(subprocess.check_output(['node', '-e', engine_script], input=json.dumps(STAGES).encode()))
        with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {'RANKING_DB_PATH': str(Path(folder) / 'route.db')}), patch('prenatal_tutor.show_tutor', return_value=False) as tutor:
            # The recap module retains its imported callable across AppTest runs.
            recap_patch = patch('journey_completion.show_tutor', tutor)
            recap_patch.start()
            self.addCleanup(recap_patch.stop)
            app = AppTest.from_file(str(Path('app.py').resolve())).run()
            app.text_input[0].set_value('Ruta completa de prueba')
            next(b for b in app.button if b.label == 'COMENZAR EXPERIENCIA').click().run()
            self.assertEqual(app.session_state['fase'], 'etapa')
            app.selectbox[0].select('Primer trimestre')
            next(b for b in app.button if b.label == 'COMENZAR TEST').click().run()
            # AppTest retains removed login widgets across reruns; rebind the same state.
            keys = ['fase','user','examen','trimestre','pts','idx','resp','fb','correcto',
                    'respuesta_seleccionada','ranking_guardado','ranking_storage_version','answers']
            saved = {k: app.session_state[k] for k in keys}
            app = AppTest.from_file(str(Path('app.py').resolve()))
            for k, value in saved.items(): app.session_state[k] = value
            app.run()
            for i in range(10):
                tutor.return_value = False
                q = app.session_state['examen'][i]
                choice = next(o for o in q['opts'] if o != q['corr']) if i == 0 else q['corr']
                app.radio[0].set_value(choice).run()
                next(b for b in app.button if b.label == 'VERIFICAR').click().run()
                self.assertTrue(next(b for b in app.button if b.label == 'CONTINUAR').disabled)
                tutor.return_value = True
                app.run()
                next(b for b in app.button if b.label == 'CONTINUAR').click().run()
                self.assertFalse(app.exception)
            self.assertEqual(app.session_state['fase'], 'final')
            self.assertEqual(app.session_state['pts'], 90)
            tutor.return_value = False
            app.run()
            self.assertTrue(next(b for b in app.button if b.label == 'CONTINUAR AL JUEGO').disabled)
            tutor.return_value = True
            app.run()
            next(b for b in app.button if b.label == 'CONTINUAR AL JUEGO').click().run()
            self.assertEqual(app.session_state['fase'], 'juego')
            tutor.return_value = False
            with patch('gestation_game.components.declare_component', return_value=lambda **kwargs: payload):
                app.run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state['fase'], 'repaso_juego')
            self.assertEqual(app.session_state['journey_game_score'], 96.15)
            self.assertEqual(sum(not r['good'] for r in app.session_state['game_review']), 1)
            cards = tutor.call_args.args[0]
            self.assertEqual(len(cards), 4)  # Introduction, one quiz error, one game error, closing.
            self.assertFalse(tutor.call_args.kwargs['compact'])
            self.assertIn('Test', cards[1]['title'])
            self.assertIn('Juego', cards[2]['title'])
            self.assertTrue(next(b for b in app.button if b.label == 'VER RANKING').disabled)
            tutor.return_value = True
            app.run()
            next(b for b in app.button if b.label == 'VER RANKING').click().run()
            self.assertEqual(app.session_state['fase'], 'ranking')
            self.assertTrue(any('93.1/100' in m.value for m in app.metric))
            next(b for b in app.button if b.label == 'FINALIZAR Y VOLVER AL INICIO').click().run()
            self.assertEqual(app.session_state['fase'], 'login')
            self.assertEqual(app.session_state['user'], '')
            self.assertFalse(app.exception)
