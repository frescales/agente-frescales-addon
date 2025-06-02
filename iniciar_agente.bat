@echo off
REM Activar entorno virtual y lanzar el servidor FastAPI

cd /d %~dp0
call venv\Scripts\activate
uvicorn main:app --reload
pause
