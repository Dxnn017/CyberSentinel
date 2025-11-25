# 🛡️ CyberSentinel

Sistema de Detección de Phishing basado en Inteligencia Artificial desarrollado en la Universidad Privada Antenor Orrego.

API REST que analiza URLs para detectar sitios web de phishing usando un modelo LightGBM entrenado con 450,000+ URLs.

## 📋 Descripción

Sistema automatizado de detección de phishing que analiza características de URLs y el contenido de páginas web para clasificarlas como **legítimas** o **fraudulentas**. 

El sistema:
- ✅ Extrae automáticamente 19 características de las URLs
- ✅ Usa un modelo LightGBM entrenado (99.47% accuracy)
- ✅ Proporciona predicciones en tiempo real
- ✅ Incluye análisis heurístico de riesgo
- ✅ API REST lista para producción

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Dxnn017/CyberSentinel.git
cd CyberSentinel
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Verificar archivos del modelo

Asegúrate de tener estos archivos en el directorio raíz:
- `mejor_modelo.pkl` - Modelo LightGBM entrenado
- `scaler.pkl` - Normalizador MinMaxScaler

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

### 3. POST `/analyze`
**Analiza una URL y devuelve predicción completa**

**Request Body (JSON):**
```json
{
  "url": "https://www.example.com"
}
```

**Respuesta:**
```json
{
  "url": "https://www.example.com",
  "is_phishing": false,
  "confidence": 0.9967,
  "risk_level": "seguro",
  "prediction": 1,
  "probabilities": {
    "phishing": 0.0032,
    "legitimate": 0.9967
  },
  "features": {
    "url_length": 22.0,
    "domain_length": 14.0,
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

### Ejemplo 1: URL Legítima

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.google.com"}'
```

### Ejemplo 2: URL Sospechosa

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "http://secure-login-verify.suspicious-site.com/update.php?id=123"}'
```

### Ejemplo 3: Usando Python

```python
import requests

response = requests.post(
    "http://localhost:8000/analyze",
    json={"url": "https://www.example.com"}
)

result = response.json()
print(f"Is Phishing: {result['is_phishing']}")
print(f"Confidence: {result['confidence']:.2%}")
print(f"Risk Level: {result['risk_level']}")
```

### Ejemplo antiguo con características manuales:

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

## 🔍 Características Extraídas Automáticamente

El sistema analiza **19 características** de cada URL:

### 1. Características Estructurales
- `url_length` - Longitud total de la URL
- `domain_length` - Longitud del dominio
- `path_length` - Longitud del path
- `tld_length` - Longitud del TLD (.com, .net, etc.)
- `num_subdomains` - Cantidad de subdominios
- `num_slashes` - Cantidad de barras (/)
- `num_dots` - Cantidad de puntos
- `num_hyphens` - Cantidad de guiones (-)
- `num_underscores` - Cantidad de guiones bajos (_)
- `num_parameters` - Cantidad de parámetros URL
- `num_digits` - Cantidad de dígitos
- `num_special_chars` - Cantidad de caracteres especiales

### 2. Indicadores de Seguridad
- `is_https` - Usa protocolo HTTPS (1=Sí, 0=No)
- `has_at_symbol` - Contiene símbolo @ (1=Sí, 0=No)
- `has_ip` - Contiene dirección IP (1=Sí, 0=No)

### 3. Análisis Heurístico
- `suspicious_keywords` - Palabras clave sospechosas (login, verify, account, etc.)
- `entropy` - Entropía de la URL (medida de aleatoriedad)
- `digit_ratio` - Ratio de dígitos respecto al total
- `risk_score` - Puntuación heurística de riesgo (0-16)

**Nota:** El modelo usa 38 características internamente (19 originales + 19 normalizadas con MinMaxScaler)

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y de alto rendimiento
- **LightGBM** - Modelo de gradient boosting (99.47% accuracy)
- **scikit-learn** - MinMaxScaler para normalización
- **Uvicorn** - Servidor ASGI
- **Pydantic** - Validación de datos

### Procesamiento
- **tldextract** - Análisis de dominios
- **NumPy** - Computación numérica
- **joblib** - Serialización del modelo

## 📊 Rendimiento del Modelo

- **Accuracy**: 99.47%
- **Precision**: 99.5%
- **Recall**: 99.4%
- **F1-Score**: 99.5%
- **Dataset**: 450,177 URLs
- **Algoritmo**: LightGBM Classifier

## 📁 Estructura del Proyecto

```
CyberSentinel/
├── app.py                    # API FastAPI
├── feature_extractor.py      # Extractor de características
├── mejor_modelo.pkl          # Modelo LightGBM entrenado
├── scaler.pkl               # MinMaxScaler para normalización
├── requirements.txt         # Dependencias Python
├── README.md               # Documentación
├── dataset/
│   └── URL dataset.csv     # Dataset original (450K URLs)
└── project_ia/
    ├── Proyecto_IA.ipynb   # Notebook de entrenamiento
    └── Proyecto de Inteligencia Artificial.pdf
```

## 📝 Notas Técnicas

- El modelo usa **38 características** internamente (19 originales + 19 normalizadas)
- La normalización se hace automáticamente con `scaler.pkl`
- El endpoint `/analyze` solo requiere la URL como entrada
- Las predicciones son en tiempo real (< 100ms)