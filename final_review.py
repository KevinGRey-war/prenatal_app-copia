"""Personalized educational recap using only recorded answers and choices."""
from feedback_examples import test_risk


def test_error_cards(answers):
    return [{'title': f'Test · Pregunta {n}',
             'text': f"Vamos paso a paso. {row['question']}\nElegiste: {row['selected']}.\nLa respuesta correcta es: {row['answer']}.\nPor qué: {row['feedback']}\n{row.get('example', '')}"}
            for n, row in enumerate(answers, 1) if not row['correct']]


def survey_cards(answers):
    if len(answers) != 10:
        return []
    errors = test_error_cards(answers)
    if not errors:
        return [{'title': '¡Muy bien! No hay errores que repasar', 'text': 'Completaste el test sin errores. Ahora podrás aplicar lo aprendido en el juego.'}]
    return [{'title': 'Hola, soy Nia · Tu asistente de IA', 'text': 'Soy la asistente de inteligencia artificial de esta aplicación. Repasemos solo las respuestas que podemos mejorar, una por una. Te explicaré el porqué con ejemplos. Equivocarse también nos ayuda a aprender.'}] + errors


def review_cards(answers, actions):
    if len(answers) != 10 or not actions:
        return []
    wrong_answers = [(n, row) for n, row in enumerate(answers, 1) if not row['correct']]
    wrong_actions = [row for row in actions if not row['good']]
    cards = [{'title': 'Hola, soy Nia · Tu asistente de IA',
              'text': 'Hola, soy Nia, la asistente de inteligencia artificial de esta aplicación prenatal. Ya completaste el test y el juego. Vamos a repasar con calma las respuestas y decisiones que podemos reforzar. Equivocarse forma parte de aprender. Te explicaré qué puedes hacer y por qué, con ejemplos. Mi orientación es educativa y no sustituye al personal de salud.'}]
    cards.extend(test_error_cards(answers))
    for row in wrong_actions:
        cards.append({'title': 'Juego · ' + row['stage'],
                      'text': f"Elegiste: {row['name']}.\n{row['explanation']}\nEstas señales pueden indicar una complicación importante. La valoración profesional permite averiguar la causa; una comida o bebida no permite descartarla. Pedir ayuda a tiempo es la acción que estamos practicando.",
                      'source': 'CDC · Señales de alarma materna',
                      'source_url': 'https://www.cdc.gov/hearher/maternal-warning-signs/index.html'})
    if not wrong_answers and not wrong_actions:
        cards.append({'title': '¡Sin errores en las dos actividades!', 'text': 'No hay respuestas equivocadas que repasar. Gracias por practicar cómo cuidarte y buscar ayuda.'})
    count = len(wrong_actions)
    game_risk = 'riesgo educativo alto' if count >= 11 else 'riesgo educativo leve' if count >= 5 else 'sin riesgo educativo'
    cards.append({'title': 'Tu aprendizaje · Un paso más para cuidarte',
                  'text': f"En el test lograste {10-len(wrong_answers)} de 10 aciertos: {test_risk(10-len(wrong_answers))}. En el juego registraste {count} {"decisión" if count == 1 else "decisiones"} por reforzar: {game_risk}. Estas categorías miden aprendizaje, no riesgo clínico. Gracias por completar las dos actividades. Pedir ayuda y comunicar tus dudas también es cuidarte. Ya puedes consultar tu puntaje conjunto."})
    return cards

