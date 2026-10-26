from sqlmodel import SQLModel


class CaracteristicaEntrada(SQLModel):
    tipo: str
    valor: str
    texto: str


class VacanteEntrada(SQLModel):
    titulo: str
    descripcion: str
    ciudad: str
    modalidad: str = "presencial"
    caracteristicas: list[CaracteristicaEntrada]


class InvitacionEntrada(SQLModel):
    correos: list[str]


class ConsentimientoEntrada(SQLModel):
    acepta: bool
    texto_aviso: str


class HojaVidaEntrada(SQLModel):
    contenido: str