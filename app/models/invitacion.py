from datetime import datetime, timedelta
from sqlmodel import Field, SQLModel
from app.models.tiempo import ahora


class Invitacion(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vacante_id: int = Field(foreign_key="vacante.id")
    correo: str
    token: str = Field(unique=True, index=True)
    estado: str = Field(default="creada")  # creada | sin_autorizacion | cv_recibido | evaluada
    creada_en: datetime = Field(default_factory=ahora)
    vence_en: datetime = Field(default_factory=lambda: ahora() + timedelta(days=7))
