from ai_agent.utils.function_definition import FunctionDefinition
from services.home_assistant_connector import (
    activar_switch,
    desactivar_switch,
    obtener_estado,
)

# Activar riego en una zona durante una duración dada
def activar_riego(zona: str, duracion: int) -> str:
    entity_id = f"switch.riego_zona_{zona.lower()}"
    activar_switch(entity_id)
    return f"Riego activado en la zona {zona} durante {duracion} minutos."

# Encender luces en una zona
def encender_luces(zona: str) -> str:
    entity_id = f"switch.luces_zona_{zona.lower()}"
    activar_switch(entity_id)
    return f"Luces encendidas en la zona {zona}."

# Obtener estado del tanque
def obtener_estado_tanque() -> dict:
    return {
        "nivel": obtener_estado("sensor.nivel_de_agua_del_tanque"),
        "volumen": obtener_estado("sensor.volumen_actual_del_tanque"),
        "porcentaje": obtener_estado("sensor.porcentaje_de_llenado_del_tanque"),
    }

tools = [
    FunctionDefinition(
        name="activar_riego",
        description="Activa el riego en una zona específica durante un tiempo determinado",
        parameters={
            "type": "object",
            "properties": {
                "zona": {"type": "string", "description": "Zona a regar (ej. Zona 1)"},
                "duracion": {"type": "integer", "description": "Duración del riego en minutos"}
            },
            "required": ["zona", "duracion"]
        },
        code=activar_riego
    ),
    FunctionDefinition(
        name="encender_luces",
        description="Enciende las luces de una zona del invernadero",
        parameters={
            "type": "object",
            "properties": {
                "zona": {"type": "string", "description": "Zona a iluminar (ej. Zona 2)"}
            },
            "required": ["zona"]
        },
        code=encender_luces
    ),
    FunctionDefinition(
        name="obtener_estado_tanque",
        description="Obtiene el estado actual del tanque (nivel, volumen y porcentaje de llenado)",
        parameters={"type": "object", "properties": {}, "required": []},
        code=obtener_estado_tanque
    )
]
