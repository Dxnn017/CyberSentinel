import streamlit as st
import requests
import json
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="CyberSentinel - Detección de Phishing",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URL de la API desplegada
API_URL = "https://cybersentinel-csdr.onrender.com"

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        border-radius: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .safe-badge {
        background-color: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .danger-badge {
        background-color: #ef4444;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    .warning-badge {
        background-color: #f59e0b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/security-shield-green.png", width=100)
    st.title("🛡️ CyberSentinel")
    st.markdown("---")
    st.markdown("### Acerca del Sistema")
    st.info("""
    **CyberSentinel** utiliza inteligencia artificial avanzada para detectar sitios web de phishing.
    
    - 🤖 Modelo: LightGBM
    - 📊 Precisión: 99.47%
    - 🔍 Características: 19 indicadores
    """)
    st.markdown("---")
    st.markdown("### ¿Cómo funciona?")
    st.write("""
    1. Ingresa la URL a analizar
    2. El sistema extrae características
    3. El modelo IA evalúa el riesgo
    4. Obtienes un resultado instantáneo
    """)
    st.markdown("---")
    st.markdown("**Desarrollado con ❤️**")

# Header principal
st.title("🛡️ CyberSentinel - Detección de Phishing")
st.markdown("### Protege tu navegación con Inteligencia Artificial")
st.markdown("---")

# Verificar estado de la API
with st.spinner("Verificando conexión con la API..."):
    try:
        health_response = requests.get(f"{API_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            st.success("✅ API conectada y lista")
            with st.expander("ℹ️ Estado del Sistema"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Estado", health_data.get("status", "N/A"))
                with col2:
                    st.metric("Modelo", health_data.get("model_type", "N/A"))
                with col3:
                    st.metric("Características", health_data.get("n_features", "N/A"))
        else:
            st.error("⚠️ La API no está respondiendo correctamente")
    except Exception as e:
        st.error(f"❌ Error de conexión: {str(e)}")

st.markdown("---")

# Input de URL
st.subheader("🔍 Analizar URL")
col1, col2 = st.columns([4, 1])

with col1:
    url_input = st.text_input(
        "Ingresa la URL que deseas analizar:",
        placeholder="https://ejemplo.com",
        help="Ingresa la URL completa, incluyendo http:// o https://"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🔎 Analizar", type="primary", use_container_width=True)

# URLs de ejemplo
st.markdown("**📋 Ejemplos de prueba:**")
example_col1, example_col2 = st.columns(2)
with example_col1:
    if st.button("✅ Sitio legítimo (Google)", use_container_width=True):
        url_input = "https://google.com"
        analyze_button = True
with example_col2:
    if st.button("⚠️ URL sospechosa", use_container_width=True):
        url_input = "http://secure-login-verify.suspicious-site.com/account/verify"
        analyze_button = True

# Análisis
if analyze_button and url_input:
    if not url_input.startswith(('http://', 'https://')):
        st.error("⚠️ Por favor, ingresa una URL válida que comience con http:// o https://")
    else:
        with st.spinner(f"🔍 Analizando {url_input}..."):
            try:
                # Llamar a la API
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"url": url_input},
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.markdown("---")
                    st.subheader("📊 Resultados del Análisis")
                    
                    # Resultado principal
                    is_phishing = result.get("is_phishing", False)
                    confidence = result.get("confidence", 0) * 100
                    risk_level = result.get("risk_level", "unknown")
                    
                    if is_phishing:
                        st.markdown(f'<div style="text-align: center;"><span class="danger-badge">⚠️ PHISHING DETECTADO - {confidence:.2f}% confianza</span></div>', unsafe_allow_html=True)
                        st.error(f"🚨 **Esta URL es peligrosa y puede ser un sitio de phishing.**")
                    else:
                        st.markdown(f'<div style="text-align: center;"><span class="safe-badge">✅ SITIO SEGURO - {confidence:.2f}% confianza</span></div>', unsafe_allow_html=True)
                        st.success(f"✅ **Esta URL parece ser legítima.**")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Métricas principales
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Nivel de Riesgo", risk_level.upper())
                    
                    with col2:
                        st.metric("Confianza", f"{confidence:.2f}%")
                    
                    with col3:
                        prob_phishing = result.get("probabilities", {}).get("phishing", 0) * 100
                        st.metric("Prob. Phishing", f"{prob_phishing:.2f}%")
                    
                    with col4:
                        heuristic_score = result.get("heuristic_score", 0)
                        st.metric("Score Heurístico", f"{heuristic_score}/16")
                    
                    # Barra de probabilidad
                    st.markdown("### 📈 Probabilidades del Modelo")
                    prob_legitimate = result.get("probabilities", {}).get("legitimate", 0) * 100
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.progress(prob_legitimate / 100, text=f"Legítimo: {prob_legitimate:.2f}%")
                    with col2:
                        st.progress(prob_phishing / 100, text=f"Phishing: {prob_phishing:.2f}%")
                    
                    # Características extraídas
                    st.markdown("### 🔬 Características Analizadas")
                    features = result.get("features", {})
                    
                    if features:
                        # Organizar características en tabs
                        tab1, tab2, tab3 = st.tabs(["📏 Estructura", "🔐 Seguridad", "⚠️ Indicadores"])
                        
                        with tab1:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Longitud URL", features.get("url_length", 0))
                                st.metric("Longitud Dominio", features.get("domain_length", 0))
                            with col2:
                                st.metric("Subdominios", features.get("num_subdomains", 0))
                                st.metric("Longitud Path", features.get("path_length", 0))
                            with col3:
                                st.metric("Puntos", features.get("num_dots", 0))
                                st.metric("Guiones", features.get("num_hyphens", 0))
                        
                        with tab2:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                https_status = "✅ Sí" if features.get("is_https", 0) == 1 else "❌ No"
                                st.metric("HTTPS", https_status)
                            with col2:
                                has_ip = "⚠️ Sí" if features.get("has_ip", 0) == 1 else "✅ No"
                                st.metric("Contiene IP", has_ip)
                            with col3:
                                st.metric("Longitud TLD", features.get("tld_length", 0))
                        
                        with tab3:
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Palabras Sospechosas", features.get("suspicious_keywords", 0))
                                st.metric("Símbolo @", "⚠️ Sí" if features.get("has_at_symbol", 0) == 1 else "✅ No")
                            with col2:
                                st.metric("Entropía", f"{features.get('entropy', 0):.2f}")
                                st.metric("Ratio Dígitos", f"{features.get('digit_ratio', 0):.2f}")
                            with col3:
                                st.metric("Caracteres Especiales", features.get("num_special_chars", 0))
                                st.metric("Parámetros", features.get("num_parameters", 0))
                    
                    # Recomendaciones
                    st.markdown("### 💡 Recomendaciones")
                    if is_phishing:
                        st.warning("""
                        **🚨 Acción Recomendada:**
                        - ❌ NO ingreses información personal
                        - ❌ NO hagas clic en enlaces de esta página
                        - ✅ Reporta este sitio
                        - ✅ Cierra inmediatamente la pestaña
                        """)
                    else:
                        if heuristic_score > 5:
                            st.warning("""
                            **⚠️ Precaución:**
                            - El sitio parece legítimo pero tiene algunos indicadores sospechosos
                            - Verifica la URL cuidadosamente
                            - Usa autenticación de dos factores si es posible
                            """)
                        else:
                            st.success("""
                            **✅ Sitio Seguro:**
                            - La URL no presenta indicadores de phishing
                            - Sin embargo, siempre verifica que sea el sitio correcto
                            - Mantén tu navegador actualizado
                            """)
                    
                    # Timestamp
                    st.markdown("---")
                    st.caption(f"⏰ Análisis realizado el {datetime.now().strftime('%d/%m/%Y a las %H:%M:%S')}")
                    
                    # Botón para analizar otra URL
                    if st.button("🔄 Analizar otra URL", type="secondary"):
                        st.rerun()
                        
                else:
                    st.error(f"❌ Error en la API: {response.status_code}")
                    st.json(response.json())
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ La solicitud tardó demasiado. Por favor, intenta nuevamente.")
            except requests.exceptions.ConnectionError:
                st.error("🔌 No se pudo conectar con la API. Verifica tu conexión a internet.")
            except Exception as e:
                st.error(f"❌ Error inesperado: {str(e)}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🛡️ CyberSentinel**")
    st.caption("Sistema de Detección de Phishing")
with col2:
    st.markdown("**📊 Tecnologías**")
    st.caption("FastAPI • LightGBM • Streamlit")
with col3:
    st.markdown("**🔗 API**")
    st.caption(f"[{API_URL}]({API_URL})")
