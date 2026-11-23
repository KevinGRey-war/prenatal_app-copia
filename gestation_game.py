"""Five-stage nutrition learning game; the original survey is kept separate."""
from pathlib import Path
import base64
import uuid

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent / "gestation_game"


def item(name, icon, detail, explanation, good=True, recipient="Mamá"):
    return dict(name=name, icon=icon, detail=detail, explanation=explanation,
                good=good, recipient=recipient)


STAGES = [
    dict(name="Primer trimestre", short="Embrión", icon="🌱", weeks="Semanas 1–13", focus="Folato, variedad y alimentos seguros",
         lesson="Al inicio se forman estructuras esenciales. Los nutrientes llegan a través de la madre: no se da comida directamente al embrión. Los alimentos con folato no sustituyen el ácido fólico indicado en el control prenatal.",
         foods=[
             item("Lentejas", "🫘", "Bien cocidas", "Aportan folato, hierro vegetal y proteína. Combínalas con una fruta rica en vitamina C."),
             item("Espinaca", "🥬", "Lavada y cocida", "Aporta folato y fibra. La higiene y la cocción reducen riesgos de contaminación."),
             item("Naranja", "🍊", "Lavada, fruta entera", "Aporta vitamina C y ayuda a aprovechar el hierro de las legumbres. Prefiere la fruta entera al jugo."),
             item("Avena", "🌾", "Cocida, sin exceso de azúcar", "Aporta energía y fibra. Puede formar parte de un desayuno variado."),
             item("Aguacate", "🥑", "Lavado antes de cortarlo", "Aporta grasas insaturadas y fibra. Es una opción dentro de una alimentación variada."),
             item("Alcohol", "🍷", "Una copa durante el embarazo", "No se conoce una cantidad ni un momento seguros para beber alcohol en el embarazo. Elige una bebida sin alcohol.", False),
             item("Queso sin pasteurizar", "🧀", "Elaborado con leche cruda", "Puede transmitir infecciones. Revisa que el queso se elabore con leche pasteurizada.", False),
             item("Huevo crudo", "🥚", "Sin cocción", "Puede transmitir microorganismos. Elige huevo completamente cocido.", False),
             item("Fruta sin lavar", "🍎", "Directamente del mercado", "Lava la fruta cuidadosamente con agua potable antes de comerla o cortarla.", False),
         ]),
    dict(name="Segundo trimestre", short="Feto en crecimiento", icon="🌿", weeks="Semanas 14–27", focus="Proteína, hierro y calcio",
         lesson="El feto crece y se mueve. La madre necesita una alimentación variada, controles y los suplementos que le indiquen; ningún alimento por sí solo asegura el desarrollo.",
         foods=[
             item("Huevo", "🥚", "Clara y yema cocidas", "Aporta proteína y colina. Cocínalo completamente para consumirlo de forma segura."),
             item("Yogur natural", "🥣", "Pasteurizado", "Aporta calcio y proteína. Revisa la pasteurización y conserva la cadena de frío."),
             item("Pollo", "🍗", "Completamente cocido", "Aporta proteína. Cocina completamente y separa utensilios de alimentos crudos y cocidos."),
             item("Fréjol", "🫘", "Bien cocido", "Aporta hierro vegetal, proteína y fibra. Una fuente de vitamina C ayuda a absorber ese hierro."),
             item("Brócoli", "🥦", "Lavado y cocido", "Aporta folato, vitamina C y fibra. Alterna verduras de distintos colores."),
             item("Carne término medio", "🥩", "Centro aún crudo", "La carne poco cocida puede transmitir infecciones. Elige una cocción completa.", False),
             item("Leche cruda", "🥛", "Sin pasteurizar", "La leche sin pasteurizar puede contener microorganismos peligrosos. Prefiere leche pasteurizada.", False),
             item("Pez espada", "🐟", "Pescado alto en mercurio", "Evita pescados con mucho mercurio. Elige variedades bajas en mercurio, bien cocidas.", False),
             item("Sushi de pescado crudo", "🍣", "Sin cocción", "Durante el embarazo elige pescado completamente cocido para reducir riesgos de infección.", False),
         ]),
    dict(name="Tercer trimestre", short="Preparándose para nacer", icon="🌸", weeks="Desde la semana 28", focus="Energía, fibra y grasas saludables",
         lesson="El bebé continúa madurando. Mantén comidas variadas y seguras, sin asumir que hay que duplicar las porciones. La ilustración representa etapas, no un pronóstico del crecimiento real.",
         foods=[
             item("Salmón", "🐟", "Bien cocido, bajo en mercurio", "Aporta proteína y grasas omega 3. Alterna pescados bajos en mercurio y respeta las recomendaciones locales."),
             item("Quinua", "🌾", "Lavada y cocida", "Aporta energía, proteína vegetal y fibra. Combínala con verduras y otras fuentes de proteína."),
             item("Zanahoria", "🥕", "Lavada y cocida", "Aporta carotenoides y fibra. Varía las verduras sin depender de un solo alimento."),
             item("Pera", "🍐", "Lavada", "Aporta fibra y agua. La fibra, junto con líquidos y actividad indicada, puede ayudar al tránsito intestinal."),
             item("Nueces", "🥜", "Sin exceso de sal, si no hay alergia", "Para la madre, aportan grasas insaturadas y energía. Evítalas si tienes alergia conocida; no son para un recién nacido."),
             item("Gaseosa como hidratación", "🥤", "Reemplazar el agua todo el día", "Las bebidas azucaradas no deben ser la fuente principal de hidratación. Prefiere agua potable.", False),
             item("Bebida energética", "⚡", "Para quitar el cansancio", "No es una solución adecuada para el cansancio del embarazo. Puede aportar mucha cafeína y otros estimulantes; consulta si el cansancio persiste.", False),
             item("Brotes crudos", "🌱", "Sin cocción", "Los brotes crudos pueden contener microorganismos difíciles de quitar con el lavado. Consúmelos bien cocidos.", False),
             item("Ensalada sin refrigerar", "🥗", "Varias horas fuera del frío", "Los alimentos perecederos necesitan conservación segura. No consumas una ensalada cuya cadena de frío se perdió.", False),
         ]),
    dict(name="Preparación para el parto", short="Camino al nacimiento", icon="✨", weeks="Antes del parto", focus="Preparar comidas y seguir las indicaciones del equipo",
         lesson="Estas elecciones son para los días previos al parto. Durante el trabajo de parto o antes de una cirugía, sigue las indicaciones del equipo sobre comidas y líquidos. Un alimento no inicia ni acelera el parto de forma segura.",
         foods=[
             item("Arroz integral", "🍚", "Recién cocido o refrigerado", "Aporta energía y fibra. Si lo guardas, refrigéralo pronto y recaliéntalo de forma segura."),
             item("Papa", "🥔", "Cocida", "Aporta energía. Puede acompañar una comida con proteína y verduras en los días previos al parto."),
             item("Banana", "🍌", "Madura, con manos limpias", "Es una opción de fruta que aporta energía. No reemplaza una alimentación variada."),
             item("Calabaza", "🎃", "Cocida", "Aporta carotenoides y variedad. Puede formar parte de comidas que prepares con anticipación y conserves bien."),
             item("Garbanzos", "🫘", "Bien cocidos", "Aportan proteína vegetal y fibra. Organizar comidas seguras facilita el cuidado después del nacimiento."),
             item("Infusión para inducir el parto", "🍵", "Sin valoración profesional", "No uses infusiones ni mezclas para provocar el parto por tu cuenta. Que algo sea natural no garantiza su seguridad.", False),
             item("Ayunar varios días", "🚫", "Para prepararse para el parto", "No hagas ayunos prolongados por tu cuenta. Sigue las instrucciones concretas del equipo que atiende tu parto.", False),
             item("Comer pese al ayuno indicado", "🍽️", "Antes de una cirugía programada", "Respeta el ayuno que indique el equipo para un procedimiento. Pregunta si no entiendes cuándo dejar de comer o beber.", False),
             item("Comida cocida sin refrigerar", "🍲", "Guardada hasta el día siguiente", "Las comidas preparadas necesitan refrigeración oportuna. Planifica la conservación, no solo la preparación.", False),
         ]),
    dict(name="Posparto", short="¡El bebé ha nacido!", icon="👶", weeks="Recién nacido", focus="Leche para el bebé; alimentación variada para la madre",
         lesson="El recién nacido no come frutas, papillas ni sólidos. La leche materna es el alimento recomendado; cuando se utiliza fórmula infantil, requiere preparación segura y orientación. Observa a quién va dirigida cada tarjeta.",
         foods=[
             item("Leche materna", "🤱", "A demanda, con apoyo si lo necesitas", "La leche materna aporta alimento y agua. Se recomienda lactancia exclusiva durante los primeros seis meses; busca apoyo si hay dolor o dificultades.", recipient="Bebé"),
             item("Fórmula infantil", "🍼", "Alternativa preparada según indicaciones", "Si se utiliza fórmula, elige una apropiada para lactantes y sigue exactamente las instrucciones del producto y del equipo de salud. No la diluyas ni la concentres.", recipient="Bebé"),
             item("Agua potable para mamá", "💧", "Disponible durante el día", "La madre puede beber agua potable según su sed y necesidades. Esto no significa ofrecer agua al recién nacido."),
             item("Comida variada para mamá", "🍲", "Legumbres, verduras y cereales", "La recuperación y la lactancia se acompañan de alimentación variada y apoyo práctico. No hace falta una dieta de un solo alimento."),
             item("Fruta lavada para mamá", "🍎", "Como parte de sus comidas", "La fruta aporta fibra y variedad a la madre. No se ofrece como papilla a un recién nacido."),
             item("Miel", "🍯", "Para calmar al recién nacido", "No des miel antes de los doce meses por el riesgo de botulismo, tampoco en el chupete o mezclada con leche.", False, "Bebé"),
             item("Papilla de frutas", "🥣", "Desde el nacimiento", "El recién nacido no necesita papillas. La alimentación complementaria comienza alrededor de los seis meses, según su desarrollo y orientación profesional.", False, "Bebé"),
             item("Agua o infusiones", "🍵", "Para la sed del recién nacido", "No sustituyas tomas por agua o infusiones. La leche materna cubre el agua que necesita; si se usa fórmula, prepárala exactamente como se indica.", False, "Bebé"),
             item("Leche de vaca", "🥛", "En lugar de leche materna o fórmula", "La leche de vaca no es la bebida principal adecuada antes de los doce meses. Consulta una alternativa de alimentación para lactantes.", False, "Bebé"),
         ]),
]

from obstetric_learning import add_obstetric_cases, SOURCE as OBSTETRIC_SOURCE
add_obstetric_cases(STAGES)
for stage, label in zip(STAGES, ('Mamá · Inicio del embarazo', 'Mamá · El embarazo avanza',
                                'Mamá · Crecemos juntos', 'Mamá · Preparándonos para el encuentro',
                                'Mamá y bebé · El primer abrazo')):
    stage['short'] = label

SOURCES = [
    OBSTETRIC_SOURCE,
    ("CDC · Comunicar tus preocupaciones", "https://www.cdc.gov/hearher/pregnant-postpartum/index.html"),
    ("OMS · Alimentación del lactante", "https://www.who.int/news-room/fact-sheets/detail/infant-and-young-child-feeding"),
    ("CDC · Alimentos seguros en el embarazo", "https://www.cdc.gov/food-safety/foods/pregnant-women.html"),
    ("CDC · Ácido fólico", "https://www.cdc.gov/folic-acid/about/intake-and-sources.html"),
    ("CDC · Preparación de fórmula", "https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html"),
    ("FDA · Pescado en el embarazo", "https://www.fda.gov/food/consumers/questions-answers-fdaepa-advice-about-eating-fish-those-who-might-become-or-are-pregnant-or"),
]


@st.cache_data(show_spinner=False)
def artwork_payload():
    # Pass binary illustrations through the component channel. Some Streamlit
    # ASGI versions return 500 for PNG responses from component static routes.
    return {name: base64.b64encode((ROOT / "assets" / filename).read_bytes()).decode("ascii")
            for name, filename in (("characters", "maternal-stages-v3.png"), ("foods", "foods-v2.png"))}


def show_game(database_path=None, participant=None):
    st.markdown('<style>@media(min-width:769px){.block-container{padding-top:12px!important;padding-bottom:0!important;max-width:1500px!important}}</style>', unsafe_allow_html=True)
    if st.session_state.get('game_content_version') != 'obstetric-actions-v4':
        st.session_state.nutrition_session = uuid.uuid4().hex
        st.session_state.game_content_version = 'obstetric-actions-v4'
        st.session_state.game_completed = False
        st.session_state.pop('journey_game_score', None)
    if "nutrition_session" not in st.session_state:
        st.session_state.nutrition_session = uuid.uuid4().hex
    # A stable component key preserves playback and the board across reruns.
    game = components.declare_component("gestation_nutrition", path=str(ROOT))
    result = game(stages=STAGES, session=st.session_state.nutrition_session, sources=SOURCES,
         artwork=artwork_payload(),
         key="gestation_nutrition_" + st.session_state.nutrition_session, default=None)
    if result is not None and database_path and participant:
        from learning_score import validated_game_score, save_score
        import sqlite3
        score = validated_game_score(result, STAGES)
        if score is not None:
            st.session_state.game_review = [
                dict(stage=STAGES[row['stage']]['name'], **STAGES[row['stage']]['foods'][row['index']])
                for row in result['history']
            ]
            try:
                save_score(database_path, participant, "game", score)
            except sqlite3.Error:
                st.warning("Tu recorrido está completo, pero no se pudo guardar el puntaje conjunto.")
            return score
    return None


def show_menu_music():
    music = (ROOT / "music.js").read_text(encoding="utf-8")
    components.html("""<!doctype html><html lang="es"><meta charset="utf-8">
    <style>body{margin:0;font:14px 'Segoe UI',sans-serif;color:#624471;display:flex;align-items:center;gap:12px;flex-wrap:wrap}button{font:inherit;border:1px solid #F2B8D3;background:#FFF1F7;border-radius:30px;padding:9px 16px;color:#624471;cursor:pointer}button:focus-visible{outline:3px solid #7c3aed}small{color:#697386}</style>
    <button id="menuMusic" type="button" aria-pressed="false">♫ Activar música</button><small>Melodía original · Jardín de vida</small>
    <script>""" + music + """
    const b=document.getElementById('menuMusic');
    function label(){b.textContent=Music.playing?'♫ Silenciar música':'♫ Activar música';b.setAttribute('aria-pressed',String(Music.playing));}
    b.onclick=async()=>{await Music.toggle();label();};
    Music.start().then(label);
    </script></html>""", height=65)


def menu_styles():
    st.markdown("""<style>
    .st-key-learning_menu div.stButton > button:first-child{background:#a52f6d!important;border:1px solid #8e275e!important;color:#fff!important;box-shadow:0 5px 14px #74294b20!important}
    .st-key-learning_menu div.stButton > button:first-child:disabled{background:#e6dce4!important;border-color:#cdbdca!important;color:#665761!important;box-shadow:none!important}
    .st-key-learning_menu button:disabled p{color:#665761!important}
    .st-key-learning_menu button:hover{background:#842356!important}
    .st-key-learning_menu button p{color:#fff!important}
    .st-key-learning_menu .menu-card{min-height:310px;padding:28px;border:1px solid #dfcedb;border-radius:24px;background:#fffafdeF;box-shadow:0 8px 25px #633d5a10;transition:transform .2s,box-shadow .2s}
    .st-key-learning_menu .menu-card:hover{transform:translateY(-3px);box-shadow:0 12px 30px #633d5a20}
    .st-key-learning_menu .menu-card.garden{background:linear-gradient(140deg,#fffafd,#f9e8f0);border-color:#d8adbf}
    .st-key-learning_menu .menu-icon{display:inline-flex;align-items:center;justify-content:center;width:68px;height:68px;border-radius:18px;background:#f8e1ec;color:#87335b;font-size:35px}
    .st-key-learning_menu .menu-icon img{width:54px;height:54px}
    .st-key-learning_menu .menu-card h2{font-size:1.65rem;line-height:1.25;color:#3e2940!important;margin:18px 0 12px}
    .st-key-learning_menu .menu-card p{font-size:.95rem;line-height:1.6;color:#554a5c!important}
    .st-key-learning_menu .menu-badge{float:right;background:#f6eaf1;color:#713d5c;border:1px solid #dfc5d5;border-radius:20px;padding:7px 10px;font-size:.72rem;font-weight:700}
    .st-key-learning_menu .menu-trail{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 24px}
    .st-key-learning_menu .menu-trail span{background:#fff8fc;border:1px solid #dec3d3;color:#653e58;border-radius:18px;padding:7px 12px;font-size:.8rem}
    @media(max-width:650px){.st-key-learning_menu .menu-card{min-height:0;padding:22px}.st-key-learning_menu .menu-badge{float:none;display:table;margin-top:12px}}
    @media(prefers-reduced-motion:reduce){.st-key-learning_menu *{transition:none!important}}
    .st-key-learning_menu .menu-card{position:relative;overflow:hidden;min-height:375px;border-width:2px;transition:transform .25s,box-shadow .25s;background:linear-gradient(145deg,#fff,#fff0f8);border-color:#eab4d1;box-shadow:0 12px 32px #86345d15}
    .st-key-learning_menu .menu-card.theory{border-top:6px solid #ae3377}
    .st-key-learning_menu .menu-card.garden{border-top:6px solid #237c73;border-color:#84c9bf;background:linear-gradient(140deg,#fafffd,#dff5ee)}
    .st-key-learning_menu .menu-card:hover{transform:translateY(-6px);box-shadow:0 18px 35px #633d5a25}
    .st-key-learning_menu .module-step{font-size:.78rem;font-weight:850;letter-spacing:1.7px;color:#9b2d66;margin-bottom:22px}
    .st-key-learning_menu .garden .module-step{color:#206e65}
    .st-key-learning_menu .module-detail{border-top:1px solid #cfa7c2;padding-top:14px;margin-top:18px;font-size:.82rem;font-weight:650;color:#6d3d59;line-height:1.5}
    .st-key-learning_menu .garden .module-detail{border-color:#9ac8bb;color:#245e56}
    .st-key-learning_menu .garden .menu-icon{background:#bce5d9}
    .st-key-learning_menu .menu-icon{animation:module-float 5s ease-in-out infinite}
    .st-key-learning_menu .garden .menu-icon{animation-delay:-2s}
    .st-key-learning_menu .menu-trail span{background:#fff;box-shadow:0 3px 9px #6d315510;border-color:#dfbdd1}
    @keyframes module-float{50%{transform:translateY(-5px) rotate(3deg)}}
    @media(max-width:650px){.st-key-learning_menu .menu-card{min-height:0}.st-key-learning_menu .module-step{margin-bottom:14px}}
    @media(prefers-reduced-motion:reduce){.st-key-learning_menu .menu-icon{animation:none}}
    </style>""", unsafe_allow_html=True)


def menu_logo(kind="game"):
    encoded = base64.b64encode((ROOT / ("test.svg" if kind == "test" else "logo.svg")).read_bytes()).decode("ascii")
    label = 'Test de conocimientos' if kind == 'test' else 'Nutrir una vida: cuidado y crecimiento'
    return f'<img src="data:image/svg+xml;base64,{encoded}" alt="{label}">'
