@echo off
echo === Web Service de Validacion de Credito ===
echo.

if not exist .env (
    echo Error: Archivo .env no encontrado
    echo Por favor copia .env.example a .env y configura tus credenciales
    pause
    exit /b 1
)

if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando el servicio...
echo El servicio estara disponible en http://localhost:8000
echo.

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

pause
