# SEAFS Docker Configuration & Deployment Artifacts

## 1. Dockerfile (Production Multi-stage)

```dockerfile
# ============================================================
# SEAFS Production Dockerfile - Multi-stage Build
# ============================================================

# Stage 1: Build dependencies
FROM python:3.11-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Security: Create non-root user
RUN groupadd -r seafs && useradd -r -g seafs seafs

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libblas3 \
    liblapack3 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /home/seafs/.local

# Set environment variables
ENV PATH=/home/seafs/.local/bin:$PATH \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set working directory
WORKDIR /app

# Copy application code
COPY --chown=seafs:seafs app.py .
COPY --chown=seafs:seafs config/ ./config/

# Security: Switch to non-root user
USER seafs

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## 2. Docker Compose (Development)

```yaml
# ============================================================
# docker-compose.yml - Development Environment
# ============================================================

version: '3.8'

services:
  seafs-api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: seafs-api
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
      - DATABASE_URL=postgresql://seafs:seafs@db:5432/seafs
    volumes:
      - ./app.py:/app/app.py:ro
      - ./config:/app/config:ro
    depends_on:
      - db
    networks:
      - seafs-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: seafs-db
    environment:
      - POSTGRES_USER=seafs
      - POSTGRES_PASSWORD=seafs
      - POSTGRES_DB=seafs
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d:ro
    ports:
      - "5432:5432"
    networks:
      - seafs-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U seafs"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: seafs-redis
    ports:
      - "6379:6379"
    networks:
      - seafs-network
    volumes:
      - redis_data:/data

  prometheus:
    image: prom/prometheus:v2.47.0
    container_name: seafs-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - seafs-network

  grafana:
    image: grafana/grafana:10.1.0
    container_name: seafs-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=seafs
    volumes:
      - ./monitoring/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml:ro
      - grafana_data:/var/lib/grafana
    networks:
      - seafs-network
    depends_on:
      - prometheus

networks:
  seafs-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

## 3. Docker Compose (Production)

```yaml
# ============================================================
# docker-compose.prod.yml - Production Environment
# ============================================================

version: '3.8'

services:
  seafs-api:
    build:
      context: .
      dockerfile: Dockerfile
    image: seafs/api:v1.0.0
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=INFO
      - DATABASE_URL=postgresql://seafs:${DB_PASSWORD}@db:5432/seafs
      - REDIS_URL=redis://redis:6379/0
    secrets:
      - db_password
    networks:
      - seafs-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  db:
    image: postgres:15-alpine
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    environment:
      - POSTGRES_USER=seafs
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
      - POSTGRES_DB=seafs
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - seafs-network
    secrets:
      - db_password

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - seafs-api
    networks:
      - seafs-network

secrets:
  db_password:
    external: true

networks:
  seafs-network:
    driver: overlay
    attachable: true

volumes:
  postgres_data:
```

## 4. Kubernetes Deployment

```yaml
# ============================================================
# k8s/seafs-deployment.yaml - Kubernetes Manifests
# ============================================================

apiVersion: apps/v1
kind: Deployment
metadata:
  name: seafs-api
  namespace: seafs
  labels:
    app: seafs-api
    version: v1.0.0
spec:
  replicas: 3
  selector:
    matchLabels:
      app: seafs-api
  template:
    metadata:
      labels:
        app: seafs-api
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: seafs-api
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: seafs-api
        image: seafs/api:v1.0.0
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "INFO"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: seafs-secrets
              key: database-url
        resources:
          requests:
            cpu: "250m"
            memory: "256Mi"
          limits:
            cpu: "1000m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        volumeMounts:
        - name: config
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: config
        configMap:
          name: seafs-config
---
apiVersion: v1
kind: Service
metadata:
  name: seafs-api
  namespace: seafs
spec:
  selector:
    app: seafs-api
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
    name: http
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: seafs-api-hpa
  namespace: seafs
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: seafs-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 5. Build & Deploy Commands

```bash
# ============================================================
# Build & Deploy Commands
# ============================================================

# Build development image
docker build -t seafs/api:dev .

# Build production image
docker build -t seafs/api:v1.0.0 .

# Run development stack
docker-compose up -d

# Run production stack
docker-compose -f docker-compose.prod.yml up -d

# Push to registry
docker tag seafs/api:v1.0.0 registry.example.com/seafs/api:v1.0.0
docker push registry.example.com/seafs/api:v1.0.0

# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n seafs -w
kubectl logs -n seafs -l app=seafs-api --tail=100

# Port forward for local testing
kubectl port-forward -n seafs svc/seafs-api 8000:80

# Run tests in container
docker run --rm seafs/api:dev pytest test_cases.py -v
```
