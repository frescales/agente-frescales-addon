import os
from openai import OpenAI
from dotenv import load_dotenv
from ai_agent.registry import get_tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agent(prompt: str):
    tools = get_tools()

    # Convertimos los objetos FunctionDefinition en el formato requerido por OpenAI
    functions = [{"type": tool.type, "function": tool.function} for tool in tools]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en producción de fresas."},
            {"role": "user", "content": prompt}
        ],
        tools=functions,
        tool_choice="auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        fn_name = msg.tool_calls[0].function.name
        fn_args = eval(msg.tool_calls[0].function.arguments)

        # Aquí buscamos el tool por nombre
        tool = next((t for t in tools if t.function["name"] == fn_name), None)
        if tool:
            return tool.code(**fn_args)

    return msg.content
