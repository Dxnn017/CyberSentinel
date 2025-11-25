"""
Ejemplo de uso de la API CyberSentinel
Muestra cómo enviar datos al modelo y recibir predicciones
"""

import requests
import json

API_URL = "http://localhost:8000"

# Ejemplo 1: URL segura (características de bajo riesgo)
ejemplo_seguro = {
    "url_length": 35.0,
    "domain_length": 12.0,
    "num_subdomains": 1.0,
    "has_at_symbol": 0.0,
    "num_hyphens": 0.0,
    "num_underscores": 0.0,
    "num_slashes": 2.0,
    "num_dots": 1.0,
    "is_https": 1.0,
    "num_digits": 0.0,
    "num_parameters": 0.0,
    "path_length": 10.0,
    "has_ip": 0.0,
    "suspicious_keywords": 0.0,
    "entropy": 3.2,
    "num_special_chars": 2.0,
    "digit_ratio": 0.0,
    "tld_length": 3.0,
    "risk_score": 0.1,
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

# Ejemplo 2: URL sospechosa (características de alto riesgo)
ejemplo_sospechoso = {
    "url_length": 150.0,
    "domain_length": 45.0,
    "num_subdomains": 5.0,
    "has_at_symbol": 1.0,
    "num_hyphens": 8.0,
    "num_underscores": 3.0,
    "num_slashes": 10.0,
    "num_dots": 8.0,
    "is_https": 0.0,
    "num_digits": 25.0,
    "num_parameters": 5.0,
    "path_length": 80.0,
    "has_ip": 1.0,
    "suspicious_keywords": 3.0,
    "entropy": 4.8,
    "num_special_chars": 20.0,
    "digit_ratio": 0.35,
    "tld_length": 2.0,
    "risk_score": 0.85,
    "feature_0": 1.0,
    "feature_1": 0.5,
    "feature_2": 0.8,
    "feature_3": 0.3,
    "feature_4": 0.9,
    "feature_5": 0.2,
    "feature_6": 0.7,
    "feature_7": 0.4,
    "feature_8": 0.6,
    "feature_9": 0.1,
    "feature_10": 0.8,
    "feature_11": 0.3,
    "feature_12": 0.5,
    "feature_13": 0.9,
    "feature_14": 0.2,
    "feature_15": 0.6,
    "feature_16": 0.4,
    "feature_17": 0.7,
    "feature_18": 0.8
}

def hacer_prediccion(datos, nombre_ejemplo):
    """Realiza una predicción y muestra los resultados"""
    print(f"\n{'='*60}")
    print(f"  {nombre_ejemplo}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(f"{API_URL}/predict", json=datos)
        response.raise_for_status()
        
        resultado = response.json()
        
        print(f"\n📊 Resultado:")
        print(f"  • Predicción: {resultado['prediction']}")
        print(f"  • Probabilidad: {resultado['probability']:.2%}")
        print(f"  • Nivel de riesgo: {resultado['risk_level'].upper()}")
        print(f"\n📈 Probabilidades por clase:")
        print(f"  • Clase 0 (Seguro): {resultado['probabilities'][0]:.2%}")
        print(f"  • Clase 1 (Amenaza): {resultado['probabilities'][1]:.2%}")
        
        # Interpretación
        if resultado['prediction'] == 0:
            print(f"\n✅ Resultado: URL clasificada como SEGURA")
        else:
            print(f"\n⚠️ Resultado: URL clasificada como AMENAZA")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error: No se pudo conectar a la API en {API_URL}")
        print("   Asegúrate de que el servidor esté corriendo.")
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Error HTTP: {e}")
        print(f"   Respuesta: {response.text}")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    print("\n" + "="*60)
    print("  CYBERSENTINEL - EJEMPLOS DE PREDICCIÓN")
    print("="*60)
    
    # Verificar que la API está disponible
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            print("\n✅ API disponible y funcionando correctamente")
        else:
            print("\n⚠️ La API respondió con un código inesperado")
    except:
        print(f"\n❌ No se pudo conectar a la API en {API_URL}")
        print("   Ejecuta la API primero con: python app.py")
        return
    
    # Ejemplo 1: URL segura
    hacer_prediccion(ejemplo_seguro, "Ejemplo 1: URL Segura")
    
    # Ejemplo 2: URL sospechosa
    hacer_prediccion(ejemplo_sospechoso, "Ejemplo 2: URL Sospechosa")
    
    print("\n" + "="*60)
    print("  FIN DE LOS EJEMPLOS")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
