import os
import requests

HA_BASE_URL = os.getenv("HA_BASE_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json",
}

def listar_entidades():
    url = f"{HA_BASE_URL}/api/states"
    response = requests.get(url, headers=HEADERS)
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "message": response.text}

def estado_entidad(entity_id: str):
    url = f"{HA_BASE_URL}/api/states/{entity_id}"
    response = requests.get(url, headers=HEADERS)
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "message": response.text}

def activar_switch(entity_id: str):
    url = f"{HA_BASE_URL}/api/services/switch/turn_on"
    data = {"entity_id": entity_id}
    response = requests.post(url, headers=HEADERS, json=data)
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "message": response.text}

def desactivar_switch(entity_id: str):
    url = f"{HA_BASE_URL}/api/services/switch/turn_off"
    data = {"entity_id": entity_id}
    response = requests.post(url, headers=HEADERS, json=data)
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "message": response.text}

def llamar_servicio(domain: str, service: str, data: dict = {}):
    url = f"{HA_BASE_URL}/api/services/{domain}/{service}"
    response = requests.post(url, headers=HEADERS, json=data)
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "message": response.text}

def obtener_estado(entidad_id: str):
    url = f"{HA_BASE_URL}/api/states/{entidad_id}"
    response = requests.get(url, headers=HEADERS)
    try:
        return response.json()
    except Exception:
        return {"status": response.status_code, "message": response.text}

    response = requests.post(url, headers=HEADERS, json=data)
    return response.json()
