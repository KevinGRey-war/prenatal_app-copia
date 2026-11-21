"""Explicit obstetric learning quota without mutating the original question bank."""
import random
from obstetric_learning import CASES


def question(text, answer, wrong1, wrong2, explanation, example):
    return dict(q=text, opts=[answer, wrong1, wrong2], corr=answer,
                bien=explanation, mal=explanation, example='Por ejemplo: '+example,
                topic='Eventos obstétricos')


COMMON = [
    question('Al pedir atención por una señal de alarma, ¿qué información debes comunicar?',
             'Síntomas, cuándo empezaron y si estás embarazada o en posparto',
             'Únicamente tu nombre', 'Solo el resultado de este test',
             'Describe los síntomas y su inicio, e informa sobre tu embarazo o parto reciente.',
             'Puedes decir: estoy embarazada y desde esta mañana tengo estos síntomas.'),
    question('¿Qué papel tiene una persona de confianza ante una señal de alarma?',
             'Acompañar y apoyar sin retrasar la atención',
             'Reemplazar la valoración médica', 'Decidir que debes esperar varios días',
             'El acompañamiento puede ayudarte a comunicar tus preocupaciones. No sustituye la atención médica.',
             'Pide compañía mientras buscas ayuda; no esperes si esa persona no está disponible.'),
]

STAGE_NAMES = ['Primer trimestre', 'Segundo trimestre', 'Tercer trimestre',
               'Preparación para el parto', 'Posparto']
EVENTS = {}
for name, case in zip(STAGE_NAMES, CASES):
    title, situation, correct, wrong1, wrong2, explanation = case
    EVENTS[name] = [question(situation+' ¿Qué corresponde hacer?', correct, wrong1,
                            wrong2, explanation, 'Ante esta situación, pide atención sin esperar al próximo control.'),
                    *COMMON]


def exam_pool(original, stage):
    """Return seven original items and three required obstetric items."""
    return random.sample(original, 7) + [dict(q) for q in EVENTS[stage]]
