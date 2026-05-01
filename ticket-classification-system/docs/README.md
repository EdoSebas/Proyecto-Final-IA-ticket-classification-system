# Ticket Classification System

Sistema de clasificacion automatica de tickets de soporte usando Machine Learning e Inteligencia Artificial.

## Descripcion

Cuando un usuario envia un ticket describiendo su problema, el sistema automaticamente:
- Clasifica el ticket en categorias: Billing, Technical Support, Cancellations, Sales, General
- Asigna una prioridad: HIGH, MEDIUM, LOW
- Notifica al agente correspondiente

## Arquitectura

El sistema esta compuesto por dos microservicios principales:

- **ticket-service**: Recibe y gestiona los tickets via API REST
- **ai-service**: Clasifica los tickets usando modelos ML/DL

La comunicacion entre servicios se realiza mediante Apache Kafka.

## Tecnologias

- Python 3.10/3.11
- FastAPI
- PostgreSQL
- Apache Kafka
- Docker
- Kubernetes
- scikit-learn (RandomForest + MLP Neural Network)

## Modelos de IA

- **RandomForest**: Modelo ML base con TF-IDF
- **MLP Neural Network**: Red neuronal multicapa con TF-IDF (modelo principal)

## Estructura del proyecto
## Instalacion local

### Requisitos
- Python 3.11
- Docker Desktop
- kubectl

### Pasos

1. Clonar el repositorio
```bash
git clone https://github.com/EdoSebas/Proyecto-Final-IA-ticket-classification-system
cd ticket-classification-system
```

2. Entrenar los modelos
```bash
cd ai-service
pip install scikit-learn pandas numpy joblib
python train_ml.py
python train_dl.py
```

3. Ejecutar pruebas
```bash
cd ..
pip install pytest httpx==0.24.1
python -m pytest tests/ -v
```

4. Desplegar en Kubernetes
```bash
kubectl apply -f k8s/configmap.yml
kubectl apply -f k8s/postgres.yml
kubectl apply -f k8s/ai-service.yml
kubectl apply -f k8s/ticket-service.yml
kubectl apply -f k8s/hpa.yml
```

5. Acceder al sistema
```bash
kubectl port-forward service/ticket-service 9090:8000
```

API disponible en: http://localhost:9090

## Pruebas

```bash
python -m pytest tests/ -v
```

Resultado esperado: 12 pruebas pasando

## CI/CD

El proyecto usa GitHub Actions con tres jobs:
- test-model: entrena y prueba los modelos ML/DL
- test-ticket-service: prueba los endpoints REST
- build-docker: construye las imagenes Docker

## Metricas del modelo

| Modelo | Accuracy Categoria | Accuracy Prioridad |
|--------|-------------------|-------------------|
| RandomForest | 66.67% | 54.17% |
| MLP Neural Network | 93.06% | 95.83% |
