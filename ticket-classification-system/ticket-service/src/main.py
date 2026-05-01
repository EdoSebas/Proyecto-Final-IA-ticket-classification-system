from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from . import models, schemas, database, kafka_utils

models.Base.metadata.create_all(bind=database.engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    kafka_utils.start_kafka_consumer(database.engine)
    yield

app = FastAPI(title="Ticket Service API", version="1.0.0", lifespan=lifespan)

@app.post("/tickets/", response_model=schemas.TicketResponse, status_code=201)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
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
    tickets = db.query(models.Ticket).offset(skip).limit(limit).all()
    return tickets

@app.get("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def read_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@app.put("/tickets/{ticket_id}", response_model=schemas.TicketResponse)
def update_ticket(ticket_id: int, ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
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
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return None
