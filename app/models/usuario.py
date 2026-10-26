# Modelado Usuario
from sqlmodel import Field, SQLModel

class Usuario(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    correo: str = Field(unique=True, index=True)
    clave_hash: str
    rol: str  # admin | reclutador