from fastapi import APIRouter
from pydantic import BaseModel
from services.home_assistant_connector import (
    llamar_servicio,
    activar_switch,
    desactivar_switch,
)

router = APIRouter(
    prefix="/homeassistant",
    tags=["Home Assistant"]
)

# ------------------------
# ✅ MODELOS
# ------------------------

class ServicioRequest(BaseModel):
    domain: str
    service: str
    entity_id: str
    data: dict = {}

class EntidadRequest(BaseModel):
    entity_id: str

class LuzRequest(BaseModel):
    entity_id: str
    brightness: int = 255
    color_name: str | None = None


# ------------------------
# ✅ ENDPOINT GENÉRICO
# ------------------------

@router.post("/servicio")
def ejecutar_servicio(req: ServicioRequest):
    payload = {"entity_id": req.entity_id}
    payload.update(req.data)
    return llamar_servicio(req.domain, req.service, payload)


# ------------------------
# ✅ SWITCH
# ------------------------

@router.post("/encender")
def encender_switch(req: EntidadRequest):
    return activar_switch(req.entity_id)

@router.post("/apagar")
def apagar_switch(req: EntidadRequest):
    return desactivar_switch(req.entity_id)


# ------------------------
# ✅ LUCES
# ------------------------

@router.post("/luz/encender")
def encender_luz(req: LuzRequest):
    payload = {
        "entity_id": req.entity_id,
        "brightness": req.brightness
    }
    if req.color_name:
        payload["color_name"] = req.color_name
    return llamar_servicio("light", "turn_on", payload)

@router.post("/luz/apagar")
def apagar_luz(req: EntidadRequest):
    return llamar_servicio("light", "turn_off", {"entity_id": req.entity_id})


# ------------------------
# ✅ SCRIPT
# ------------------------

@router.post("/script/ejecutar")
def ejecutar_script(req: EntidadRequest):
    return llamar_servicio("script", "turn_on", {"entity_id": req.entity_id})


# ------------------------
# ✅ AUTOMATION
# ------------------------

@router.post("/automation/activar")
def activar_automation(req: EntidadRequest):
    return llamar_servicio("automation", "turn_on", {"entity_id": req.entity_id})

@router.post("/automation/desactivar")
def desactivar_automation(req: EntidadRequest):
    return llamar_servicio("automation", "turn_off", {"entity_id": req.entity_id})


# ------------------------
# ✅ SCENE
# ------------------------

@router.post("/scene/activar")
def activar_escena(req: EntidadRequest):
    return llamar_servicio("scene", "turn_on", {"entity_id": req.entity_id})

# ------------------------
# ✅ INPUT_NUMBER
# ------------------------

class InputNumberRequest(BaseModel):
    entity_id: str
    value: float

@router.post("/input_number/set")
def set_input_number(req: InputNumberRequest):
    return llamar_servicio("input_number", "set_value", {
        "entity_id": req.entity_id,
        "value": req.value
    })


# ------------------------
# ✅ INPUT_BOOLEAN
# ------------------------

@router.post("/input_boolean/activar")
def activar_boolean(req: EntidadRequest):
    return llamar_servicio("input_boolean", "turn_on", {"entity_id": req.entity_id})

@router.post("/input_boolean/desactivar")
def desactivar_boolean(req: EntidadRequest):
    return llamar_servicio("input_boolean", "turn_off", {"entity_id": req.entity_id})


# ------------------------
# ✅ INPUT_TEXT
# ------------------------

class InputTextRequest(BaseModel):
    entity_id: str
    value: str

@router.post("/input_text/set")
def set_input_text(req: InputTextRequest):
    return llamar_servicio("input_text", "set_value", {
        "entity_id": req.entity_id,
        "value": req.value
    })

@router.get("/estado")
def obtener_estado_entidad(entity_id: str):
    from services.home_assistant_connector import obtener_estado
    return obtener_estado(entity_id)
