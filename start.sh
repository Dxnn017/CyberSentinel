#!/bin/bash

echo "🚀 Iniciando CyberSentinel API..."
echo ""

# Verificar que el modelo existe
if [ ! -f "mejor_modelo.pkl" ]; then
    echo "❌ Error: No se encontró el archivo mejor_modelo.pkl"
    exit 1
fi

# Verificar que las dependencias están instaladas
echo "📦 Verificando dependencias..."
pip install -q -r requirements.txt

echo ""
echo "✅ Dependencias instaladas"
echo ""
echo "🌐 Iniciando servidor en http://localhost:8000"
echo "📚 Documentación disponible en http://localhost:8000/docs"
echo ""
echo "Presiona CTRL+C para detener el servidor"
echo ""

# Iniciar el servidor
python app.py
