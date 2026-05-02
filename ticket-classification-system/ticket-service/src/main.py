from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from . import models, schemas, database, kafka_utils

# Crea las tablas definidas en SQLAlchemy si aun no existen.
models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicia el consumidor de Kafka en segundo plano cuando arranca la API.
    kafka_utils.start_kafka_consumer(database.engine)
    yield

app = FastAPI(title="Ticket Classification System API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def root():
    # Endpoint raiz para verificar rapidamente que la API esta disponible.
    return {
        "message": "Ticket Classification System API funcionando",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "crear_ticket": "POST /tickets/",
            "listar_tickets": "GET /tickets/",
            "obtener_ticket": "GET /tickets/{id}",
            "actualizar_ticket": "PUT /tickets/{id}",
            "eliminar_ticket": "DELETE /tickets/{id}"
        }
    }

@app.get("/health")
def health():
    # Health check para Docker, Railway, Kubernetes o pruebas locales.
    return {"status": "ok"}

@app.post("/tickets/", response_model=schemas.TicketResponse, status_code=201)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    # Guarda el ticket y publica un evento para que el servicio de IA lo clasifique.
    db_ticket = models.Ticket(
        title=ticket.title,
        description=ticket.description
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    kafka_utils.publish_ticket_created(db_ticket.id, db_ticket.title, db_ticket.description)
    return db_ticket

@app.get("/tickets/", response_model=list[schemas.TicketResponse])
def read_tickets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    # Lista tickets con paginacion basica.
    tickets = db.query(models.Ticket).offset(skip).limit(limit).all()
    return tickets

@app.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    # Busca un ticket por ID y responde 404 si no existe.
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.put("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(ticket_id: int, ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    # Actualiza titulo y descripcion del ticket.
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db_ticket.title = ticket.title
    db_ticket.description = ticket.description
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@app.delete("/tickets/{ticket_id}", status_code=204)
def delete_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    # Elimina un ticket existente.
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return None
