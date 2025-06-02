import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from fastapi import FastAPI
from ai_agent.core_agent import run_agent
from pydantic import BaseModel
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Crear instancia de FastAPI
app = FastAPI(title="Agente FRESCALES")

# Routers importados desde la estructura modular
from routers.produccion import endpoints as produccion
from routers.insumos import router as insumos_router
from routers.enfermedades import router as enfermedades_router
from routers.sensores.endpoints import router as sensores_router
from routers.precios import router as precios_router
from routers.homeassistant import endpoints as ha_router

# Incluir routers
app.include_router(insumos_router, prefix="/insumos", tags=["Insumos"])
app.include_router(produccion.router, prefix="/produccion", tags=["Producción"])
app.include_router(enfermedades_router, prefix="/enfermedades", tags=["Enfermedades"])
app.include_router(precios_router, prefix="/precios", tags=["Precios"])
app.include_router(ha_router.router)
app.include_router(sensores_router)

# Ruta raíz
@app.get("/")
def root():
    return {"message": "Agente FRESCALES activo 🧠🍓"}

# Entrada de preguntas para el agente
class PreguntaInput(BaseModel):
    pregunta: str

@app.post("/preguntar")
async def preguntar(input: PreguntaInput):
    return {"respuesta": run_agent(input.pregunta)}
