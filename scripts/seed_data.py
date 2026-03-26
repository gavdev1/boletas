import requests
import json
import time
import os
import random

BASE_URL = "http://127.0.0.1:8000"

def safe_post(url, json_data, headers=None):
    try:
        resp = requests.post(url, json=json_data, headers=headers)
        if resp.status_code not in [200, 201]:
            print(f"❌ Error en POST {url} ({resp.status_code}): {resp.text}")
            return None
        return resp.json()
    except Exception as e:
        print(f"❌ Excepción en POST {url}: {e}")
        return None

def seed_system():
    print("--- 🚀 Iniciando Población Dinámica del Sistema (Versión Extendida) ---")
    
    # 1. Registrar y Loguear Admin
    requests.post(f"{BASE_URL}/auth/register", json={"username": "director", "email": "director@escuela.com", "password": "password123"})
    login = safe_post(f"{BASE_URL}/auth/login", {"username": "director", "password": "password123"})
    if not login: 
        print("❌ Error de comunicación con el servidor. ¿Está el backend encendido?")
        return
        
    token = login["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Autenticación exitosa.")

    # 2. Configuración del Plantel
    config = {
        "nombre_plantel": "U.E. Colegio Las Acacias",
        "direccion_plantel": "Av. Principal Los Mangos, Valencia, Venezuela",
        "anio_escolar_actual": "2024-2025",
        "profesor_guia_default": "Prof. Roberto Gómez"
    }
    safe_post(f"{BASE_URL}/configuracion/", config, headers)
    print("✅ Configuración del plantel establecida.")

    # 3. Crear Secciones
    secciones_data = [
        {"grado": 1, "letra": "A", "modalidad": "Media General"},
        {"grado": 1, "letra": "B", "modalidad": "Media General"},
        {"grado": 2, "letra": "A", "modalidad": "Media General"},
        {"grado": 3, "letra": "A", "modalidad": "Media General"},
        {"grado": 4, "letra": "A", "modalidad": "Técnica"},
        {"grado": 5, "letra": "A", "modalidad": "Técnica"},
    ]
    for s in secciones_data:
        s["anio_escolar"] = "2024-2025"
        safe_post(f"{BASE_URL}/secciones/", s, headers)
    print("✅ Secciones creadas.")

    # 4. Crear Materias (Para 1ero y 4to grado)
    materias_1ro = [
        "Matemáticas I", "Castellano I", "G.H.C I", "Inglés I", 
        "Ciencias Naturales I", "Arte y Patrimonio", "Educación Física", "Orientación"
    ]
    materias_4to = [
        "Matemáticas IV", "Castellano IV", "Física I", "Química I", 
        "Dibujo Técnico", "Informática", "Educación Física", "Inglés IV"
    ]
    
    materias_ids_1ro = []
    for nombre in materias_1ro:
        m = safe_post(f"{BASE_URL}/materias/", {"nombre": nombre, "grado": 1, "es_numerica": True, "modalidad": "Media General"}, headers)
        if m: materias_ids_1ro.append(m["id"])
        
    materias_ids_4to = []
    for nombre in materias_4to:
        m = safe_post(f"{BASE_URL}/materias/", {"nombre": nombre, "grado": 4, "es_numerica": True, "modalidad": "Técnica"}, headers)
        if m: materias_ids_4to.append(m["id"])
    print(f"✅ Materias creadas para 1° y 4° grado.")

    # 5. Crear Alumnos
    alumnos_info = [
        {"cedula": "V-30000001", "nombre": "Andrés", "apellido": "Bello", "numero_lista": 1, "grado": 1, "seccion": "A", "modalidad": "Media General", "lugar_nacimiento": "Caracas", "estado_nacimiento": "Distrito Capital"},
        {"cedula": "V-30000002", "nombre": "Simón", "apellido": "Rodríguez", "numero_lista": 2, "grado": 1, "seccion": "A", "modalidad": "Media General", "lugar_nacimiento": "Caracas", "estado_nacimiento": "Distrito Capital"},
        {"cedula": "V-30000003", "nombre": "Luisa", "apellido": "Cáceres", "numero_lista": 3, "grado": 1, "seccion": "B", "modalidad": "Media General", "lugar_nacimiento": "La Asunción", "estado_nacimiento": "Nueva Esparta"},
        {"cedula": "V-30000004", "nombre": "Josefa", "apellido": "Camejo", "numero_lista": 4, "grado": 4, "seccion": "A", "modalidad": "Técnica", "lugar_nacimiento": "Coro", "estado_nacimiento": "Falcón"},
        {"cedula": "V-30000005", "nombre": "Francisco", "apellido": "Miranda", "numero_lista": 5, "grado": 4, "seccion": "A", "modalidad": "Técnica", "lugar_nacimiento": "Caracas", "estado_nacimiento": "Distrito Capital"},
    ]
    
    alumnos_creados = []
    for data in alumnos_info:
        data["fecha_nacimiento"] = "2010-01-01"
        data["nombre_representante"] = "Representante Legal"
        data["telefono_representante"] = "+58 412-1234567"
        data["correo_representante"] = f"rep_{data['cedula']}@ejemplo.com"
        data["direccion_representante"] = "Dirección de prueba, Valencia"
        data["correo_estudiante"] = f"alumno_{data['cedula']}@ejemplo.com"
        data["codigo"] = f"AL-{data['cedula']}"
        al = safe_post(f"{BASE_URL}/alumnos/", data, headers)
        if al: 
            alumnos_creados.append({"id": al["id"], "grado": data["grado"]})
    print(f"✅ {len(alumnos_creados)} Alumnos inscritos.")

    # 6. Cargar Notas
    print("⏳ Cargando notas para todos los lapsos...")
    for al_obj in alumnos_creados:
        al_id = al_obj["id"]
        grado = al_obj["grado"]
        materias_a_cargar = materias_ids_1ro if grado == 1 else materias_ids_4to
        
        for mat_id in materias_a_cargar:
            for lapso in [1, 2, 3]:
                nota = random.randint(10, 20)
                safe_post(f"{BASE_URL}/calificaciones/", {
                    "alumno_id": al_id, 
                    "materia_id": mat_id, 
                    "lapso": lapso, 
                    "nota": nota,
                    "anio_escolar": "2024-2025"
                }, headers)
    print("✅ Calificaciones cargadas exitosamente.")

    # 7. Crear Tareas de Ejemplo
    tareas_data = [
        {"titulo": "Cargar notas del 1er Lapso", "contenido": "Revisar planillas de 1ero A.", "completada": True},
        {"titulo": "Generar boletas finales", "contenido": "Esperar aprobación del consejo.", "completada": False},
        {"titulo": "Reunión de representantes", "contenido": "Viernes 25 de Octubre.", "completada": False},
    ]
    for t in tareas_data:
        safe_post(f"{BASE_URL}/tareas/", t, headers)
    print("✅ Tareas de ejemplo creadas.")

    # 8. Generar Boletas Automáticas (Solo para algunos)
    print("⏳ Generando boletas de prueba...")
    for i in range(min(3, len(alumnos_creados))):
        al_obj = alumnos_creados[i]
        safe_post(f"{BASE_URL}/boletas/", {
            "alumno_id": al_obj["id"], 
            "hasta_lapso": 2, 
            "tipo_evaluacion": "Parcial L1+L2",
            "observaciones": "Promovido satisfactoriamente."
        }, headers)
        
    print("✅ Boletas generadas.")

    print("\n✨ ¡Población de datos extendida FINALIZADA con éxito! ✨")

if __name__ == "__main__":
    seed_system()
