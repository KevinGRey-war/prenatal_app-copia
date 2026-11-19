"""A single local learning score; clinical/educational classifications stay separate."""
import sqlite3
from contextlib import contextmanager
import unicodedata


def identity(name):
    return ' '.join(unicodedata.normalize('NFKC', name).casefold().split())


@contextmanager
def connect(path):
    con = sqlite3.connect(path)
    con.execute('''CREATE TABLE IF NOT EXISTS learning_scores (
        person TEXT NOT NULL, name TEXT NOT NULL, activity TEXT NOT NULL,
        score REAL NOT NULL CHECK(score BETWEEN 0 AND 100),
        PRIMARY KEY(person, activity))''')
    try:
        with con:
            yield con
    finally:
        con.close()


def save_score(path, name, activity, score):
    if activity not in ('test', 'game') or not 0 <= score <= 100 or not identity(name):
        raise ValueError('Resultado inválido')
    with connect(path) as con:
        con.execute('''INSERT INTO learning_scores VALUES(?,?,?,?)
            ON CONFLICT(person,activity) DO UPDATE SET
            score=MAX(score,excluded.score), name=excluded.name''',
            (identity(name), name.strip(), activity, score))


def validated_game_score(payload, stages):
    """Recalculate from choices; never trust browser totals or completion flags."""
    if not isinstance(payload, dict) or not isinstance(payload.get('history'), list):
        return None
    history = payload['history']
    if len(history) > sum(len(s['foods']) for s in stages):
        return None
    seen, good, current = set(), 0, 0
    counts = [0] * len(stages)
    for row in history:
        if not isinstance(row, dict):
            return None
        stage, index = row.get('stage'), row.get('index')
        if type(stage) is not int or type(index) is not int:
            return None
        if not 0 <= stage < len(stages) or not 0 <= index < len(stages[stage]['foods']):
            return None
        if stage != current:
            if stage != current + 1 or counts[current] != sum(f['good'] for f in stages[current]['foods']):
                return None
            current = stage
        if (stage, index) in seen:
            return None
        seen.add((stage, index))
        correct = stages[stage]['foods'][index]['good']
        good += correct
        counts[stage] += correct
    if any(counts[i] != sum(f['good'] for f in s['foods']) for i, s in enumerate(stages)):
        return None
    return round(100 * good / len(history), 2) if history else None


def ranking(path):
    with connect(path) as con:
        # Include existing test history without changing or deleting it.
        if con.execute("SELECT 1 FROM sqlite_master WHERE name='ranking' AND type='table'").fetchone():
            for name, score in con.execute('SELECT nombre, MAX(puntos) FROM ranking GROUP BY nombre').fetchall():
                if name and score is not None and 0 <= score <= 100:
                    con.execute('''INSERT INTO learning_scores VALUES(?,?,?,?)
                        ON CONFLICT(person,activity) DO UPDATE SET score=MAX(score,excluded.score)''',
                        (identity(name), name, 'test', score))
        rows = con.execute('''SELECT person, MAX(name),
            MAX(CASE WHEN activity='test' THEN score END),
            MAX(CASE WHEN activity='game' THEN score END)
            FROM learning_scores GROUP BY person''').fetchall()
    result = [dict(person=p, nombre=n, test=t, game=g,
                   puntos=round(((t or 0)+(g or 0))/2, 1), complete=t is not None and g is not None)
              for p, n, t, g in rows]
    return sorted(result, key=lambda r: (-r['complete'], -r['puntos'], r['person']))


def show_learning_ranking(path, name, current_test=None, current_game=None):
    import streamlit as st
    try:
        rows = ranking(path)
    except sqlite3.Error:
        st.warning('No se pudo consultar el puntaje conjunto. Tus resultados de esta actividad siguen visibles.')
        return
    st.subheader('Tu aprendizaje, un solo puntaje')
    st.caption('Test: 50 puntos · Juego: 50 puntos. Se conserva tu mejor resultado de cada actividad. '
               'El juego se calcula por aciertos entre elecciones realizadas. Las categorías de riesgo educativo se evalúan por separado.')
    own = next((r for r in rows if r['person'] == identity(name)), None)
    if current_test is not None and current_game is not None:
        st.metric('Puntaje conjunto de este recorrido', f"{(current_test + current_game)/2:.1f}/100")
        st.caption(f"Este recorrido · Test: {current_test:g}/100 · Juego: {current_game:g}/100")
    if own and own['complete']:
        st.caption(f"Tu mejor puntaje combinado en el ranking: {own['puntos']:g}/100")
    completed = [r for r in rows if r['complete']][:10]
    if completed:
        st.dataframe([{'Participante': r['nombre'], 'Test /50': round(r['test']/2, 1),
                       'Juego /50': round(r['game']/2, 1), 'Total /100': r['puntos']} for r in completed],
                     hide_index=True, use_container_width=True)
    else:
        st.info('El ranking conjunto se habilita al completar un test y el recorrido del juego.')
