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

SOURCES = [
    ("OMS · Alimentación del lactante", "https://www.who.int/news-room/fact-sheets/detail/infant-and-young-child-feeding"),
    ("CDC · Alimentos seguros en el embarazo", "https://www.cdc.gov/food-safety/foods/pregnant-women.html"),
    ("CDC · Ácido fólico", "https://www.cdc.gov/folic-acid/about/intake-and-sources.html"),
    ("CDC · Preparación de fórmula", "https://www.cdc.gov/infant-toddler-nutrition/formula-feeding/preparation-and-storage.html"),
    ("FDA · Pescado en el embarazo", "https://www.fda.gov/food/consumers/questions-answers-fdaepa-advice-about-eating-fish-those-who-might-become-or-are-pregnant-or"),
]


def show_game():
    if "nutrition_session" not in st.session_state:
        st.session_state.nutrition_session = uuid.uuid4().hex
    # A stable component key preserves playback and the board across reruns.
    game = components.declare_component("gestation_nutrition", path=str(ROOT))
    game(stages=STAGES, session=st.session_state.nutrition_session, sources=SOURCES,
         key="gestation_nutrition", default=None)


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
    .st-key-learning_menu .menu-card {position:relative;overflow:hidden;min-height:285px;
        border:1px solid #ecd7e8;border-radius:26px;padding:25px;
        background:linear-gradient(135deg,#fff9fc,#f7effb);box-shadow:0 12px 32px #75418212;
        transition:transform .2s,box-shadow .2s}
    .st-key-learning_menu .menu-card:hover {transform:translateY(-5px);box-shadow:0 20px 38px #ab6b9b25}
    .st-key-learning_menu .menu-card.garden {background:linear-gradient(135deg,#fff7ef,#edf8f0)}
    .st-key-learning_menu .menu-card .menu-icon {font-size:44px;display:inline-block;animation:menu-float 4s ease-in-out infinite}
    .st-key-learning_menu .menu-icon img {width:64px;height:64px;display:block}
    .st-key-learning_menu .menu-card h2 {font-size:1.65rem;line-height:1.2;margin:10px 0;color:#24324b}
    .st-key-learning_menu .menu-card p {font-size:.95rem;line-height:1.55;color:#677287}
    .st-key-learning_menu .menu-badge {float:right;padding:6px 11px;border-radius:30px;background:#ffffffbc;color:#80537d;font-size:.75rem;font-weight:800}
    .st-key-learning_menu .menu-trail {display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 24px}
    .st-key-learning_menu .menu-trail span {padding:7px 12px;border-radius:20px;background:#fff9;border:1px solid #eadce9;color:#786080;font-size:.8rem}
    @keyframes menu-float {50% {transform:translateY(-6px) rotate(4deg)}}
    @media(prefers-reduced-motion:reduce){.st-key-learning_menu *{animation:none!important;transition:none!important}}
    @media(max-width:650px){.st-key-learning_menu .menu-card{min-height:0;padding:20px}}
    </style>""", unsafe_allow_html=True)


def menu_logo():
    encoded = base64.b64encode((ROOT / "logo.svg").read_bytes()).decode("ascii")
    return f'<img src="data:image/svg+xml;base64,{encoded}" alt="Jardín de vida: cuidado y crecimiento">'
