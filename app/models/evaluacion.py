from datetime import datetime
from sqlmodel import Field, SQLModel
from app.models.tiempo import ahora


class Evaluacion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    invitacion_id: int = Field(foreign_key="invitacion.id", unique=True)
    fase_final: str  # pasa | no_pasa
    puntaje: int = Field(default=0)
    detalle: str  # JSON: lista de reglas, cumple y evidencia
    fecha: datetime = Field(default_factory=ahora)
