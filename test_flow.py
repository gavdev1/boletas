import sys
import os

# Ensure the root path is accessible to Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal
from persistencia.models import User, Seccion, Alumno, Materia, Calificacion, Boleta
from core.security import get_password_hash, create_access_token

def clear_test_data(db):
    print("Limpiando datos de prueba...")
    db.query(Boleta).filter(Boleta.anio_escolar == "TEST-YEAR").delete()
    db.query(Calificacion).filter(Calificacion.anio_escolar == "TEST-YEAR").delete()
    db.query(Materia).filter(Materia.nombre == "Materia de Prueba Técnica").delete()
    db.query(Alumno).filter(Alumno.cedula == "V-8888888").delete()
    db.query(Seccion).filter(Seccion.grado == 99).delete()
    db.commit()

def run():
    client = TestClient(app)
    db = SessionLocal()
    
    # 1. Login or bypass
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(username="admin", email="admin@test.com", hashed_password=get_password_hash("admin"))
        db.add(admin)
        db.commit()
    
    token = create_access_token(data={"sub": admin.username})
    headers = {"Authorization": f"Bearer {token}"}
    
    clear_test_data(db)

    try:
        print("=== TEST 1: Creando Sección ===")
        res = client.post("/secciones/", json={"grado": 99, "letra": "Z", "modalidad": "Técnica"}, headers=headers)
        assert res.status_code == 201, f"Fallo al crear sección: {res.text}"
        print("Sección creada exitosamente.")

        print("=== TEST 2: Creando Alumno ===")
        res = client.post("/alumnos/", json={
            "cedula": "V-8888888",
            "nombre": "Estudiante",
            "apellido": "Técnico",
            "grado": 99,
            "seccion": "Z",
            "modalidad": "Técnica",
            "numero_lista": 1
        }, headers=headers)
        assert res.status_code == 201, f"Fallo al crear alumno: {res.text}"
        alumno_id = res.json()["id"]
        print(f"Alumno creado exitosamente (ID: {alumno_id}).")

        print("=== TEST 3: Creando Materia ===")
        res = client.post("/materias/", json={"nombre": "Materia de Prueba Técnica", "grado": 99, "es_numerica": True, "modalidad": "Técnica"}, headers=headers)
        assert res.status_code == 201, f"Fallo al crear materia: {res.text}"
        materia_id = res.json()["id"]
        print(f"Materia creada exitosamente (ID: {materia_id}).")

        print("=== TEST 3.5: Probando Filtro GET /materias/ ===")
        res = client.get("/materias/?modalidad=Técnica", headers=headers)
        assert res.status_code == 200, f"Fallo al buscar materias x modalidad: {res.text}"
        materias_list = res.json()
        assert len(materias_list) == 1, "Debe haber exactamente 1 materia listada"
        assert materias_list[0]["modalidad"] == "Técnica", "La modalidad no coincide"
        print("Filtro GET /materias/?modalidad=... funciona perfectamente.")

        print("=== TEST 4: Registrando Calificaciones ===")
        for lapso, nota in [(1, 15), (2, 18), (3, 20)]:
            res = client.post("/calificaciones/", json={
                "alumno_id": alumno_id,
                "materia_id": materia_id,
                "lapso": lapso,
                "nota": nota,
                "anio_escolar": "TEST-YEAR"
            }, headers=headers)
            assert res.status_code == 200 or res.status_code == 201, f"Fallo al crear calificacion lapso {lapso}: {res.text}"
        print("Calificaciones Lapso 1, 2 y 3 registradas.")

        print("=== TEST 5: Generando Boleta ===")
        res = client.post("/boletas/", json={
            "alumno_id": alumno_id,
            "anio_escolar": "TEST-YEAR",
            "hasta_lapso": 3,
            "inasistencias_lapso_1": 2,
            "inasistencias_lapso_2": 0,
            "inasistencias_lapso_3": 1
        }, headers=headers)
        assert res.status_code == 201, f"Fallo al crear boleta: {res.text}"
        boleta_id = res.json()["id"]
        print(f"Boleta generada exitosamente (ID: {boleta_id}). La media global de la sección es: {res.json().get('media_seccion')}")

        print("=== TEST 6: Generando PDF ===")
        res = client.get(f"/boletas/{boleta_id}/pdf", headers=headers)
        assert res.status_code == 200, f"Fallo al generar PDF: {res.text}"
        assert res.headers["content-type"] == "application/pdf", "El archivo no es un PDF"
        
        pdf_path = r"C:\Users\stefa\.gemini\antigravity\brain\c1ef25e8-4cfa-4b95-8862-5b0f0b18e08e\boleta_tecnica_prueba.pdf"
        with open(pdf_path, "wb") as f:
            f.write(res.content)
            
        print(f"PDF generado con éxito y guardado en {pdf_path}")

    except AssertionError as e:
        print(f"\\n!!! ERROR EN EL TEST !!!\\n{e}")
    finally:
        # clear_test_data(db)  # <-- Comentado para que los datos queden guardados en SQLite
        db.close()

if __name__ == "__main__":
    run()
