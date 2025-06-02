from ai_agent.utils.function_definition import FunctionDefinition  # CORREGIDO
from services.influx_connector import query_influx
from services.supabase_connector import supabase
from datetime import datetime
from typing import Dict

def sugerirRiego(zona: str) -> dict:
    """Sugiere si debe regarse la zona en base a humedad promedio actual."""
    query = f'''
    from(bucket: "frescales")
      |> range(start: -1h)
      |> filter(fn: (r) => r["_measurement"] == "humedad_sustrato" and r["zona"] == "{zona}")
      |> mean()
    '''
    humedad = query_influx(query)
    if humedad is None:
        return {"zona": zona, "mensaje": "No se encontraron datos recientes de humedad."}

    if humedad < 60:
        return {"zona": zona, "humedad_actual": humedad, "sugerencia": "💧 Activar riego ahora."}
    elif humedad > 80:
        return {"zona": zona, "humedad_actual": humedad, "sugerencia": "🛑 No regar, humedad excesiva."}
    else:
        return {"zona": zona, "humedad_actual": humedad, "sugerencia": "✅ Humedad adecuada, no regar por ahora."}

def sugerirPlanNutricion(fecha: str) -> dict:
    """Sugiere plan nutricional en base a CE y pH del día."""
    fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
    start = fecha_dt.strftime("%Y-%m-%dT00:00:00Z")
    end = fecha_dt.strftime("%Y-%m-%dT23:59:59Z")

    query_ce = f'''
    from(bucket: "frescales")
      |> range(start: {start}, stop: {end})
      |> filter(fn: (r) => r["_measurement"] == "ce")
      |> mean()
    '''
    query_ph = f'''
    from(bucket: "frescales")
      |> range(start: {start}, stop: {end})
      |> filter(fn: (r) => r["_measurement"] == "ph")
      |> mean()
    '''
    ce = query_influx(query_ce)
    ph = query_influx(query_ph)

    sugerencias = []
    if ce is not None and ce < 1.6:
        sugerencias.append("💡 Aumentar concentración de nutrientes.")
    elif ce is not None and ce > 2.2:
        sugerencias.append("💡 Diluir solución o revisar acumulación de sales.")

    if ph is not None and ph < 5.5:
        sugerencias.append("⚠️ Subir el pH (muy ácido).")
    elif ph is not None and ph > 6.5:
        sugerencias.append("⚠️ Bajar el pH (muy alcalino).")

    return {
        "fecha": fecha,
        "ce_promedio": ce,
        "ph_promedio": ph,
        "sugerencias": sugerencias or ["✅ Parámetros dentro de rango recomendado."]
    }

def sugerirPlanFitosanitario(fecha: str) -> dict:
    """Sugiere acciones fitosanitarias basado en enfermedades y clima."""
    enfermedades = supabase.table("enfermedades_detectadas").select("*").eq("fecha", fecha).execute().data
    lluvia = query_influx(f'''
    from(bucket: "frescales")
      |> range(start: {fecha}T00:00:00Z, stop: {fecha}T23:59:59Z)
      |> filter(fn: (r) => r["_measurement"] == "lluvia")
      |> mean()
    ''')

    sugerencias = []

    if enfermedades:
        for e in enfermedades:
            if "antracnosis" in e["nombre"].lower():
                sugerencias.append("🔴 Aplicar fungicida específico para antracnosis.")
            elif "botrytis" in e["nombre"].lower():
                sugerencias.append("🟠 Revisar ventilación y aplicar tratamiento preventivo.")

    if lluvia is not None and lluvia > 5:
        sugerencias.append("💦 Revisar exceso de humedad. Posible riesgo de hongos.")

    return {
        "fecha": fecha,
        "lluvia_promedio": lluvia,
        "enfermedades_detectadas": [e["nombre"] for e in enfermedades] if enfermedades else [],
        "sugerencias": sugerencias or ["✅ No se detectan alertas fitosanitarias para esta fecha."]
    }

tools = [
    FunctionDefinition(
        name="sugerirRiego",
        description="Sugiere si debe regarse la zona en base a la humedad del sustrato",
        parameters={
            "type": "object",
            "properties": {
                "zona": {"type": "string", "description": "Nombre de la zona (ej. zona_1)"}
            },
            "required": ["zona"]
        },
        code=sugerirRiego
    ),
    FunctionDefinition(
        name="sugerirPlanNutricion",
        description="Sugiere un plan de nutrición en base al pH y CE promedio del día",
        parameters={
            "type": "object",
            "properties": {
                "fecha": {"type": "string", "format": "date"}
            },
            "required": ["fecha"]
        },
        code=sugerirPlanNutricion
    ),
    FunctionDefinition(
        name="sugerirPlanFitosanitario",
        description="Sugiere acciones fitosanitarias basadas en enfermedades detectadas y clima",
        parameters={
            "type": "object",
            "properties": {
                "fecha": {"type": "string", "format": "date"}
            },
            "required": ["fecha"]
        },
        code=sugerirPlanFitosanitario
    )
]
