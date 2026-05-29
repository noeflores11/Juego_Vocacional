import os
import random

import numpy as np
import requests
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier


@st.cache_resource
def entrenar_modelo_vocacional():
    """Aquí se entrena el modelo que va a clasificar el perfil vocacional del jugador."""
    np.random.seed(42)
    X = np.random.randint(1, 11, size=(400, 17))
    y = []

    for alumno in X:
        (prog_sim, log_sim, seg_sim, dat_sim, ux_sim, cloud_sim,
         db_sim, data_analysis_sim, os_net_sim, testing_sim, pm_sim,
         backend_sim, frontend_sim, arch_sim, consult_sim, ai_sim, ml_sim) = alumno

        score_dev = prog_sim * 2 + ux_sim + backend_sim + frontend_sim + int(pm_sim / 2)
        score_sec = seg_sim * 2 + os_net_sim + cloud_sim + int(testing_sim / 2)
        score_data = data_analysis_sim * 2 + db_sim + log_sim + int(ml_sim / 2)
        score_support = os_net_sim + testing_sim + db_sim + int(seg_sim / 2) + int(cloud_sim / 2)
        score_arch = arch_sim * 3 + backend_sim + cloud_sim + pm_sim
        score_consult = consult_sim * 3 + pm_sim + log_sim + ux_sim
        score_ai = ai_sim * 3 + ml_sim + data_analysis_sim + db_sim
        score_ml = ml_sim * 3 + ai_sim + data_analysis_sim + prog_sim

        etiqueta_dev = int(score_dev >= 16 or (prog_sim >= 8 and ux_sim >= 6))
        etiqueta_sec = int(score_sec >= 15 or seg_sim >= 8)
        etiqueta_data = int(score_data >= 15 or data_analysis_sim >= 7)
        etiqueta_support = int(score_support >= 14 or os_net_sim >= 7)
        etiqueta_arch = int(score_arch >= 14 or arch_sim >= 8)
        etiqueta_consult = int(score_consult >= 14 or consult_sim >= 8)
        etiqueta_ai = int(score_ai >= 14 or ai_sim >= 8)
        etiqueta_ml = int(score_ml >= 14 or ml_sim >= 8)

        etiquetas = [etiqueta_dev, etiqueta_sec, etiqueta_data, etiqueta_support,
                     etiqueta_arch, etiqueta_consult, etiqueta_ai, etiqueta_ml]

        if sum(etiquetas) == 0:
            mayor = np.argmax([score_dev, score_sec, score_data, score_support,
                               score_arch, score_consult, score_ai, score_ml])
            etiquetas[mayor] = 1

        y.append(etiquetas)

    y = np.array(y)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)
    modelo = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    modelo.fit(X_train, y_train)
    return modelo


modelo_ia = entrenar_modelo_vocacional()


def generar_mensaje_plantilla(perfil, nombre):
    plantillas = [
        f"¡Felicidades {nombre}! Tu perfil apunta hacia {perfil}, una ruta muy prometedora en tecnología.",
        f"Muy bien, {nombre}. {perfil} es un camino excelente para tu forma de pensar y resolver problemas.",
        f"Excelente trabajo, {nombre}. {perfil} combina creatividad, lógica y oportunidades reales de crecimiento.",
    ]
    return random.choice(plantillas)


def obtener_dialogo_ia(perfil, nombre):
    """Esta parte genera un mensaje motivador con IA, si la API responde bien."""
    API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    prompt = (
        "<|system|>\n"
        "Eres el Mentor Vocacional de la Universidad de Sistemas. Sé breve, motivador y habla en español."
        "<|user|>\n"
        f"Felicita a {nombre} porque su perfil ideal es: {perfil}. Dile por qué es una excelente carrera en 2 renglones."
        "<|assistant|>\n"
    )

    try:
        headers = {}
        hf_token = os.environ.get('HF_API_KEY') or os.environ.get('HUGGINGFACE_API_KEY')
        if hf_token:
            headers['Authorization'] = f'Bearer {hf_token}'

        response = requests.post(API_URL, headers=headers or None,
                                 json={'inputs': prompt, 'parameters': {'max_new_tokens': 100}},
                                 timeout=6)
        res_json = response.json()

        if isinstance(res_json, list) and len(res_json) and isinstance(res_json[0], dict):
            texto = res_json[0].get('generated_text') or res_json[0].get('text') or str(res_json[0])
        elif isinstance(res_json, dict):
            texto = res_json.get('generated_text') or res_json.get('text') or str(res_json)
        else:
            texto = str(res_json)

        if '<|assistant|>' in texto:
            texto = texto.split('<|assistant|>\n')[-1]

        return texto.strip() or generar_mensaje_plantilla(perfil, nombre)
    except Exception:
        return generar_mensaje_plantilla(perfil, nombre)


def calcular_puntajes_perfil(scores):
    """Calcula una puntuación heurística para cada perfil usando las respuestas del jugador."""
    score_dev = scores['prog'] * 2 + scores['ux'] + scores['backend'] + scores['frontend'] + int(scores['pm'] / 2)
    score_sec = scores['seg'] * 2 + scores['osn'] + scores['cloud'] + int(scores['test'] / 2)
    score_data = scores['da'] * 2 + scores['db'] + scores['log'] + int(scores['ml'] / 2)
    score_support = scores['osn'] + scores['test'] + scores['db'] + int(scores['seg'] / 2) + int(scores['cloud'] / 2)
    score_arch = scores['arch'] * 3 + scores['backend'] + scores['cloud'] + scores['pm']
    score_consult = scores['consult'] * 3 + scores['pm'] + scores['log'] + scores['ux']
    score_ai = scores['ai'] * 3 + scores['ml'] + scores['da'] + scores['db']
    score_ml = scores['ml'] * 3 + scores['ai'] + scores['da'] + scores['prog']

    return {
        'Desarrollo de Software': score_dev,
        'Ciberseguridad': score_sec,
        'Ciencia de Datos / IA': score_data,
        'Soporte Tecnológico y Redes': score_support,
        'Arquitectura de software / soluciones': score_arch,
        'Consultoría tecnológica': score_consult,
        'Inteligencia artificial aplicada': score_ai,
        'Machine Learning': score_ml,
    }


def clasificar_perfil(scores):
    """Aquí se sacan los perfiles que más encajan con las respuestas del jugador."""
    puntajes = calcular_puntajes_perfil(scores)
    perfiles_con_proba = sorted(puntajes.items(), key=lambda item: item[1], reverse=True)

    top2_perfiles = [perfil for perfil, _ in perfiles_con_proba[:2]]
    perfiles_asignados = top2_perfiles

    return {
        'top2_perfiles': top2_perfiles,
        'perfiles_asignados': perfiles_asignados,
        'perfiles_con_proba': perfiles_con_proba,
        'datos_jugador': None,
    }
