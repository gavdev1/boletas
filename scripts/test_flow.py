import requests
import json
import os
import time
import random

BASE_URL = "http://localhost:8000"

def log_output(msg):
    with open("flow_log.txt", "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def run_test_flow():
    # Clear log
    if os.path.exists("flow_log.txt"):
        os.remove("flow_log.txt")
        
    log_output("--- 1. Login/Register ---")
    session = requests.Session()
    
    unique_suffix = int(time.time())
    
    login_data = {"username": f"testuser_{unique_suffix}", "password": "password123"}
    
    response = session.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code != 200:
        log_output("Login failed, attempting register...")
        reg_data = {
            "username": f"testuser_{unique_suffix}",
            "email": f"test_{unique_suffix}@example.com",
            "password": "password123"
        }
        res_reg = session.post(f"{BASE_URL}/auth/register", json=reg_data)
        if res_reg.status_code != 201:
            log_output(f"Failed to register: {res_reg.text}")
            return
        response = session.post(f"{BASE_URL}/auth/login", json=login_data)
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    session.headers.update(headers)
    log_output("Login successful! Token acquired.")

    log_output("\n--- 2. Create Seccion ---")
    seccion_data = {
        "grado": 2,
        "letra": "A",
        "modalidad": "Media General"
    }
    res_secc = session.post(f"{BASE_URL}/secciones/", json=seccion_data)
    if res_secc.status_code == 201:
        log_output(f"Created Seccion {seccion_data['grado']}-{seccion_data['letra']}")
    else:
        log_output(f"Failed to create Seccion (might already exist): {res_secc.text}")

    log_output("\n--- 3. Create Alumno ---")
    alumno_data = {
        "cedula": f"V-{unique_suffix}",
        "nombre": f"Estudiante_{unique_suffix}",
        "apellido": "Alemán",
        "grado": 2,
        "seccion": "A",
        "numero_lista": random.randint(1, 40),
        "modalidad": "Media General"
    }
    res_alum = session.post(f"{BASE_URL}/alumnos/", json=alumno_data)
    if res_alum.status_code == 201:
        alumno_id = res_alum.json()["id"]
        log_output(f"Created Alumno {alumno_data['nombre']} con ID: {alumno_id}")
    else:
        log_output(f"Failed to create Alumno: {res_alum.text}")
        return

    log_output("\n--- 4. Create Materia ---")
    materia_data = {
        "nombre": f"Biología {unique_suffix}",
        "grado": 2,
        "es_numerica": True,
        "modalidad": "Media General"
    }
    res_materia = session.post(f"{BASE_URL}/materias/", json=materia_data)
    if res_materia.status_code == 201:
        materia_id = res_materia.json()["id"]
        log_output(f"Created Materia {materia_data['nombre']} con ID: {materia_id}")
    else:
        log_output(f"Failed to create Materia: {res_materia.text}")
        return

    log_output("\n--- 5. Agregar Calificaciones ---")
    for lapso, nota in [(1, 15), (2, 16), (3, 18)]:
        calif_data = {
            "alumno_id": alumno_id,
            "materia_id": materia_id,
            "lapso": lapso,
            "nota": nota
        }
        res_calif = session.post(f"{BASE_URL}/calificaciones/", json=calif_data)
        if res_calif.status_code == 201:
            log_output(f"Added grade {nota} for lapso {lapso}")
        else:
            log_output(f"Failed to add grade for lapso {lapso}: {res_calif.text}")

    log_output("\n--- 6. Generar Boleta ---")
    boleta_data = {
        "alumno_id": alumno_id,
        "anio_escolar": "2024-2025",
        "grado": 2,
        "seccion": "A",
        "tipo_evaluacion": "Final",
        "hasta_lapso": 3
    }
    res_boleta = session.post(f"{BASE_URL}/boletas/", json=boleta_data)
    if res_boleta.status_code == 201:
        boleta_id = res_boleta.json()["id"]
        log_output(f"Boleta created with ID: {boleta_id}")
    else:
        log_output(f"Failed to create Boleta: {res_boleta.text}")
        return

    log_output("\n--- 7. Descargar y Guardar PDF ---")
    res_pdf = session.get(f"{BASE_URL}/boletas/{boleta_id}/pdf")
    if res_pdf.status_code == 200:
        pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "boleta_prueba.pdf")
        with open(pdf_path, "wb") as f:
            f.write(res_pdf.content)
        log_output(f"Successfully downloaded PDF to {pdf_path}")
    else:
        log_output(f"Failed to download PDF: {res_pdf.text}")

if __name__ == "__main__":
    run_test_flow()
