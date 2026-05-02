import json
import threading
import time
from kafka import KafkaProducer, KafkaConsumer
import os


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
PRODUCER = None


def get_kafka_producer():
    # Crea un productor Kafka reutilizable para publicar eventos del ticket-service.
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


def publish_ticket_created(ticket_id: int, title: str, description: str):
    # Publica el evento que avisa al ai-service que existe un ticket nuevo.
    producer = get_kafka_producer()
    if producer:
        event = {
            "event_type": "TicketCreated",
            "ticket_id": ticket_id,
            "title": title,
            "description": description,
        }
        producer.send("ticket_events", event)
        producer.flush()


def consume_ticket_classified(engine):
    # Escucha eventos de clasificacion y actualiza el ticket en la base de datos.
    from . import models
    from sqlalchemy.orm import sessionmaker

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Intentos de reconexion mientras Kafka termina de arrancar.
    consumer = None
    for _ in range(10):
        try:
            consumer = KafkaConsumer(
                "ticket_events",
                bootstrap_servers=KAFKA_BROKER,
                group_id="ticket_service_group",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                auto_offset_reset="earliest",
            )
            print("Started Kafka Consumer in ticket-service")
            break
        except Exception as e:
            print(f"Waiting for Kafka to be ready... {e}")
            time.sleep(5)

    if not consumer:
        return

    try:
        for message in consumer:
            event = message.value
            if event.get("event_type") == "TicketClassified":
                ticket_id = event.get("ticket_id")
                ai_category = event.get("ai_category")
                ai_priority = event.get("ai_priority")
                ai_confidence = event.get("ai_confidence")

                db = SessionLocal()
                try:
                    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
                    if ticket:
                        ticket.ai_category = ai_category
                        ticket.ai_priority = ai_priority
                        ticket.ai_confidence = ai_confidence
                        ticket.status = "IN_PROGRESS"
                        db.commit()
                        print(f"Ticket {ticket_id} updated with AI classification.")
                except Exception as e:
                    print(f"Error updating ticket: {e}")
                finally:
                    db.close()
    except Exception as e:
        print(f"Consumer failed: {e}")


def start_kafka_consumer(engine):
    # Ejecuta el consumidor en un hilo daemon para no bloquear FastAPI.
    thread = threading.Thread(target=consume_ticket_classified, args=(engine,), daemon=True)
    thread.start()
