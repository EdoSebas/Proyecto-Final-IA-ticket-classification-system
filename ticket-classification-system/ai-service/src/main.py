from fastapi import FastAPI
from contextlib import asynccontextmanager
import threading
import json
import time
from kafka import KafkaConsumer, KafkaProducer
import os
from .model import predict_ticket


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
PRODUCER = None


def get_kafka_producer():
    # Productor usado para devolver a Kafka el resultado de la clasificacion.
    global PRODUCER
    if PRODUCER is None:
        try:
            PRODUCER = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
        except Exception as e:
            print(f"Error connecting to Kafka: {e}")
    return PRODUCER


def consume_and_predict():
    # Consume eventos TicketCreated, ejecuta el modelo y publica TicketClassified.
    consumer = None
    for _ in range(10):
        try:
            consumer = KafkaConsumer(
                "ticket_events",
                bootstrap_servers=KAFKA_BROKER,
                group_id="ai_service_group",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
            )
            print("Started Kafka Consumer in ai-service")
            break
        except Exception as e:
            print(f"Waiting for Kafka to be ready... {e}")
            time.sleep(5)

    if not consumer:
        return

    try:
        for message in consumer:
            event = message.value
            if event.get("event_type") == "TicketCreated":
                print(f"AI Service received ticket: {event}")
                ticket_id = event.get("ticket_id")
                title = event.get("title", "")
                description = event.get("description", "")

                # Combina titulo y descripcion para darle mas contexto al modelo.
                full_text = f"{title} {description}"

                # Ejecuta la prediccion de categoria, prioridad y confianza.
                prediction = predict_ticket(full_text)
                print(f"Prediction for ticket {ticket_id}: {prediction}")

                # Publica el resultado para que ticket-service actualice la base de datos.
                producer = get_kafka_producer()
                if producer:
                    result_event = {
                        "event_type": "TicketClassified",
                        "ticket_id": ticket_id,
                        "ai_category": prediction["ai_category"],
                        "ai_priority": prediction["ai_priority"],
                        "ai_confidence": prediction["ai_confidence"],
                    }
                    producer.send("ticket_events", result_event)
                    producer.flush()
    except Exception as e:
        print(f"AI Consumer failed: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia el consumidor en un hilo secundario al arrancar el servicio de IA.
    thread = threading.Thread(target=consume_and_predict, daemon=True)
    thread.start()
    yield


app = FastAPI(title="AI Classification Service", version="1.0.0", lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-classification"}
