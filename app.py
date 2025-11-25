from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, HttpUrl
import joblib
import numpy as np
from typing import Dict
import uvicorn
from feature_extractor import URLFeatureExtractor

# Cargar el modelo y el scaler al iniciar la aplicación
try:
    model = joblib.load('mejor_modelo.pkl')
    print("✓ Modelo cargado exitosamente")
    print(f"  Tipo: {type(model).__name__}")
    print(f"  Características esperadas: {model.n_features_in_ if hasattr(model, 'n_features_in_') else 'N/A'}")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")
    model = None

try:
    scaler = joblib.load('scaler.pkl')
    print("✓ Scaler cargado exitosamente")
except Exception as e:
    print(f"✗ Error al cargar el scaler: {e}")
    scaler = None

# Inicializar extractor de características
extractor = URLFeatureExtractor()

app = FastAPI(
    title="CyberSentinel API",
    description="Sistema de Detección de Phishing basado en Inteligencia Artificial - Universidad Privada Antenor Orrego",
    version="1.0.0"
)

# Modelo de entrada para análisis de URL
class URLInput(BaseModel):
    url: str = Field(..., description="URL completa a analizar")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.google.com"
            }
        }

# Modelo de respuesta
class AnalysisOutput(BaseModel):
    url: str = Field(..., description="URL analizada")
    is_phishing: bool = Field(..., description="True si es phishing, False si es legítima")
    confidence: float = Field(..., description="Nivel de confianza de la predicción (0-1)")
    risk_level: str = Field(..., description="Nivel de riesgo: seguro, medio, alto")
    prediction: int = Field(..., description="0=Phishing, 1=Legítima")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades por clase")
    features: Dict[str, float] = Field(..., description="Características extraídas de la URL")
    heuristic_score: int = Field(..., description="Puntuación heurística de riesgo (0-16)")

@app.get("/")
def read_root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "CyberSentinel - Sistema de Detección de Phishing",
        "version": "1.0.0",
        "universidad": "Universidad Privada Antenor Orrego",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "analyze": "/analyze (POST) - Analiza una URL para detectar phishing",
            "health": "/health (GET) - Verifica el estado del sistema",
            "docs": "/docs (GET) - Documentación interactiva",
            "redoc": "/redoc (GET) - Documentación alternativa"
        }
    }

@app.get("/health")
def health_check():
    """Verificar el estado de la API y del modelo"""
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    return {
        "status": "healthy",
        "model_loaded": True,
        "model_type": type(model).__name__,
        "n_features": model.n_features_in_ if hasattr(model, 'n_features_in_') else None,
        "feature_extractor": "URLFeatureExtractor v1.0"
    }

@app.post("/analyze", response_model=AnalysisOutput)
def analyze_url(data: URLInput):
    """
    Analiza una URL para detectar si es phishing o legítima.
    
    El sistema extrae automáticamente 19 características de la URL incluyendo:
    - Características estructurales (longitud, subdominios, etc.)
    - Indicadores de seguridad (HTTPS, IP, etc.)
    - Análisis heurístico (palabras sospechosas, entropía, etc.)
    
    Args:
        data: Objeto con la URL a analizar
        
    Returns:
        Análisis completo incluyendo predicción, confianza y características extraídas
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        url = data.url
        
        # Extraer características de la URL
        features_dict = extractor.extract_features(url)
        features_array = extractor.extract_features_array(url, scaler=scaler)
        
        # Realizar predicción
        prediction = int(model.predict(features_array)[0])
        probabilities = model.predict_proba(features_array)[0].tolist()
        
        # prediction: 0=Phishing, 1=Legítima
        is_phishing = (prediction == 0)
        confidence = probabilities[prediction]
        
        # Determinar nivel de riesgo
        if is_phishing:
            if confidence >= 0.9:
                risk_level = "alto"
            elif confidence >= 0.7:
                risk_level = "medio"
            else:
                risk_level = "bajo"
        else:
            risk_level = "seguro"
        
        return AnalysisOutput(
            url=url,
            is_phishing=is_phishing,
            confidence=confidence,
            risk_level=risk_level,
            prediction=prediction,
            probabilities={
                "phishing": probabilities[0],
                "legitimate": probabilities[1]
            },
            features=features_dict,
            heuristic_score=features_dict['risk_score']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🛡️  CYBERSENTINEL - Sistema de Detección de Phishing")
    print("  📚  Universidad Privada Antenor Orrego")
    print("="*70 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
