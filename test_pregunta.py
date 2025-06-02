import sys
import os

# Añadir la raíz del proyecto al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_agent.core_agent import run_agent


from ai_agent.core_agent import run_agent
# Prueba directa con pregunta
pregunta = "¿Cuántos kilogramos se produjeron el mes pasado en el invernadero 1?"
respuesta = run_agent(pregunta)
print("🔍 Pregunta:", pregunta)
print("🧠 Respuesta:", respuesta)
