#!/bin/bash

echo "=== Credit Limit Validation Web Service ==="
echo ""

if [ ! -f ".env" ]; then
    echo "Error: Archivo .env no encontrado"
    echo "Por favor copia .env.example a .env y configura tus credenciales"
    exit 1
fi

echo "Instalando dependencias..."
pip install -r requirements.txt

echo ""
echo "Iniciando el servicio..."
echo "El servicio estara disponible en http://localhost:8000"
echo ""

python app.py
