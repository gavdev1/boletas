import requests
import os

BASE_URL = "http://127.0.0.1:8000"

def verify_full_table():
    # 1. Login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "director", "password": "password123"})
    if resp.status_code != 200:
        print(f"❌ Login fallido: {resp.text}")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Add some grades if needed (seed should have them)
    # 3. Create Boleta for Lapso 1 ONLY
    print("--- 📄 Generando Boleta Lapso 1 (Expected Full Table with L2/L3 empty) ---")
    boleta_data = {
        "alumno_id": 1,
        "hasta_lapso": 1,
        "tipo_evaluacion": "Primer Lapso - Estructura Completa",
        "observaciones": "La tabla debe verse completa aunque solo haya notas en L1."
    }
    resp = requests.post(f"{BASE_URL}/boletas/", json=boleta_data, headers=headers)
    if resp.status_code != 201:
        print(f"❌ Error al crear boleta: {resp.text}")
        return
        
    boleta_id = resp.json()["id"]
    print(f"✅ Boleta Creada: ID {boleta_id}")
    
    # Download PDF
    pdf_resp = requests.get(f"{BASE_URL}/boletas/{boleta_id}/pdf", headers=headers)
    filename = "boleta_l1_full_table.pdf"
    with open(filename, "wb") as f:
        f.write(pdf_resp.content)
    print(f"💾 {filename} guardado.")

if __name__ == "__main__":
    if not os.path.exists("outputs"): os.makedirs("outputs")
    os.chdir("outputs")
    verify_full_table()
