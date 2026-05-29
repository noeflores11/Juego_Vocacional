import streamlit as st


def inicializar_estado():
    """Aquí se ponen los valores base del juego para que no se pierdan entre pantallas."""
    if 'paso_juego' not in st.session_state:
        st.session_state.paso_juego = 0
    if 'nombre_usuario' not in st.session_state:
        st.session_state.nombre_usuario = ''

    valores = {
        'puntos_prog': 5,
        'puntos_log': 5,
        'puntos_seg': 5,
        'puntos_dat': 5,
        'puntos_ux': 5,
        'puntos_cloud': 5,
        'puntos_db': 5,
        'puntos_da': 5,
        'puntos_os': 5,
        'puntos_test': 5,
        'puntos_pm': 5,
        'puntos_backend': 5,
        'puntos_frontend': 5,
        'puntos_arch': 5,
        'puntos_consult': 5,
        'puntos_ai': 5,
        'puntos_ml': 5,
        'puntos_intereses': [],
        'respuestas': [0, 0, 0, 0, 0],
    }

    for clave, valor in valores.items():
        if clave not in st.session_state:
            st.session_state[clave] = valor


def obtener_puntajes():
    """Esta función trae los puntajes actuales para usarlos al final del juego."""
    return {
        'prog': st.session_state.get('puntos_prog', 5),
        'log': st.session_state.get('puntos_log', 5),
        'dat': st.session_state.get('puntos_dat', 5),
        'ux': st.session_state.get('puntos_ux', 5),
        'cloud': st.session_state.get('puntos_cloud', 5),
        'seg': st.session_state.get('puntos_seg', 5),
        'db': st.session_state.get('puntos_db', 5),
        'da': st.session_state.get('puntos_da', 5),
        'osn': st.session_state.get('puntos_os', 5),
        'test': st.session_state.get('puntos_test', 5),
        'pm': st.session_state.get('puntos_pm', 5),
        'backend': st.session_state.get('puntos_backend', 5),
        'frontend': st.session_state.get('puntos_frontend', 5),
        'arch': st.session_state.get('puntos_arch', 5),
        'consult': st.session_state.get('puntos_consult', 5),
        'ai': st.session_state.get('puntos_ai', 5),
        'ml': st.session_state.get('puntos_ml', 5),
    }


def reiniciar_juego():
    """Aquí se resetea todo para volver a jugar desde cero."""
    st.session_state.paso_juego = 0
    st.session_state.nombre_usuario = ''
    st.session_state.puntos_prog = 5
    st.session_state.puntos_log = 5
    st.session_state.puntos_seg = 5
    st.session_state.puntos_dat = 5
    st.session_state.puntos_ux = 5
    st.session_state.puntos_cloud = 5
    st.session_state.puntos_db = 5
    st.session_state.puntos_da = 5
    st.session_state.puntos_os = 5
    st.session_state.puntos_test = 5
    st.session_state.puntos_pm = 5
    st.session_state.puntos_backend = 5
    st.session_state.puntos_frontend = 5
    st.session_state.puntos_arch = 5
    st.session_state.puntos_consult = 5
    st.session_state.puntos_ai = 5
    st.session_state.puntos_ml = 5
    st.session_state.puntos_intereses = []
    st.session_state.respuestas = [0, 0, 0, 0, 0]
