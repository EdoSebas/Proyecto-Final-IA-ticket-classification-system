from src import database, models
from src.seed_data import SEED_TICKETS


def seed_database():
    # Crea la tabla si no existe, limpia datos previos y reinicia el contador de IDs.
    models.Base.metadata.create_all(bind=database.engine)

    with database.engine.begin() as connection:
        connection.execute(models.Ticket.__table__.delete())
        dialect = database.engine.dialect.name
        if dialect == "postgresql":
            connection.exec_driver_sql("ALTER SEQUENCE tickets_id_seq RESTART WITH 1")
        elif dialect in {"mysql", "mariadb"}:
            connection.exec_driver_sql("ALTER TABLE tickets AUTO_INCREMENT = 1")
        elif dialect == "sqlite":
            connection.exec_driver_sql("DELETE FROM sqlite_sequence WHERE name = 'tickets'")
        else:
            print(f"No se reinicio el contador de IDs para el motor: {dialect}")

    db = database.SessionLocal()
    try:
        # Convierte cada ejemplo en un registro Ticket listo para insertar.
        tickets = [
            models.Ticket(
                title=title,
                description=title,
                status="OPEN",
                ai_category=category,
                ai_priority=priority,
                ai_confidence=1.0,
            )
            for title, category, priority in SEED_TICKETS
        ]
        db.add_all(tickets)
        db.commit()
        print(f"Base de datos sembrada con {len(tickets)} tickets.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
