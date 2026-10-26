from datetime import datetime

from sqlmodel import Field, SQLModel

from app.models.tiempo import ahora


class Consentimiento(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    invitacion_id: int = Field(foreign_key="invitacion.id", unique=True)
    acepta: bool
    texto_aviso: str
    version_aviso: str = Field(default="1")
    fecha: datetime = Field(default_factory=ahora)
