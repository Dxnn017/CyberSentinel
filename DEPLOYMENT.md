# Guía de Despliegue - CyberSentinel API

## 🚀 Opciones de Despliegue

### 1. Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Iniciar servidor
python app.py

# O usar el script
./start.sh
```

### 2. Docker (Recomendado para Producción)

Crear `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Exponer puerto
EXPOSE 8000

# Comando para iniciar
CMD ["python", "app.py"]
```

Construir y ejecutar:

```bash
# Construir imagen
docker build -t cybersentinel-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 --name cybersentinel cybersentinel-api

# Ver logs
docker logs -f cybersentinel
```

### 3. Docker Compose

Crear `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./mejor_modelo.pkl:/app/mejor_modelo.pkl:ro
```

Ejecutar:

```bash
docker-compose up -d
```

### 4. Servicios en la Nube

#### A. Render

1. Crear `render.yaml`:

```yaml
services:
  - type: web
    name: cybersentinel-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
```

2. Conectar repositorio en [render.com](https://render.com)

#### B. Railway

```bash
# Instalar Railway CLI
npm i -g @railway/cli

# Login y deploy
railway login
railway init
railway up
```

#### C. Google Cloud Run

```bash
# Autenticar
gcloud auth login

# Build y deploy
gcloud run deploy cybersentinel-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### D. AWS Elastic Beanstalk

```bash
# Instalar EB CLI
pip install awsebcli

# Inicializar y deploy
eb init -p python-3.12 cybersentinel-api
eb create cybersentinel-env
eb deploy
```

### 5. Servidor VPS (Ubuntu/Debian)

```bash
# Conectar al servidor
ssh user@your-server-ip

# Instalar dependencias
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clonar proyecto
git clone <tu-repositorio>
cd CyberSentinel

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar gunicorn para producción
pip install gunicorn

# Crear servicio systemd
sudo nano /etc/systemd/system/cybersentinel.service
```

Contenido del servicio:

```ini
[Unit]
Description=CyberSentinel API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/CyberSentinel
Environment="PATH=/path/to/CyberSentinel/venv/bin"
ExecStart=/path/to/CyberSentinel/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Configurar Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Iniciar servicios:

```bash
# Habilitar y iniciar servicio
sudo systemctl enable cybersentinel
sudo systemctl start cybersentinel

# Reiniciar nginx
sudo systemctl restart nginx

# Verificar estado
sudo systemctl status cybersentinel
```

## 🔒 Seguridad en Producción

### 1. Variables de Entorno

Crear `.env`:

```env
API_KEY=tu-api-key-secreta
ALLOWED_ORIGINS=https://tu-dominio.com
MAX_REQUESTS_PER_MINUTE=60
```

### 2. Autenticación API Key

Modificar `app.py`:

```python
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader

API_KEY = "tu-api-key-secreta"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@app.post("/predict", dependencies=[Security(verify_api_key)])
async def predict(data: PredictionInput):
    # ... código existente
```

### 3. CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

### 4. Rate Limiting

```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/predict")
@limiter.limit("10/minute")
async def predict(request: Request, data: PredictionInput):
    # ... código existente
```

## 📊 Monitoreo

### Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas con Prometheus

```bash
pip install prometheus-fastapi-instrumentator
```

```python
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

## 🧪 Testing

```bash
# Tests unitarios
pytest tests/

# Test de carga
locust -f locustfile.py
```

## 📝 Checklist de Producción

- [ ] Variables de entorno configuradas
- [ ] HTTPS habilitado (Let's Encrypt)
- [ ] Autenticación implementada
- [ ] Rate limiting activado
- [ ] CORS configurado
- [ ] Logs configurados
- [ ] Monitoreo activo
- [ ] Backups del modelo
- [ ] Documentación actualizada
- [ ] Health checks funcionando
- [ ] Manejo de errores robusto
