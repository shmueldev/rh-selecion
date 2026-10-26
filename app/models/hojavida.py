from datetime import datetime
from sqlmodel import Field, SQLModel
from app.models.tiempo import ahora


class HojaVida(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    invitacion_id: int = Field(foreign_key="invitacion.id", unique=True)
    contenido: str  # JSON del formato ATS
    recibida_en: datetime = Field(default_factory=ahora)
