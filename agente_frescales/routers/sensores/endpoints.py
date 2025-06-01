from fastapi import APIRouter, Query
from datetime import date
from services.influx_connector import (
    consultar_promedio_diario,
    consultar_valor_diario,
    analizar_clima_vs_produccion,
    exportar_entidades_csv,
    client
)
from routers.sensores.schema import PromedioSensorResponse
from constants.humedad_sustrato import SENSORES_HUMEDAD_SUSTRATO

router = APIRouter(
    prefix="/sensor",
    tags=["Sensores"]
)

@router.get("/ph/hoy", response_model=PromedioSensorResponse)
def obtener_ph_hoy():
    return consultar_promedio_diario(sensor_id="fresas_ph", field="value")

@router.get("/ce/hoy", response_model=PromedioSensorResponse)
def obtener_ce_hoy():
    return consultar_promedio_diario(sensor_id="fresas_electrical_conductivity", field="value")

@router.get("/luminosidad/historico")
def luminosidad_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="luminosidad_inv1",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="lx"
    )

@router.get("/entidades/exportar")
def exportar_entidades():
    return exportar_entidades_csv()

@router.get("/ce/historico")
def ce_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="fresas_electrical_conductivity",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="state"
    )

@router.get("/humedad_ambiente/historico")
def humedad_ambiente_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="ambiente_humedad_ambiente",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="%"
    )

@router.get("/temperatura/historico")
def temperatura_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="ambiente_temperatura_ambiente",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="°C"
    )

@router.get("/presion/historico")
def presion_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="ambiente_presi_n_atmosf_rica",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="hPa"
    )

@router.get("/humedad_sustrato/historico")
def humedad_sustrato_historico(
    inv: int = Query(...),
    zona: int = Query(...),
    fecha_inicio: date = Query(...),
    fecha_fin: date = Query(...)
):
    sensor = SENSORES_HUMEDAD_SUSTRATO[f"inv{inv}"][f"zona{zona}"]
    entity_id = sensor["entity_id"]
    measurement = sensor["measurement"]

    return consultar_valor_diario(
        sensor_id=entity_id,
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement=measurement
    )

@router.get("/ph/historico")
def ph_historico(fecha_inicio: date = Query(...), fecha_fin: date = Query(...)):
    return consultar_valor_diario(
        sensor_id="fresas_ph",
        field="value",
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        measurement="state"
    )

# ✅ NUEVO ENDPOINT DEBUG
@router.get("/debug/sensores")
def listar_sensores_y_mediciones():
    try:
        result = client.query("SHOW MEASUREMENTS")
        measurements = [m['name'] for m in result.get_points()]

        sensores = {}
        for m in measurements:
            try:
                tags = client.query(f'SHOW TAG VALUES FROM \"{m}\" WITH KEY = \"entity_id\"')
                sensores[m] = [t['value'] for t in tags.get_points()]
            except:
                sensores[m] = []

        return sensores
    except Exception as e:
        return {"error": str(e)}
