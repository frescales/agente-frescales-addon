from ai_agent.utils.function_definition import FunctionDefinition  # CORREGIDO
from services.supabase_connector import supabase

def registrarConversacion(usuario: str, pregunta: str, respuesta: str) -> dict:
    """Registra una conversación entre el usuario y el agente para trazabilidad."""
    data = {
        "usuario": usuario,
        "pregunta": pregunta,
        "respuesta": respuesta
    }
    insert = supabase.table("conversaciones_agente").insert(data).execute()
    return {"status": "registrado", "id": insert.data[0]["id"]}

tools = [
    FunctionDefinition(
        name="registrarConversacion",
        description="Registra una conversación con el agente para fines de trazabilidad",
        parameters={
            "type": "object",
            "properties": {
                "usuario": {"type": "string", "description": "Identificador del usuario"},
                "pregunta": {"type": "string", "description": "Pregunta hecha por el usuario"},
                "respuesta": {"type": "string", "description": "Respuesta generada por el agente"}
            },
            "required": ["usuario", "pregunta", "respuesta"]
        },
        code=registrarConversacion
    )
]
