from src import database, models


# Datos de demostracion para poblar la tabla tickets sin importar manualmente el CSV.
SEED_TICKETS = [
    ("Mi factura llego con un cobro incorrecto", "Billing", "HIGH"),
    ("Me cobraron dos veces el mismo servicio", "Billing", "HIGH"),
    ("Necesito una copia de mi factura", "Billing", "MEDIUM"),
    ("Cual es el costo del plan premium", "Billing", "LOW"),
    ("No puedo acceder a mi cuenta", "Technical Support", "HIGH"),
    ("La aplicacion se cierra sola al iniciar sesion", "Technical Support", "HIGH"),
    ("El sistema esta caido y no puedo trabajar", "Technical Support", "HIGH"),
    ("Tengo un error 500 al guardar archivos", "Technical Support", "HIGH"),
    ("La pagina carga muy lento desde ayer", "Technical Support", "MEDIUM"),
    ("No me llegan las notificaciones por correo", "Technical Support", "MEDIUM"),
    ("Quiero cancelar mi suscripcion mensual", "Cancellations", "HIGH"),
    ("Deseo dar de baja mi cuenta permanentemente", "Cancellations", "HIGH"),
    ("Quiero cancelar el plan anual y pedir reembolso", "Cancellations", "HIGH"),
    ("Como cancelo mi prueba gratuita", "Cancellations", "MEDIUM"),
    ("Quiero pausar mi suscripcion por un mes", "Cancellations", "MEDIUM"),
    ("Estoy interesado en comprar el plan empresarial", "Sales", "LOW"),
    ("Tienen descuentos para estudiantes", "Sales", "LOW"),
    ("Quiero informacion sobre los planes disponibles", "Sales", "LOW"),
    ("Me gustaria hacer una demo del producto", "Sales", "LOW"),
    ("No entiendo como funciona el sistema", "General", "LOW"),
]


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
