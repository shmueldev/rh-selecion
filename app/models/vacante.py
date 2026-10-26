from datetime import datetime
from sqlmodel import Field, SQLModel
from app.models.tiempo import ahora

class Vacante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    ciudad: str
    estado: str = Field(default="abierta")  # abierta | cerrada
    modalidad: str = Field(default="presencial")  # presencial | remoto | hibrido
    creada_en: datetime = Field(default_factory=ahora)
