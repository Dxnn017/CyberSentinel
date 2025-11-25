import requests
import json

# URL de la API (ajustar según donde esté corriendo)
API_URL = "http://localhost:8000"

def test_health():
    """Probar el endpoint de salud"""
    print("=== Test: Health Check ===")
    response = requests.get(f"{API_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_prediction():
    """Probar el endpoint de predicción"""
    print("=== Test: Prediction ===")
    
    # Datos de ejemplo
    data = {
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
    
    response = requests.post(f"{API_URL}/predict", json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

if __name__ == "__main__":
    try:
        # Probar salud
        test_health()
        
        # Probar predicción
        test_prediction()
        
    except requests.exceptions.ConnectionError:
        print("Error: No se pudo conectar a la API. ¿Está corriendo el servidor?")
    except Exception as e:
        print(f"Error: {e}")
