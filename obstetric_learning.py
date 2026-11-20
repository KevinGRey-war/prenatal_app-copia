"""Recognition and help-seeking scenarios, not clinical diagnosis or treatment."""

SOURCE = ('CDC · Señales de alarma materna',
          'https://www.cdc.gov/hearher/maternal-warning-signs/index.html')

CASES = [
    ('Sangrado durante el embarazo',
     'Tienes sangrado vaginal parecido a una menstruación.',
     'Buscar atención médica inmediata', 'Esperar al próximo control', 'Intentar resolverlo con alimentos',
     'Este sangrado requiere atención inmediata. Comer o esperar no sustituye la valoración médica.'),
    ('Dolor de cabeza y visión',
     'Tienes dolor de cabeza intenso y visión borrosa.',
     'Buscar atención médica inmediata', 'Dormir y esperar hasta mañana', 'Cambiar la dieta y esperar',
     'Son señales de alarma. Busca atención inmediata; no retrases la consulta para probar alimentos.'),
    ('Cambios en los movimientos',
     'Tu bebé se mueve menos de lo habitual.',
     'Buscar valoración médica inmediata', 'Esperar al día siguiente', 'Comer algo dulce y posponer la consulta',
     'La disminución de movimientos requiere valoración inmediata. Comer algo no descarta un problema.'),
    ('Dificultad para respirar',
     'Te cuesta respirar y tienes dolor en el pecho.',
     'Pedir ayuda médica de emergencia', 'Continuar las actividades', 'Tomar una bebida y esperar',
     'Busca ayuda de emergencia ahora. Estos síntomas no deben tratarse solamente con descanso o alimentos.'),
    ('Sangrado después del nacimiento',
     'Después del parto empapas una toalla higiénica en una hora.',
     'Buscar atención médica inmediata', 'Esperar varios días', 'Comer alimentos con hierro y esperar',
     'Es una señal de alarma. Busca atención inmediata: comer hierro no trata una hemorragia.'),
]


def add_obstetric_cases(stages):
    for stage, case in zip(stages, CASES):
        title, situation, correct, wrong1, wrong2, explanation = case
        stage['emergency'] = dict(title=title, situation=situation)
        stage['focus'] = title
        stage['lesson'] = situation + ' ' + explanation + ' Las tarjetas representan acciones de cuidado, no tratamientos. No hace falta completar estas acciones antes de pedir ayuda.'
        actions = [
            (correct, 'Atención sin demora', 'care', explanation, True),
            ('Pedir acompañamiento', 'Una persona de confianza', 'support',
             'Pide apoyo mientras buscas atención. Si nadie puede acompañarte, no retrases la ayuda.', True),
            ('Comunicar los síntomas', 'Cuenta qué pasa y desde cuándo', 'message',
             'Describe al equipo lo que sientes y cuándo comenzó. En este evento: ' + situation, True),
            ('Informar la etapa', stage['weeks'], 'calendar',
             'Informa que estás embarazada o que has dado a luz recientemente.', True),
            ('Compartir antecedentes', 'Medicamentos y problemas de salud', 'record',
             'Cuenta tus antecedentes y medicamentos al equipo. No demores la atención por buscar documentos.', True),
            (wrong1, 'Posponer la atención', 'clock', explanation, False),
            ('Ignorar la señal', 'Continuar como si nada', 'ignore', explanation, False),
            ('Fruta como solución', 'Comer y posponer la consulta', 'fruit',
             'La fruta puede formar parte de la alimentación habitual, pero no resuelve esta señal de alarma. ' + explanation, False),
            ('Infusión como solución', 'Sustituir la atención por una bebida', 'tea',
             'Una infusión no sustituye la atención de este evento. ' + explanation, False),
        ]
        stage['foods'] = [dict(name=name, detail=detail, icon=icon, explanation=feedback,
                               good=good, recipient='Mamá', kind='obstetric')
                          for name, detail, icon, feedback, good in actions]
    return stages
