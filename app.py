from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from typing import List
import uvicorn

# Cargar el modelo al iniciar la aplicación
try:
    model = joblib.load('mejor_modelo.pkl')
    print("✓ Modelo cargado exitosamente")
except Exception as e:
    print(f"✗ Error al cargar el modelo: {e}")
    model = None

app = FastAPI(
    title="CyberSentinel API",
    description="API para predicción de amenazas usando modelo LightGBM",
    version="1.0.0"
)

# Modelo de datos para la entrada
class PredictionInput(BaseModel):
    """
    Datos de entrada para el modelo de predicción.
    El modelo requiere 38 características.
    """
    url_length: float = Field(..., description="Longitud de la URL")
    domain_length: float = Field(..., description="Longitud del dominio")
    num_subdomains: float = Field(..., description="Número de subdominios")
    has_at_symbol: float = Field(..., description="Tiene símbolo @")
    num_hyphens: float = Field(..., description="Número de guiones")
    num_underscores: float = Field(..., description="Número de guiones bajos")
    num_slashes: float = Field(..., description="Número de barras")
    num_dots: float = Field(..., description="Número de puntos")
    is_https: float = Field(..., description="Es HTTPS")
    num_digits: float = Field(..., description="Número de dígitos")
    num_parameters: float = Field(..., description="Número de parámetros")
    path_length: float = Field(..., description="Longitud del path")
    has_ip: float = Field(..., description="Tiene dirección IP")
    suspicious_keywords: float = Field(..., description="Palabras clave sospechosas")
    entropy: float = Field(..., description="Entropía")
    num_special_chars: float = Field(..., description="Número de caracteres especiales")
    digit_ratio: float = Field(..., description="Ratio de dígitos")
    tld_length: float = Field(..., description="Longitud del TLD")
    risk_score: float = Field(..., description="Puntuación de riesgo")
    feature_0: float = Field(..., description="Característica 0")
    feature_1: float = Field(..., description="Característica 1")
    feature_2: float = Field(..., description="Característica 2")
    feature_3: float = Field(..., description="Característica 3")
    feature_4: float = Field(..., description="Característica 4")
    feature_5: float = Field(..., description="Característica 5")
    feature_6: float = Field(..., description="Característica 6")
    feature_7: float = Field(..., description="Característica 7")
    feature_8: float = Field(..., description="Característica 8")
    feature_9: float = Field(..., description="Característica 9")
    feature_10: float = Field(..., description="Característica 10")
    feature_11: float = Field(..., description="Característica 11")
    feature_12: float = Field(..., description="Característica 12")
    feature_13: float = Field(..., description="Característica 13")
    feature_14: float = Field(..., description="Característica 14")
    feature_15: float = Field(..., description="Característica 15")
    feature_16: float = Field(..., description="Característica 16")
    feature_17: float = Field(..., description="Característica 17")
    feature_18: float = Field(..., description="Característica 18")

    class Config:
        json_schema_extra = {
            "example": {
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
        }

# Modelo de respuesta
class PredictionOutput(BaseModel):
    prediction: int = Field(..., description="Predicción del modelo (0 o 1)")
    probability: float = Field(..., description="Probabilidad de la clase predicha")
    probabilities: List[float] = Field(..., description="Probabilidades de todas las clases [clase_0, clase_1]")
    risk_level: str = Field(..., description="Nivel de riesgo: bajo, medio, alto")

@app.get("/")
def read_root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "CyberSentinel API",
        "version": "1.0.0",
        "status": "running",
        "model_loaded": model is not None,
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
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
        "n_features": len(model.feature_names_in_) if hasattr(model, 'feature_names_in_') else None
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    """
    Realizar predicción con el modelo.
    
    Args:
        data: Objeto con las 38 características requeridas por el modelo
        
    Returns:
        Predicción, probabilidad y nivel de riesgo
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Convertir los datos de entrada a un array numpy en el orden correcto
        features = np.array([[
            data.url_length,
            data.domain_length,
            data.num_subdomains,
            data.has_at_symbol,
            data.num_hyphens,
            data.num_underscores,
            data.num_slashes,
            data.num_dots,
            data.is_https,
            data.num_digits,
            data.num_parameters,
            data.path_length,
            data.has_ip,
            data.suspicious_keywords,
            data.entropy,
            data.num_special_chars,
            data.digit_ratio,
            data.tld_length,
            data.risk_score,
            data.feature_0,
            data.feature_1,
            data.feature_2,
            data.feature_3,
            data.feature_4,
            data.feature_5,
            data.feature_6,
            data.feature_7,
            data.feature_8,
            data.feature_9,
            data.feature_10,
            data.feature_11,
            data.feature_12,
            data.feature_13,
            data.feature_14,
            data.feature_15,
            data.feature_16,
            data.feature_17,
            data.feature_18
        ]])
        
        # Realizar predicción
        prediction = int(model.predict(features)[0])
        probabilities = model.predict_proba(features)[0].tolist()
        probability = probabilities[prediction]
        
        # Determinar nivel de riesgo
        if prediction == 0:
            risk_level = "bajo"
        elif probability < 0.7:
            risk_level = "medio"
        else:
            risk_level = "alto"
        
        return PredictionOutput(
            prediction=prediction,
            probability=probability,
            probabilities=probabilities,
            risk_level=risk_level
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en la predicción: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
