from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.tiempo import ahora


class Revision(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    invitacion_id: int = Field(foreign_key="invitacion.id", unique=True)
    decision: str  # sigue | descartada
    nota: str = Field(default="")
    fecha: datetime = Field(default_factory=ahora)
