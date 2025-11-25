"""
CyberSentinel - Extractor de Características de URLs
Basado en el Agente de Análisis y Razonamiento Heurístico del proyecto original
"""

import re
import numpy as np
from urllib.parse import urlparse
import tldextract


class URLFeatureExtractor:
    """
    Agente de Análisis: Extrae características relevantes de las URLs
    Implementa razonamiento heurístico basado en reglas expertas
    """

    def __init__(self):
        self.suspicious_keywords = [
            'login', 'verify', 'account', 'update', 'secure', 'banking',
            'confirm', 'suspend', 'restore', 'click', 'password', 'signin'
        ]

    def extract_features(self, url):
        """
        Extrae las 19 características de una URL
        
        Args:
            url (str): URL a analizar
            
        Returns:
            dict: Diccionario con las 19 características
        """
        features = {}

        try:
            # Parsear URL
            parsed = urlparse(url)
            extracted = tldextract.extract(url)

            # 1. Longitud de la URL
            features['url_length'] = len(url)

            # 2. Longitud del dominio
            features['domain_length'] = len(parsed.netloc)

            # 3. Número de subdominios
            features['num_subdomains'] = len(extracted.subdomain.split('.')) if extracted.subdomain else 0

            # 4. Presencia de @ en URL (regla heurística)
            features['has_at_symbol'] = 1 if '@' in url else 0

            # 5. Número de guiones
            features['num_hyphens'] = url.count('-')

            # 6. Número de underscores
            features['num_underscores'] = url.count('_')

            # 7. Número de barras
            features['num_slashes'] = url.count('/')

            # 8. Número de puntos
            features['num_dots'] = url.count('.')

            # 9. Uso de HTTPS (regla heurística)
            features['is_https'] = 1 if parsed.scheme == 'https' else 0

            # 10. Número de dígitos en URL
            features['num_digits'] = sum(c.isdigit() for c in url)

            # 11. Número de parámetros
            features['num_parameters'] = len(parsed.query.split('&')) if parsed.query else 0

            # 12. Longitud del path
            features['path_length'] = len(parsed.path)

            # 13. Presencia de IP en URL (regla heurística)
            features['has_ip'] = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) else 0

            # 14. Palabras clave sospechosas (razonamiento heurístico)
            url_lower = url.lower()
            features['suspicious_keywords'] = sum(1 for kw in self.suspicious_keywords if kw in url_lower)

            # 15. Entropía de la URL (medida de aleatoriedad)
            features['entropy'] = self._calculate_entropy(url)

            # 16. Caracteres especiales
            special_chars = set('!@#$%^&*()+=[]{}|;:,<>?')
            features['num_special_chars'] = sum(1 for c in url if c in special_chars)

            # 17. Ratio de dígitos
            features['digit_ratio'] = features['num_digits'] / len(url) if len(url) > 0 else 0

            # 18. TLD (Top Level Domain)
            features['tld_length'] = len(extracted.suffix)

            # 19. Razonamiento heurístico: Puntuación de riesgo
            features['risk_score'] = self._calculate_risk_score(features)

        except Exception as e:
            print(f"Error procesando URL: {url[:50]}... - {str(e)}")
            # Retornar características por defecto en caso de error
            features = {
                'url_length': 0, 'domain_length': 0, 'num_subdomains': 0,
                'has_at_symbol': 0, 'num_hyphens': 0, 'num_underscores': 0,
                'num_slashes': 0, 'num_dots': 0, 'is_https': 0,
                'num_digits': 0, 'num_parameters': 0, 'path_length': 0,
                'has_ip': 0, 'suspicious_keywords': 0, 'entropy': 0,
                'num_special_chars': 0, 'digit_ratio': 0, 'tld_length': 0,
                'risk_score': 0
            }

        return features

    def extract_features_array(self, url, scaler=None):
        """
        Extrae características y las devuelve como array NumPy con 38 features
        (19 originales + 19 normalizadas con el scaler del entrenamiento)
        
        Args:
            url (str): URL a analizar
            scaler: MinMaxScaler usado en el entrenamiento (opcional)
                   Si no se proporciona, intenta cargar desde 'scaler.pkl'
            
        Returns:
            numpy.ndarray: Array con las 38 características en orden
        """
        import joblib
        import os
        
        features = self.extract_features(url)
        
        # Orden correcto de características según el modelo
        feature_order = [
            'url_length', 'domain_length', 'num_subdomains', 'has_at_symbol',
            'num_hyphens', 'num_underscores', 'num_slashes', 'num_dots',
            'is_https', 'num_digits', 'num_parameters', 'path_length',
            'has_ip', 'suspicious_keywords', 'entropy', 'num_special_chars',
            'digit_ratio', 'tld_length', 'risk_score'
        ]
        
        # Extraer las 19 características originales
        original_features = np.array([[features[key] for key in feature_order]])
        
        # Duplicar las características: 19 + 19 = 38
        # (En el notebook se hizo así antes de normalizar)
        features_38 = np.concatenate([original_features, original_features], axis=1)
        
        # Cargar scaler si no fue proporcionado
        if scaler is None:
            scaler_path = 'scaler.pkl'
            if os.path.exists(scaler_path):
                scaler = joblib.load(scaler_path)
            else:
                print(f"⚠️ Warning: Scaler not found at {scaler_path}")
        
        # Normalizar las 38 características usando el scaler
        if scaler is not None:
            features_normalized = scaler.transform(features_38)
            return features_normalized
        else:
            # Fallback: normalización manual si no hay scaler disponible
            print("⚠️ Using fallback normalization (less accurate)")
            # Normalizar solo las segundas 19
            data_min = np.array([11.0, 4.0, 0.0, 0.0, 0.0, 0.0, 2.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.792, 0.0, 0.0, 0.0, 0.0])
            data_max = np.array([392.0, 89.0, 7.0, 1.0, 27.0, 11.0, 28.0, 18.0, 1.0, 127.0, 30.0, 293.0, 1.0, 9.0, 5.986, 27.0, 0.5, 8.0, 16.0])
            normalized = (original_features - data_min) / (data_max - data_min)
            normalized = np.clip(normalized, 0, 1)
            return np.concatenate([original_features, normalized], axis=1)

    def _calculate_entropy(self, text):
        """
        Calcula la entropía de Shannon de un texto
        
        Args:
            text (str): Texto para calcular entropía
            
        Returns:
            float: Valor de entropía
        """
        if not text:
            return 0
        entropy = 0
        for char in set(text):
            prob = text.count(char) / len(text)
            entropy -= prob * np.log2(prob)
        return entropy

    def _calculate_risk_score(self, features):
        """
        Sistema Experto: Calcula puntuación de riesgo basada en reglas heurísticas
        If-Then rules para detección preliminar
        
        Args:
            features (dict): Diccionario con características extraídas
            
        Returns:
            int: Puntuación de riesgo (0-16)
        """
        score = 0

        # Regla 1: URLs muy largas son sospechosas
        if features['url_length'] > 75:
            score += 2

        # Regla 2: Presencia de @ es altamente sospechoso
        if features['has_at_symbol'] == 1:
            score += 3

        # Regla 3: Muchos subdominios son sospechosos
        if features['num_subdomains'] > 3:
            score += 2

        # Regla 4: Sin HTTPS aumenta riesgo
        if features['is_https'] == 0:
            score += 1

        # Regla 5: Palabras clave sospechosas
        if features['suspicious_keywords'] > 2:
            score += 3

        # Regla 6: IP en URL es muy sospechoso
        if features['has_ip'] == 1:
            score += 3

        # Regla 7: Alta entropía indica aleatorización
        if features['entropy'] > 4:
            score += 2

        return score


if __name__ == "__main__":
    # Test del extractor
    print("=" * 70)
    print("TEST DEL EXTRACTOR DE CARACTERÍSTICAS")
    print("=" * 70)
    
    extractor = URLFeatureExtractor()
    
    # URLs de ejemplo
    test_urls = [
        "https://www.google.com",
        "http://suspicious-paypa1.verify-account.login.phishing.com/secure?id=12345",
        "https://github.com/user/repo",
        "http://192.168.1.1/admin/login.php"
    ]
    
    for url in test_urls:
        print(f"\n🔍 Analizando: {url}")
        print("-" * 70)
        features = extractor.extract_features(url)
        for key, value in features.items():
            print(f"  {key:25s}: {value}")
        print(f"\n  📊 Risk Score: {features['risk_score']}/16")
