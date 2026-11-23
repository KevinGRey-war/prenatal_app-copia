"""Personalized educational recap using only recorded answers and choices."""
from feedback_examples import test_risk


def review_cards(answers, actions):
    if len(answers) != 10 or not actions:
        return []
    wrong_answers = [(n, row) for n, row in enumerate(answers, 1) if not row['correct']]
    wrong_actions = [row for row in actions if not row['good']]
    cards = [{'title': 'Hola, soy Nia · Tu asistente de IA',
              'text': 'Hola, soy Nia, la asistente de inteligencia artificial de esta aplicación prenatal. Ya completaste el test y el juego. Vamos a repasar con calma las respuestas y decisiones que podemos reforzar. Equivocarse forma parte de aprender. Te explicaré qué puedes hacer y por qué, con ejemplos. Mi orientación es educativa y no sustituye al personal de salud.'}]
    if not wrong_answers:
        cards.append({'title': 'Tu test · ¡Diez aciertos!', 'text': 'Respondiste correctamente las diez preguntas del test. ¡Muy bien! Ahora repasemos cómo aplicaste tus conocimientos en el juego.'})
    for number, row in wrong_answers:
        cards.append({'title': f'Test · Pregunta {number}',
                      'text': f"Repasemos esta pregunta: {row['question']}\nElegiste: {row['selected']}.\nLa respuesta correcta es: {row['answer']}.\n{row['feedback']}\n{row.get('example', '')}"})
    if not wrong_actions:
        cards.append({'title': 'Tu juego · Buenas decisiones', 'text': 'Todas las acciones que elegiste en el juego fueron adecuadas. Practicaste cómo reconocer señales de alarma, comunicar lo que ocurre y buscar atención.'})
    for row in wrong_actions:
        cards.append({'title': 'Juego · ' + row['stage'],
                      'text': f"Elegiste: {row['name']}.\n{row['explanation']}"})
    count = len(wrong_actions)
    game_risk = 'riesgo educativo alto' if count >= 11 else 'riesgo educativo leve' if count >= 5 else 'sin riesgo educativo'
    cards.append({'title': 'Tu aprendizaje · Un paso más para cuidarte',
                  'text': f"En el test lograste {10-len(wrong_answers)} de 10 aciertos: {test_risk(10-len(wrong_answers))}. En el juego registraste {count} decisiones por reforzar: {game_risk}. Estas categorías miden aprendizaje, no riesgo clínico. Gracias por completar las dos actividades. Pedir ayuda y comunicar tus dudas también es cuidarte. Ya puedes consultar tu puntaje conjunto."})
    return cards
