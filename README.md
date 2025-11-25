# CyberSentinel API

API REST para predicción de amenazas cibernéticas usando un modelo LightGBM.

## 📋 Descripción

Esta API permite realizar predicciones usando un modelo de machine learning entrenado (LGBMClassifier) que requiere 38 características de entrada para clasificar amenazas.

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Verificar que el modelo esté presente

Asegúrate de que el archivo `mejor_modelo.pkl` esté en el directorio raíz del proyecto.

## ▶️ Ejecutar la API

```bash
python app.py
```

O usando uvicorn directamente:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

La API estará disponible en: `http://localhost:8000`

## 📚 Documentación

Una vez que la API esté corriendo, puedes acceder a:

- **Documentación interactiva (Swagger UI)**: http://localhost:8000/docs
- **Documentación alternativa (ReDoc)**: http://localhost:8000/redoc

## 🔌 Endpoints

### 1. GET `/`
Información general de la API

**Respuesta:**
```json
{
  "message": "CyberSentinel API",
  "version": "1.0.0",
  "status": "running",
  "model_loaded": true,
  "endpoints": {
    "predict": "/predict (POST)",
    "health": "/health (GET)",
    "docs": "/docs (GET)"
  }
}
```

### 2. GET `/health`
Verificar el estado de la API

**Respuesta:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "LGBMClassifier",
  "n_features": 38
}
```

### 3. POST `/predict`
Realizar predicción con el modelo

**Request Body (JSON):**
```json
{
  "url_length": 50.0,
  "domain_length": 15.0,
  "num_subdomains": 2.0,
  "has_at_symbol": 0.0,
  "num_hyphens": 1.0,
  "num_underscores": 0.0,
  "num_slashes": 3.0,
  "num_dots": 2.0,
  "is_https": 1.0,
  "num_digits": 5.0,
  "num_parameters": 1.0,
  "path_length": 20.0,
  "has_ip": 0.0,
  "suspicious_keywords": 0.0,
  "entropy": 3.5,
  "num_special_chars": 5.0,
  "digit_ratio": 0.1,
  "tld_length": 3.0,
  "risk_score": 0.2,
  "feature_0": 0.0,
  "feature_1": 0.0,
  "feature_2": 0.0,
  "feature_3": 0.0,
  "feature_4": 0.0,
  "feature_5": 0.0,
  "feature_6": 0.0,
  "feature_7": 0.0,
  "feature_8": 0.0,
  "feature_9": 0.0,
  "feature_10": 0.0,
  "feature_11": 0.0,
  "feature_12": 0.0,
  "feature_13": 0.0,
  "feature_14": 0.0,
  "feature_15": 0.0,
  "feature_16": 0.0,
  "feature_17": 0.0,
  "feature_18": 0.0
}
```

**Respuesta:**
```json
{
  "prediction": 0,
  "probability": 0.95,
  "probabilities": [0.95, 0.05],
  "risk_level": "bajo"
}
```

**Campos de respuesta:**
- `prediction`: Clase predicha (0 o 1)
- `probability`: Probabilidad de la clase predicha
- `probabilities`: Array con probabilidades de ambas clases [clase_0, clase_1]
- `risk_level`: Nivel de riesgo calculado ("bajo", "medio", "alto")

## 🧪 Probar la API

### Usando curl:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "url_length": 50.0,
    "domain_length": 15.0,
    "num_subdomains": 2.0,
    "has_at_symbol": 0.0,
    "num_hyphens": 1.0,
    "num_underscores": 0.0,
    "num_slashes": 3.0,
    "num_dots": 2.0,
    "is_https": 1.0,
    "num_digits": 5.0,
    "num_parameters": 1.0,
    "path_length": 20.0,
    "has_ip": 0.0,
    "suspicious_keywords": 0.0,
    "entropy": 3.5,
    "num_special_chars": 5.0,
    "digit_ratio": 0.1,
    "tld_length": 3.0,
    "risk_score": 0.2,
    "feature_0": 0.0,
    "feature_1": 0.0,
    "feature_2": 0.0,
    "feature_3": 0.0,
    "feature_4": 0.0,
    "feature_5": 0.0,
    "feature_6": 0.0,
    "feature_7": 0.0,
    "feature_8": 0.0,
    "feature_9": 0.0,
    "feature_10": 0.0,
    "feature_11": 0.0,
    "feature_12": 0.0,
    "feature_13": 0.0,
    "feature_14": 0.0,
    "feature_15": 0.0,
    "feature_16": 0.0,
    "feature_17": 0.0,
    "feature_18": 0.0
  }'
```

### Usando el script de prueba:

```bash
# Instalar requests si no está instalado
pip install requests

# Ejecutar el script de prueba
python test_api.py
```

## 📦 Características del Modelo

El modelo requiere 38 características de entrada:

1. **Características de URL:**
   - url_length, domain_length, path_length, tld_length
   - num_subdomains, num_slashes, num_dots, num_hyphens, num_underscores
   - num_parameters, num_digits, num_special_chars

2. **Indicadores binarios:**
   - has_at_symbol, has_ip, is_https

3. **Métricas calculadas:**
   - entropy, digit_ratio, suspicious_keywords, risk_score

4. **Características adicionales:**
   - feature_0 a feature_18 (19 características adicionales)

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **LightGBM**: Modelo de gradient boosting
- **Uvicorn**: Servidor ASGI de alto rendimiento
- **Pydantic**: Validación de datos
- **scikit-learn**: Herramientas de ML
- **NumPy**: Computación numérica

## 📝 Notas

- El modelo debe cargarse con `joblib.load()` en lugar de `pickle.load()`
- Todas las características deben ser de tipo `float`
- Las 38 características son obligatorias para hacer predicciones