import streamlit as st
import numpy as np

from game_logic import inicializar_estado, obtener_puntajes, reiniciar_juego
from model import clasificar_perfil, obtener_dialogo_ia

# Configuración básica de la app
st.set_page_config(page_title="Videojuego Vocacional Inteligente", page_icon="🎮", layout="wide")

# ==========================================
# 3. INTERFAZ DEL JUEGO
# ==========================================
st.title("🎮 Videojuego Vocacional Inteligente: Promoción de Sistemas")
st.write("---")

inicializar_estado()

# Aquí empieza el flujo del juego, paso por paso
if st.session_state.paso_juego == 0:
    st.subheader("🛸 ¡Bienvenido a la Nave de Sistemas!")
    st.markdown("Responde preguntas reales con distintos formatos para que el sistema detecte tus intereses técnicos y humanos.")
    nombre = st.text_input("Ingresa tu nombre de jugador:", value=st.session_state.nombre_usuario)
    if st.button("Iniciar Misión 🚀"):
        if nombre:
            st.session_state.nombre_usuario = nombre
            st.session_state.paso_juego = 1
            st.rerun()
        else:
            st.error("Por favor, introduce tu nombre primero.")

elif st.session_state.paso_juego == 1:
    st.subheader("Paso 1/8: Programación y lógica")
    st.write("¿Qué tanto disfrutas resolver problemas con código y matemáticas?")
    st.session_state.puntos_prog = st.slider("Pasión por programar:", 1, 10, st.session_state.puntos_prog)
    st.session_state.puntos_log = st.slider("Gusto por el análisis lógico y numérico:", 1, 10, st.session_state.puntos_log)
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 2
        st.rerun()

elif st.session_state.paso_juego == 2:
    st.subheader("Paso 2/8: Seguridad y redes")
    st.write("Elige la actividad técnica que más te llama la atención.")
    opcion_seg = st.radio("¿Qué prefieres?", [
        "Defender sistemas y redes",
        "Configurar servidores en la nube",
        "Probar aplicaciones contra ataques",
        "Detectar fallos en infraestructuras"
    ])
    if opcion_seg == "Defender sistemas y redes":
        st.session_state.puntos_seg = 9
        st.session_state.puntos_os = 7
        st.session_state.puntos_cloud = 6
    elif opcion_seg == "Configurar servidores en la nube":
        st.session_state.puntos_cloud = 9
        st.session_state.puntos_backend = 7
        st.session_state.puntos_os = 7
    elif opcion_seg == "Probar aplicaciones contra ataques":
        st.session_state.puntos_test = 8
        st.session_state.puntos_seg = 7
    else:
        st.session_state.puntos_os = 8
        st.session_state.puntos_backend = 6
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 3
        st.rerun()

elif st.session_state.paso_juego == 3:
    st.subheader("Paso 3/8: Diseño y experiencia")
    st.write("¿Qué aspecto del diseño te interesa más?")
    opcion_ui = st.selectbox("Selecciona una preferencia:", [
        "Crear interfaces atractivas",
        "Mejorar la experiencia de usuario",
        "Diseñar pantallas fáciles de usar",
        "Conectar la interfaz con el backend"
    ])
    if opcion_ui == "Crear interfaces atractivas":
        st.session_state.puntos_frontend = 9
        st.session_state.puntos_ux = 8
    elif opcion_ui == "Mejorar la experiencia de usuario":
        st.session_state.puntos_ux = 9
        st.session_state.puntos_frontend = 7
    elif opcion_ui == "Diseñar pantallas fáciles de usar":
        st.session_state.puntos_ux = 8
        st.session_state.puntos_frontend = 7
    else:
        st.session_state.puntos_frontend = 8
        st.session_state.puntos_backend = 7
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 4
        st.rerun()

elif st.session_state.paso_juego == 4:
    st.subheader("Paso 4/8: Datos y bases")
    st.write("¿Qué tanto te interesa trabajar con información y bases de datos?")
    st.session_state.puntos_db = st.slider("Interés en bases de datos:", 1, 10, st.session_state.puntos_db)
    st.session_state.puntos_da = st.slider("Interés en análisis de datos:", 1, 10, st.session_state.puntos_da)
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 5
        st.rerun()

elif st.session_state.paso_juego == 5:
    st.subheader("Paso 5/8: Pruebas y gestión")
    st.write("Selecciona todas las actividades que te gustaría hacer en un proyecto.")
    opciones = st.multiselect("Selecciona todas las que apliquen:", [
        "Probar la calidad del software",
        "Planificar tareas de equipo",
        "Detectar y corregir fallos",
        "Comunicar avances con compañeros"
    ])
    if "Probar la calidad del software" in opciones:
        st.session_state.puntos_test = max(st.session_state.puntos_test, 8)
    if "Planificar tareas de equipo" in opciones:
        st.session_state.puntos_pm = max(st.session_state.puntos_pm, 8)
    if "Detectar y corregir fallos" in opciones:
        st.session_state.puntos_os = max(st.session_state.puntos_os, 7)
    if "Comunicar avances con compañeros" in opciones:
        st.session_state.puntos_pm = max(st.session_state.puntos_pm, 7)
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 6
        st.rerun()

elif st.session_state.paso_juego == 6:
    st.subheader("Paso 6/8: Tipo de proyecto")
    st.write("Elige el proyecto que más te motiva.")
    tipo_proyecto = st.radio("Selecciona una opción:", [
        "Crear una app móvil para usuarios",
        "Construir un sistema seguro en la nube",
        "Montar un modelo de datos para una empresa",
        "Diseñar un portal web interactivo"
    ])
    if tipo_proyecto == "Crear una app móvil para usuarios":
        st.session_state.puntos_frontend = 10
        st.session_state.puntos_backend = 9
        st.session_state.puntos_prog = max(st.session_state.puntos_prog, 8)
    elif tipo_proyecto == "Construir un sistema seguro en la nube":
        st.session_state.puntos_cloud = 10
        st.session_state.puntos_seg = 9
    elif tipo_proyecto == "Montar un modelo de datos para una empresa":
        st.session_state.puntos_da = 10
        st.session_state.puntos_db = 9
        st.session_state.puntos_dat = max(st.session_state.puntos_dat, 8)
    else:
        st.session_state.puntos_ux = 9
        st.session_state.puntos_frontend = 8
        st.session_state.puntos_prog = max(st.session_state.puntos_prog, 7)
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 7
        st.rerun()

elif st.session_state.paso_juego == 7:
    st.subheader("Paso 7/8: Arquitectura, consultoría e IA")
    st.write("Elige qué camino te inspira más en tecnología.")
    opcion_avanzada = st.radio("Selecciona una opción:", [
        "Diseñar la arquitectura de sistemas y soluciones técnicas",
        "Asesorar empresas en tecnología y procesos digitales",
        "Aplicar inteligencia artificial en proyectos reales",
        "Crear modelos de Machine Learning que aprendan de datos"
    ])
    if opcion_avanzada == "Diseñar la arquitectura de sistemas y soluciones técnicas":
        st.session_state.puntos_arch = 10
        st.session_state.puntos_backend = 9
        st.session_state.puntos_cloud = 8
    elif opcion_avanzada == "Asesorar empresas en tecnología y procesos digitales":
        st.session_state.puntos_consult = 10
        st.session_state.puntos_pm = 9
        st.session_state.puntos_log = 8
    elif opcion_avanzada == "Aplicar inteligencia artificial en proyectos reales":
        st.session_state.puntos_ai = 10
        st.session_state.puntos_da = 9
        st.session_state.puntos_db = 8
    else:
        st.session_state.puntos_ml = 10
        st.session_state.puntos_ai = 9
        st.session_state.puntos_dat = 8
    if st.button("Siguiente ➡️"):
        st.session_state.paso_juego = 8
        st.rerun()

elif st.session_state.paso_juego == 8:
    st.subheader("🎯 ¡Misión Cumplida! Tu Perfil Vocacional ha sido Clasificado")

    puntajes = obtener_puntajes()
    resultado = clasificar_perfil(puntajes)
    top2_perfiles = resultado['top2_perfiles']
    perfiles_asignados = resultado['perfiles_asignados']
    prog = puntajes['prog']
    log = puntajes['log']
    dat = puntajes['dat']
    ux = puntajes['ux']
    cloud = puntajes['cloud']
    seg = puntajes['seg']
    db = puntajes['db']
    da = puntajes['da']
    osn = puntajes['osn']
    test = puntajes['test']
    pm = puntajes['pm']
    backend = puntajes['backend']
    frontend = puntajes['frontend']
    arch = puntajes['arch']
    consult = puntajes['consult']
    ai = puntajes['ai']
    ml = puntajes['ml']

    st.metric(label="Perfiles más fuertes", value=", ".join(top2_perfiles))
    st.write("---")
    st.write("**Top 1:**", top2_perfiles[0])
    st.write("**Top 2:**", top2_perfiles[1])
    st.write("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Puntajes principales usados:**")
        st.write(f"• Programación: {prog}")
        st.write(f"• Razonamiento lógico: {log}")
        st.write(f"• Seguridad: {seg}")
        st.write(f"• UX / Interfaz: {ux}")
        st.write(f"• Cloud: {cloud}")
    with col2:
        st.markdown("**Otras habilidades:**")
        st.write(f"• Bases de datos: {db}")
        st.write(f"• Análisis de datos: {da}")
        st.write(f"• Testing: {test}")
        st.write(f"• Gestión / PM: {pm}")
        st.write(f"• Arquitectura de software: {arch}")
        st.write(f"• Consultoría tecnológica: {consult}")
        st.write(f"• Inteligencia Artificial: {ai}")
        st.write(f"• Machine Learning: {ml}")
        st.write(f"• Backend: {backend}")
        st.write(f"• Frontend: {frontend}")

    st.subheader("🤖 Mensaje Dinámico de la IA Narradora:")
    with st.spinner("Generando tu mensaje..."):
        mensaje_personalizado = obtener_dialogo_ia(", ".join(perfiles_asignados), st.session_state.nombre_usuario)
    st.info(mensaje_personalizado)

    if st.button("Jugar de Nuevo 🔄"):
        reiniciar_juego()
        st.rerun()