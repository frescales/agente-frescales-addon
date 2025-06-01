#!/bin/bash

cd /app
echo "🚀 Iniciando Agente FRESCALES..."
uvicorn main:app --host 0.0.0.0 --port 8000
