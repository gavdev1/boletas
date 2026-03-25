import requests
import os

BASE_URL = "http://127.0.0.1:8000"

def test_cumulative_pdf():
    # 1. Login
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": "director", "password": "password123"})
    if resp.status_code != 200:
        print(f"❌ Login fallido: {resp.text}")
        return
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # ID del alumno a probar (debe existir en la DB)
    alumno_id = 6
    
    # 3. Create Boleta for Lapso 1 ONLY
    print("--- 📄 Generando Boleta Lapso 1 ---")
    boleta_data = {
        "alumno_id": alumno_id,
        "hasta_lapso": 1,
        "tipo_evaluacion": "Primer Lapso - Parcial",
        "observaciones": "Solo debe verse el lapso 1."
    }
    resp = requests.post(f"{BASE_URL}/boletas/", json=boleta_data, headers=headers)
    if resp.status_code != 201:
        print(f"❌ Error creando boleta L1 ({resp.status_code}): {resp.text}")
        return
    boleta_l1 = resp.json()
    print(f"✅ Boleta L1 Creada: ID {boleta_l1['id']}")
    
    # Download PDF L1
    pdf_resp = requests.get(f"{BASE_URL}/boletas/{boleta_l1['id']}/pdf", headers=headers)
    with open("boleta_lapso_1.pdf", "wb") as f:
        f.write(pdf_resp.content)
    print("💾 boleta_lapso_1.pdf guardado.")
    
    # 4. Create Boleta for Lapso 1 & 2
    print("\n--- 📄 Generando Boleta Lapso 1 y 2 ---")
    boleta_data["hasta_lapso"] = 2
    boleta_data["tipo_evaluacion"] = "Segundo Lapso - Acumulativo"
    boleta_data["observaciones"] = "Deben verse lapsos 1 y 2."
    resp = requests.post(f"{BASE_URL}/boletas/", json=boleta_data, headers=headers)
    boleta_l2 = resp.json()
    print(f"✅ Boleta L2 Creada: ID {boleta_l2['id']}")
    
    # Download PDF L2
    pdf_resp = requests.get(f"{BASE_URL}/boletas/{boleta_l2['id']}/pdf", headers=headers)
    with open("boleta_lapso_2.pdf", "wb") as f:
        f.write(pdf_resp.content)
    print("💾 boleta_lapso_2.pdf guardado.")

    # 5. Create Full Boleta (Default 3)
    print("\n--- 📄 Generando Boleta Año Completo ---")
    boleta_data["hasta_lapso"] = 3
    boleta_data["tipo_evaluacion"] = "Final de Año"
    boleta_data["observaciones"] = "Debe verse todo."
    resp = requests.post(f"{BASE_URL}/boletas/", json=boleta_data, headers=headers)
    boleta_full = resp.json()
    print(f"✅ Boleta Full Creada: ID {boleta_full['id']}")
    
    # Download PDF Full
    pdf_resp = requests.get(f"{BASE_URL}/boletas/{boleta_full['id']}/pdf", headers=headers)
    with open("boleta_final.pdf", "wb") as f:
        f.write(pdf_resp.content)
    print("💾 boleta_final.pdf guardado.")

if __name__ == "__main__":
    if not os.path.exists("outputs"): os.makedirs("outputs")
    os.chdir("outputs")
    test_cumulative_pdf()
