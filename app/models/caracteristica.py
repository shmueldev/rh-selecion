from sqlmodel import Field, SQLModel

class Caracteristica(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    vacante_id: int = Field(foreign_key="vacante.id")
    tipo: str    # anios_experiencia | titulo | idioma | ciudad | habilidad
    valor: str   # "2", "inglés B1", "nómina"
    texto: str   # lo que lee el reclutador

    