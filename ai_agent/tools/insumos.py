from ai_agent.utils.function_definition import FunctionDefinition  # CORREGIDO
from services.supabase_connector import supabase
from datetime import datetime
from typing import List

def getInsumosAplicados(fecha_inicio: str, fecha_fin: str, invernadero: str) -> List[dict]:
    """Lista de insumos usados en un rango de fechas para un invernadero específico."""
    respuesta = supabase.table("insumos_aplicados") \
        .select("*") \
        .gte("fecha", fecha_inicio) \
        .lte("fecha", fecha_fin) \
        .eq("invernadero", invernadero) \
        .execute()
    return respuesta.data

def getCostoProduccion(invernadero: str, desde: str, hasta: str) -> dict:
    """Calcula el costo total de insumos por kilogramo de fresa producido en un rango."""
    insumos = supabase.table("insumos_aplicados") \
        .select("costo_total") \
        .gte("fecha", desde) \
        .lte("fecha", hasta) \
        .eq("invernadero", invernadero) \
        .execute().data

    produccion = supabase.table("produccion") \
        .select("kilos") \
        .gte("fecha", desde) \
        .lte("fecha", hasta) \
        .eq("invernadero", invernadero) \
        .execute().data

    total_costo = sum(item["costo_total"] for item in insumos if item["costo_total"] is not None)
    total_kilos = sum(item["kilos"] for item in produccion if item["kilos"] is not None)

    costo_kg = round(total_costo / total_kilos, 2) if total_kilos > 0 else 0
    return {
        "invernadero": invernadero,
        "desde": desde,
        "hasta": hasta,
        "total_kilos": total_kilos,
        "total_costo": total_costo,
        "costo_por_kg": costo_kg
    }

def getReposicionesNutrientes(fecha_inicio: str, fecha_fin: str) -> List[dict]:
    """Historial de reposiciones de nutrientes entre dos fechas."""
    respuesta = supabase.table("reposiciones") \
        .select("*") \
        .gte("fecha", fecha_inicio) \
        .lte("fecha", fecha_fin) \
        .execute()
    return respuesta.data

tools = [
    FunctionDefinition(
        name="getInsumosAplicados",
        description="Lista los insumos aplicados entre dos fechas para un invernadero",
        parameters={
            "type": "object",
            "properties": {
                "fecha_inicio": {"type": "string", "format": "date", "description": "Fecha inicial en formato YYYY-MM-DD"},
                "fecha_fin": {"type": "string", "format": "date", "description": "Fecha final en formato YYYY-MM-DD"},
                "invernadero": {"type": "string", "description": "Nombre o ID del invernadero"}
            },
            "required": ["fecha_inicio", "fecha_fin", "invernadero"]
        },
        code=getInsumosAplicados
    ),
    FunctionDefinition(
        name="getCostoProduccion",
        description="Calcula el costo total de insumos por kg producido",
        parameters={
            "type": "object",
            "properties": {
                "invernadero": {"type": "string", "description": "Nombre o ID del invernadero"},
                "desde": {"type": "string", "format": "date", "description": "Fecha inicial"},
                "hasta": {"type": "string", "format": "date", "description": "Fecha final"}
            },
            "required": ["invernadero", "desde", "hasta"]
        },
        code=getCostoProduccion
    ),
    FunctionDefinition(
        name="getReposicionesNutrientes",
        description="Devuelve el historial de reposiciones entre dos fechas",
        parameters={
            "type": "object",
            "properties": {
                "fecha_inicio": {"type": "string", "format": "date"},
                "fecha_fin": {"type": "string", "format": "date"}
            },
            "required": ["fecha_inicio", "fecha_fin"]
        },
        code=getReposicionesNutrientes
    )
]
