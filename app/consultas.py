# Aqui vemos la invitacion que tiene el usuario por medio del token.
# Antes se probó select(Consentimiento).where(Invitacion.token == token).
# Ese select no sirve: el token no es una columna de Consentimiento.
# La fila se busca en Invitacion, que es la tabla donde se guardó el token al invitar.

from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.invitacion import Invitacion


def obtener_invitacion(session: Session, token: str) -> Invitacion:
    # select arma la consulta. exec la corre en la base.
    # where deja solo la fila cuyo token es el de la URL.
    # first() va después de exec y devuelve la primera fila que coincide, o None.
    # Utilizamos first para obtener solo el primer resultado que coincida con los criterios.
    # Si first() se pone dentro del select, esa consulta no se ejecuta.
    invitacion = session.exec(
        select(Invitacion).where(Invitacion.token == token)
    ).first()
    if invitacion is None:
        # 404: la ruta existe, pero no hay una invitación con ese token.
        raise HTTPException(status_code=404, detail="La invitacion no existe")
    # La variable invitacion queda con todos los datos de esa fila: id, correo, estado y vacante_id.
    return invitacion
