from ai_agent.utils.function_definition import FunctionDefinition  # CAMBIO AQUÍ
from services.influx_connector import query_influx
from typing import List, Dict

def getPromedioLuminosidad(mes: str, invernadero: str) -> dict:
    query = f'''
    from(bucket: "frescales")
      |> range(start: {mes}-01T00:00:00Z, stop: {mes}-31T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "luminosidad" and r["invernadero"] == "{invernadero}")
      |> mean()
    '''
    result = query_influx(query)
    return {"mes": mes, "invernadero": invernadero, "luminosidad_promedio": result}

def getPromedioHumedadSustrato(zona: str, desde: str, hasta: str) -> dict:
    query = f'''
    from(bucket: "frescales")
      |> range(start: {desde}T00:00:00Z, stop: {hasta}T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "humedad_sustrato" and r["zona"] == "{zona}")
      |> mean()
    '''
    result = query_influx(query)
    return {"zona": zona, "desde": desde, "hasta": hasta, "humedad_promedio": result}

def getPromedioPH_CE(mes: str) -> dict:
    query_ph = f'''
    from(bucket: "frescales")
      |> range(start: {mes}-01T00:00:00Z, stop: {mes}-31T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "ph")
      |> mean()
    '''
    query_ce = f'''
    from(bucket: "frescales")
      |> range(start: {mes}-01T00:00:00Z, stop: {mes}-31T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "ce")
      |> mean()
    '''
    ph_result = query_influx(query_ph)
    ce_result = query_influx(query_ce)
    return {"mes": mes, "ph_promedio": ph_result, "ce_promedio": ce_result}

def getHistoricoSensor(sensor: str, desde: str, hasta: str) -> List[dict]:
    query = f'''
    from(bucket: "frescales")
      |> range(start: {desde}T00:00:00Z, stop: {hasta}T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "{sensor}")
    '''
    result = query_influx(query)
    return result

tools = [
    FunctionDefinition(
        name="getPromedioLuminosidad",
        description="Devuelve la luminosidad media mensual para un invernadero",
        parameters={
            "type": "object",
            "properties": {
                "mes": {"type": "string", "description": "Mes en formato YYYY-MM"},
                "invernadero": {"type": "string", "description": "Nombre o ID del invernadero"}
            },
            "required": ["mes", "invernadero"]
        },
        code=getPromedioLuminosidad
    ),
    FunctionDefinition(
        name="getPromedioHumedadSustrato",
        description="Devuelve la humedad promedio de sustrato en una zona entre dos fechas",
        parameters={
            "type": "object",
            "properties": {
                "zona": {"type": "string"},
                "desde": {"type": "string", "format": "date"},
                "hasta": {"type": "string", "format": "date"}
            },
            "required": ["zona", "desde", "hasta"]
        },
        code=getPromedioHumedadSustrato
    ),
    FunctionDefinition(
        name="getPromedioPH_CE",
        description="Devuelve el pH y CE promedio de un mes",
        parameters={
            "type": "object",
            "properties": {
                "mes": {"type": "string", "description": "Mes en formato YYYY-MM"}
            },
            "required": ["mes"]
        },
        code=getPromedioPH_CE
    ),
    FunctionDefinition(
        name="getHistoricoSensor",
        description="Devuelve el historial de un sensor entre dos fechas",
        parameters={
            "type": "object",
            "properties": {
                "sensor": {"type": "string"},
                "desde": {"type": "string", "format": "date"},
                "hasta": {"type": "string", "format": "date"}
            },
            "required": ["sensor", "desde", "hasta"]
        },
        code=getHistoricoSensor
    )
]
