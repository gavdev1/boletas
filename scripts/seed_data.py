import requests
import json
import time
import os

BASE_URL = "http://127.0.0.1:8000"

def safe_post(url, json_data, headers=None):
    resp = requests.post(url, json=json_data, headers=headers)
    if resp.status_code not in [200, 201]:
        print(f"❌ Error en POST {url} ({resp.status_code}): {resp.text}")
        return None
    return resp.json()

def seed_system():
    print("--- 🚀 Iniciando Población Dinámica del Sistema ---")
    
    # 1. Registrar y Loguear Admin
    requests.post(f"{BASE_URL}/auth/register", json={"username": "director", "email": "director@escuela.com", "password": "password123"})
    login = safe_post(f"{BASE_URL}/auth/login", {"username": "director", "password": "password123"})
    if not login: return
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Autenticación exitosa.")

    # 2. Configuración del Plantel
    config = {
        "nombre_plantel": "U.E. Colegio Las Acacias",
        "direccion_plantel": "Av. Principal Los Mangos, Valencia",
        "anio_escolar_actual": "2024-2025",
        "profesor_guia_default": "Prof. Roberto Gómez"
    }
    safe_post(f"{BASE_URL}/configuracion/", config, headers)
    print("✅ Configuración del plantel establecida.")

    # 3. Crear 8 Materias
    materias_nombres = [
        "Matemáticas", "Castellano", "G.H.C", "Inglés", 
        "Ciencias Naturales", "Arte y Patrimonio", "Educación Física", "Orientación"
    ]
    materias_ids = []
    for nombre in materias_nombres:
        m = safe_post(f"{BASE_URL}/materias/", {"nombre": nombre, "grado": 1, "es_numerica": True}, headers)
        if m: materias_ids.append(m["id"])
    print(f"✅ {len(materias_ids)} Materias creadas.")

    # 4. Crear 5 Alumnos
    alumnos_data = [
        {"cedula": "V-30000001", "nombre": "Andrés", "apellido": "Bello", "numero_lista": 1},
        {"cedula": "V-30000002", "nombre": "Simón", "apellido": "Rodríguez", "numero_lista": 2},
        {"cedula": "V-30000003", "nombre": "Luisa", "apellido": "Cáceres", "numero_lista": 3},
        {"cedula": "V-30000004", "nombre": "Josefa", "apellido": "Camejo", "numero_lista": 4},
        {"cedula": "V-30000005", "nombre": "Francisco", "apellido": "Miranda", "numero_lista": 5},
    ]
    alumnos_ids = []
    for data in alumnos_data:
        data.update({"grado": 1, "seccion": "A"})
        al = safe_post(f"{BASE_URL}/alumnos/", data, headers)
        if al: 
            alumnos_ids.append(al["id"])
            print(f"DEBUG: Alumno creado con ID {al['id']}")
    print(f"✅ {len(alumnos_ids)} Alumnos inscritos en 1ero 'A'.")

    # 5. Cargar Notas (Lapsos 1, 2 y 3)
    import random
    print("⏳ Cargando notas para los 3 lapsos (esto puede tardar unos segundos)...")
    for al_id in alumnos_ids:
        for mat_id in materias_ids:
            # Notas aleatorias entre 12 y 20 para que se vea real
            nota1 = random.randint(12, 20)
            nota2 = random.randint(12, 20)
            nota3 = random.randint(12, 20)
            safe_post(f"{BASE_URL}/calificaciones/", {"alumno_id": al_id, "materia_id": mat_id, "lapso": 1, "nota": nota1}, headers)
            safe_post(f"{BASE_URL}/calificaciones/", {"alumno_id": al_id, "materia_id": mat_id, "lapso": 2, "nota": nota2}, headers)
            safe_post(f"{BASE_URL}/calificaciones/", {"alumno_id": al_id, "materia_id": mat_id, "lapso": 3, "nota": nota3}, headers)
    print("✅ Notas cargadas exitosamente (incluyendo 3er lapso).")

    # 6. Generar Boletas Automáticas
    for al_id in alumnos_ids:
        # Generar una del 1er lapso, una del 2do y una del 3ero (Final)
        safe_post(f"{BASE_URL}/boletas/", {"alumno_id": al_id, "hasta_lapso": 1, "tipo_evaluacion": "Primer Lapso"}, headers)
        safe_post(f"{BASE_URL}/boletas/", {"alumno_id": al_id, "hasta_lapso": 2, "tipo_evaluacion": "Acumulativa L1+L2"}, headers)
        safe_post(f"{BASE_URL}/boletas/", {"alumno_id": al_id, "hasta_lapso": 3, "tipo_evaluacion": "Final Año Escolar"}, headers)
    print("✅ 15 Boletas generadas (5 para cada periodo acumulativo).")

    print("\n✨ ¡SISTEMA POBLADO CON ÉXITO! ✨")
    print("Puedes ir a Swagger (/docs) para ver los resultados o descargar los PDFs.")

if __name__ == "__main__":
    seed_system()
