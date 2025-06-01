from influxdb import InfluxDBClient
from datetime import datetime, timedelta, date
import pandas as pd
import os 
# Parámetros de conexión local
INFLUX_HOST = os.getenv("INFLUX_HOST", "127.0.0.1")
INFLUX_PORT = int(os.getenv("INFLUX_PORT", 8086))
INFLUX_USER = os.getenv("INFLUX_USER", "agente")
INFLUX_PASSWORD = os.getenv("INFLUX_PASSWORD", "agente123")
INFLUX_DB = os.getenv("INFLUX_DB", "homeassistant")  # Puedes definir INFLUX_DB en el .env

client = InfluxDBClient(
    host=INFLUX_HOST,
    port=INFLUX_PORT,
    username=INFLUX_USER,
    password=INFLUX_PASSWORD,
    database=INFLUX_DB,
)
def query_influx(sensor_id: str, fecha_inicio: str, fecha_fin: str, measurement: str = "state") -> pd.DataFrame:
    filtro_horas = ""
    if sensor_id == "luminosidad_inv1":
        filtro_horas = "AND time >= now() - 12h AND time <= now()"  # solo horas luz

    consulta = f"""
    SELECT mean("value") AS value
    FROM "{measurement}"
    WHERE
        "entity_id" = '{sensor_id}'
        AND time >= '{fecha_inicio}T00:00:00Z'
        AND time <= '{fecha_fin}T23:59:59Z'
        {filtro_horas}
    GROUP BY time(1d) fill(none)
    """

    try:
        result = client.query(consulta)
        points = list(result.get_points())
        return pd.DataFrame(points)
    except Exception as e:
        print(f"❌ Error Influx local: {e}")
        return pd.DataFrame()


def consultar_promedio_diario(sensor_id: str, field: str) -> dict:
    hoy = datetime.utcnow().date()
    df = query_influx(sensor_id, str(hoy), str(hoy))

    print(f"\n🧪 DEBUG [{sensor_id}] → DataFrame:\n", df.head())

    if not df.empty and "value" in df.columns:
        valor = round(df["value"].mean(), 2)
        return {"sensor_id": sensor_id, "fecha": str(hoy), "promedio": valor}

    return {"sensor_id": sensor_id, "fecha": str(hoy), "promedio": None}


def consultar_valor_diario(sensor_id: str, field: str, dias: int = None, fecha_inicio: date = None, fecha_fin: date = None, measurement: str = "state") -> list:
    if dias is not None:
        fecha_fin = datetime.utcnow().date()
        fecha_inicio = fecha_fin - timedelta(days=dias)
    elif not (fecha_inicio and fecha_fin):
        raise ValueError("Debes proporcionar 'dias' o 'fecha_inicio' y 'fecha_fin'")

    df = query_influx(sensor_id, str(fecha_inicio), str(fecha_fin), measurement=measurement)

    if df.empty:
        return []

    df["time"] = pd.to_datetime(df["time"]).dt.date
    diario = df.groupby("time")["value"].mean().round(2)
    return [{"fecha": str(f), "valor": v} for f, v in diario.items()]


def analizar_clima_vs_produccion():
    from constants.clima import SENSORES_CLIMA
    from services.supabase_connector import obtener_total_producido

    hoy = datetime.utcnow().date()
    hace7 = hoy - timedelta(days=7)

    resultados = {}
    for clave, info in SENSORES_CLIMA.items():
        df = query_influx(info["entity_id"], str(hace7), str(hoy))
        if df.empty:
            resultados[clave] = None
        else:
            df["time"] = pd.to_datetime(df["time"]).dt.date
            diario = df.groupby("time")["value"].mean().round(2)
            resultados[clave] = [{"fecha": str(k), "valor": v} for k, v in diario.items()]

    produccion = obtener_total_producido(rango="comparar", fecha_inicio=hace7, fecha_fin=hoy)
    return {"clima": resultados, "produccion": produccion}


def exportar_entidades_csv():
    ini = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%dT00:00:00Z")
    fin = datetime.utcnow().strftime("%Y-%m-%dT23:59:59Z")

    consulta = f"""
    SELECT COUNT("value") AS registros
    FROM "state"
    WHERE time >= '{ini}' AND time <= '{fin}'
    GROUP BY "entity_id"
    """

    try:
        result = client.query(consulta)
        rows = []
        for k, v in result.items():
            entity_id = k[1]['entity_id']
            count = list(v.get_points())[0]["registros"]
            rows.append({"entity_id": entity_id, "registros": count})
        df = pd.DataFrame(rows)
        ruta = os.path.join(os.getcwd(), "entidades_influx.csv")
        df.to_csv(ruta, index=False)
        return {"status": "ok", "total": len(df), "archivo": ruta}
    except Exception as e:
        return {"status": "error", "detalle": str(e)}

