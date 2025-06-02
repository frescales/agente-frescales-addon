from ai_agent.utils.function_definition import FunctionDefinition  # CORREGIDO
from services.supabase_connector import supabase
from typing import List

def getIncidenciasEnfermedades(desde: str, hasta: str) -> List[dict]:
    """Devuelve la lista de enfermedades detectadas entre dos fechas."""
    respuesta = supabase.table("incidencias_enfermedades").select("*").gte("fecha", desde).lte("fecha", hasta).execute()
    return respuesta.data

def getTratamientosAplicados(desde: str, hasta: str) -> List[dict]:
    """Devuelve los tratamientos aplicados contra enfermedades en un rango de fechas."""
    tratamientos = supabase.table("tratamientos_enfermedades") \
        .select("*") \
        .gte("fecha", desde) \
        .lte("fecha", hasta) \
        .execute().data

    detalles = supabase.table("detalle_tratamientos_enfermedades") \
        .select("*, productos(nombre), unidades(nombre)") \
        .execute().data

    respuesta = []
    for t in tratamientos:
        productos_usados = [
            {
                "producto_id": d["producto_id"],
                "nombre": d["productos"]["nombre"],
                "cantidad": d["cantidad"],
                "unidad": d["unidades"]["nombre"]
            }
            for d in detalles if d["tratamiento_id"] == t["id"]
        ]
        respuesta.append({
            "id": t["id"],
            "fecha": t["fecha"],
            "enfermedad": t["enfermedad"],
            "zona": t["zona"],
            "productos": productos_usados
        })

    return respuesta

tools = [
    FunctionDefinition(
        name="getIncidenciasEnfermedades",
        description="Lista las enfermedades detectadas en un rango de fechas",
        parameters={
            "type": "object",
            "properties": {
                "desde": {"type": "string", "format": "date", "description": "Fecha inicial (YYYY-MM-DD)"},
                "hasta": {"type": "string", "format": "date", "description": "Fecha final (YYYY-MM-DD)"}
            },
            "required": ["desde", "hasta"]
        },
        code=getIncidenciasEnfermedades
    ),
    FunctionDefinition(
        name="getTratamientosAplicados",
        description="Devuelve los tratamientos fitosanitarios aplicados en un rango de fechas",
        parameters={
            "type": "object",
            "properties": {
                "desde": {"type": "string", "format": "date"},
                "hasta": {"type": "string", "format": "date"}
            },
            "required": ["desde", "hasta"]
        },
        code=getTratamientosAplicados
    )
]
