from ai_agent.utils.function_definition import FunctionDefinition
from services.supabase_connector import supabase
from datetime import datetime, timedelta
import calendar

# Obtener el ID del producto "Fresa" y su unidad
def obtener_producto_fresa():
    productos = supabase.table("productos").select("id, unidad_id").eq("nombre", "Fresa").execute().data
    if not productos:
        raise ValueError("Producto 'Fresa' no encontrado.")
    return productos[0]["id"], productos[0]["unidad_id"]

def obtener_nombre_unidad(unidad_id):
    unidad = supabase.table("unidades").select("nombre").eq("id", unidad_id).execute().data
    return unidad[0]["nombre"] if unidad else "unidad desconocida"

def getProduccionSemana(invernadero: str):
    producto_id, unidad_id = obtener_producto_fresa()
    unidad = obtener_nombre_unidad(unidad_id)

    hoy = datetime.utcnow()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio = inicio_semana.strftime("%Y-%m-%d")
    fin = hoy.strftime("%Y-%m-%d")

    data = supabase.table("produccion") \
        .select("fecha,cantidad") \
        .gte("fecha", inicio) \
        .lte("fecha", fin) \
        .eq("ubicacion_id", invernadero) \
        .eq("producto_id", producto_id) \
        .execute().data

    total = sum(item["cantidad"] for item in data)
    return f"La producción de esta semana en {invernadero} fue de {total} {unidad.lower()}s."

def getProduccionMes(invernadero: str, mes: str = None, año: int = None):
    producto_id, unidad_id = obtener_producto_fresa()
    unidad = obtener_nombre_unidad(unidad_id)

    hoy = datetime.utcnow()
    año = año or hoy.year
    mes = int(mes) if mes else hoy.month

    inicio = datetime(año, mes, 1)
    _, last_day = calendar.monthrange(año, mes)
    fin = datetime(año, mes, last_day)

    data = supabase.table("produccion") \
        .select("fecha,cantidad") \
        .gte("fecha", inicio.strftime("%Y-%m-%d")) \
        .lte("fecha", fin.strftime("%Y-%m-%d")) \
        .eq("ubicacion_id", invernadero) \
        .eq("producto_id", producto_id) \
        .execute().data

    total = sum(item["cantidad"] for item in data)
    return f"Se produjeron {total} {unidad.lower()}s en el mes {mes} de {año} en {invernadero}."

def getProduccionHistorica(invernadero: str, desde: str, hasta: str):
    producto_id, unidad_id = obtener_producto_fresa()
    unidad = obtener_nombre_unidad(unidad_id)

    data = supabase.table("produccion") \
        .select("fecha,cantidad") \
        .gte("fecha", desde) \
        .lte("fecha", hasta) \
        .eq("ubicacion_id", invernadero) \
        .eq("producto_id", producto_id) \
        .order("fecha") \
        .execute().data

    total = sum(item["cantidad"] for item in data)
    return {
        "resumen": f"Entre {desde} y {hasta}, se produjeron {total} {unidad.lower()}s en {invernadero}.",
        "datos": data
    }

def getComparativaProduccionMensual(invernadero: str, mes1: str, mes2: str):
    producto_id, unidad_id = obtener_producto_fresa()
    unidad = obtener_nombre_unidad(unidad_id)

    hoy = datetime.utcnow()
    año = hoy.year

    def calcular(mes):
        inicio = datetime(año, int(mes), 1)
        _, last_day = calendar.monthrange(año, int(mes))
        fin = datetime(año, int(mes), last_day)
        data = supabase.table("produccion") \
            .select("fecha,cantidad") \
            .gte("fecha", inicio.strftime("%Y-%m-%d")) \
            .lte("fecha", fin.strftime("%Y-%m-%d")) \
            .eq("ubicacion_id", invernadero) \
            .eq("producto_id", producto_id) \
            .execute().data
        return sum(item["cantidad"] for item in data)

    total1 = calcular(mes1)
    total2 = calcular(mes2)

    return {
        "resumen": f"Comparativa en {invernadero}: Mes {mes1} = {total1} {unidad.lower()}s, Mes {mes2} = {total2} {unidad.lower()}s.",
        "detalles": {
            f"mes_{mes1}": total1,
            f"mes_{mes2}": total2
        }
    }

tools = [
    FunctionDefinition(
        name="getProduccionSemana",
        description="Producción semanal actual en un invernadero",
        parameters={
            "type": "object",
            "properties": {
                "invernadero": {"type": "string", "description": "ID del invernadero"}
            },
            "required": ["invernadero"]
        },
        code=getProduccionSemana
    ),
    FunctionDefinition(
        name="getProduccionMes",
        description="Producción mensual en un invernadero",
        parameters={
            "type": "object",
            "properties": {
                "invernadero": {"type": "string"},
                "mes": {"type": "string"},
                "año": {"type": "integer"}
            },
            "required": ["invernadero"]
        },
        code=getProduccionMes
    ),
    FunctionDefinition(
        name="getProduccionHistorica",
        description="Producción entre dos fechas",
        parameters={
            "type": "object",
            "properties": {
                "invernadero": {"type": "string"},
                "desde": {"type": "string", "format": "date"},
                "hasta": {"type": "string", "format": "date"}
            },
            "required": ["invernadero", "desde", "hasta"]
        },
        code=getProduccionHistorica
    ),
    FunctionDefinition(
        name="getComparativaProduccionMensual",
        description="Compara producción entre dos meses",
        parameters={
            "type": "object",
            "properties": {
                "invernadero": {"type": "string"},
                "mes1": {"type": "string"},
                "mes2": {"type": "string"}
            },
            "required": ["invernadero", "mes1", "mes2"]
        },
        code=getComparativaProduccionMensual
    )
]
