from datetime import date, time
from pydantic import BaseModel, Field


class Evento(BaseModel):
    titulo: str = Field(..., min_length=1)
    descricao: str
    data: date
    horario: time
    local: str
    capacidade: int = Field(..., gt=0)
    categoria: str
