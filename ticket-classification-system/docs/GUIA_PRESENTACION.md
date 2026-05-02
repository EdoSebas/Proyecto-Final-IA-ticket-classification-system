# Guia de presentacion del proyecto

## 1. Introduccion

Explica el problema:

> El proyecto resuelve la clasificacion automatica de tickets de soporte. Un usuario escribe un problema y el sistema predice la categoria del ticket y su prioridad.

Categorias usadas:

- Billing
- Technical Support
- Cancellations
- Sales
- General

Prioridades:

- HIGH
- MEDIUM
- LOW

## 2. Arquitectura general

Muestra la idea de microservicios:

- `ticket-service`: API REST para crear y consultar tickets.
- `ai-service`: servicio de inteligencia artificial que clasifica texto.
- `PostgreSQL`: base de datos de tickets.
- `Kafka`: mensajeria asincrona entre servicios.
- `Docker`: contenedores locales.
- `Kubernetes`: manifiestos de despliegue.
- `Railway`: despliegue en la nube.

Frase sugerida:

> La arquitectura separa la gestion de tickets de la clasificacion de IA. Esto permite escalar la API y el modelo por separado.

## 3. Explicar el flujo

Orden del flujo:

1. El usuario crea un ticket en `POST /tickets/`.
2. `ticket-service` guarda el ticket en PostgreSQL.
3. `ticket-service` publica un evento `TicketCreated` en Kafka.
4. `ai-service` consume el evento.
5. `ai-service` ejecuta `predict_ticket()`.
6. `ai-service` publica `TicketClassified`.
7. `ticket-service` actualiza `ai_category`, `ai_priority` y `ai_confidence`.

## 4. Dataset y modelo de IA

Archivo principal:

```text
ai-service/dataset_tickets.csv
```

Comandos para entrenar:

```powershell
cd C:\Users\juans\OneDrive\Desktop\PROYECTO-FINAL-IA-2026\ticket-classification-system\ai-service
python train_ml.py
python train_dl.py
```

Explicacion:

> El dataset contiene textos etiquetados con categoria y prioridad. El entrenamiento convierte los textos en vectores numericos usando TF-IDF y luego entrena modelos para predecir la categoria y la prioridad.

Modelos:

- `train_ml.py`: TF-IDF + RandomForest.
- `train_dl.py`: TF-IDF + MLPClassifier.
- `src/model.py`: carga el modelo entrenado y expone `predict_ticket()`.

## 5. Pruebas del modelo

Desde la raiz del proyecto:

```powershell
cd C:\Users\juans\OneDrive\Desktop\PROYECTO-FINAL-IA-2026\ticket-classification-system
python -m pytest tests/test_model.py -v
```

Prueba manual:

```powershell
cd ai-service
python
```

Dentro de Python:

```python
from src.model import predict_ticket

predict_ticket("Me cobraron doble este mes")
predict_ticket("No puedo iniciar sesion")
predict_ticket("Quiero cancelar mi plan")
predict_ticket("Estoy interesado en comprar licencias")
```

Para salir:

```python
exit()
```

## 6. Pruebas generales del sistema

Desde la raiz:

```powershell
python -m pytest tests/ -v
```

Explicacion:

> Esta suite prueba tanto el modelo de IA como endpoints basicos del servicio de tickets.

## 7. Docker local

Levantar base de datos y API:

```powershell
cd C:\Users\juans\OneDrive\Desktop\PROYECTO-FINAL-IA-2026\ticket-classification-system
docker compose up -d --build
```

Cargar datos de demostracion:

```powershell
docker compose exec ticket-service python seed_tickets.py
```

Probar health check:

```powershell
curl.exe http://localhost:8000/health
```

Ver documentacion Swagger:

```text
http://localhost:8000/docs
```

Listar tickets:

```powershell
curl.exe http://localhost:8000/tickets/
```

## 8. Base de datos local

Entrar a PostgreSQL:

```powershell
docker exec -it ticket_classification_db psql -U admin -d tickets_db
```

Comandos utiles dentro de PostgreSQL:

```sql
\dt
\d tickets
SELECT id, title, ai_category, ai_priority FROM tickets ORDER BY id;
SELECT ai_category, COUNT(*) FROM tickets GROUP BY ai_category;
SELECT ai_priority, COUNT(*) FROM tickets GROUP BY ai_priority;
\q
```

## 9. API REST

Endpoints principales:

- `GET /`: informacion general.
- `GET /health`: estado de la API.
- `POST /tickets/`: crear ticket.
- `GET /tickets/`: listar tickets.
- `GET /tickets/{id}`: consultar ticket.
- `PUT /tickets/{id}`: actualizar ticket.
- `DELETE /tickets/{id}`: eliminar ticket.

Ejemplo de creacion de ticket:

```powershell
curl.exe -X POST http://localhost:8000/tickets/ -H "Content-Type: application/json" -d "{\"title\":\"No puedo iniciar sesion\",\"description\":\"La plataforma no me deja entrar con mi usuario\"}"
```

## 10. Despliegue en la nube

URL de Railway:

```text
https://proyecto-final-ia-ticket-classification-system-production.up.railway.app
```

Pruebas:

```powershell
curl.exe https://proyecto-final-ia-ticket-classification-system-production.up.railway.app/health
curl.exe https://proyecto-final-ia-ticket-classification-system-production.up.railway.app/tickets/
```

Swagger:

```text
https://proyecto-final-ia-ticket-classification-system-production.up.railway.app/docs
```

## 11. CI/CD

Explica:

> El proyecto incluye GitHub Actions para ejecutar pruebas y validar la construccion de Docker. Railway despliega automaticamente cuando se suben cambios a GitHub.

Comandos de entrega:

```powershell
git status
git add .
git commit -m "docs: add presentation comments and guide"
git push
```

## 12. Buenas practicas

Menciona:

- Separacion por microservicios.
- Variables de entorno para configuracion.
- Contenedores Docker.
- Pruebas automatizadas.
- Documentacion de endpoints.
- Modelo entrenado separado de la API.
- Base de datos persistente.
- Despliegue cloud con Railway.

## 13. Cierre

Frase sugerida:

> El sistema demuestra una arquitectura completa de IA aplicada a soporte: recibe tickets, los almacena, clasifica automaticamente categoria y prioridad, expone endpoints REST, usa contenedores, tiene pruebas y puede desplegarse en la nube.
