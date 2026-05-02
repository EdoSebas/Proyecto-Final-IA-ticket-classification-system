from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Esquema de entrada para crear o actualizar tickets desde la API.
class TicketCreate(BaseModel):
    title: str
    description: str

# Esquema de salida que devuelve la API al cliente.
class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    ai_category: Optional[str] = None
    ai_priority: Optional[str] = None
    ai_confidence: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True
