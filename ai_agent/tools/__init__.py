from ai_agent.tools.produccion import tools as produccion_tools
from ai_agent.tools.insumos import tools as insumos_tools
from ai_agent.tools.clima import tools as clima_tools
from ai_agent.tools.sugerencias import tools as sugerencias_tools
from ai_agent.tools.control import tools as control_tools
from ai_agent.tools.enfermedades import tools as enfermedades_tools
from ai_agent.tools.trazabilidad import tools as trazabilidad_tools

tools = (
    produccion_tools +
    insumos_tools +
    clima_tools +
    sugerencias_tools +
    control_tools +
    enfermedades_tools +
    trazabilidad_tools
)
