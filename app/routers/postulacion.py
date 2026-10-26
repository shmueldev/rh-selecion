# Rutas de Ana. El token de la URL identifica su invitación.
# La búsqueda de esa fila está en obtener_invitacion.

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.consultas import obtener_invitacion
from app.database.database import SessionDep
from app.models.consentimiento import Consentimiento
from app.models.hojavida import HojaVida
from app.schemas import ConsentimientoEntrada, HojaVidaEntrada

router = APIRouter(tags=["postulacion"])


# ver la invitacion
@router.get("/postular/{token}")
def ver_invitacion(token: str, session: SessionDep):
    # Traemos la ficha completa por el token. Si no existe, obtener_invitacion responde 404.
    invitacion = obtener_invitacion(session, token)
    return {
        "correo": invitacion.correo,
        "estado": invitacion.estado,
        "vacante_id": invitacion.vacante_id,
    }


# Aceptar o Rechazar la invitacion
@router.post("/postular/{token}/consentimiento")
def responder_aviso(token: str, datos: ConsentimientoEntrada, session: SessionDep):
    # La variable invitacion pasa a tener todos los datos de esa fila.
    # Traemos la ficha tecnica completa de Ana.
    invitacion = obtener_invitacion(session, token)

    # Ya tenemos la fila de Ana guardada en invitacion. Utilizamos el id para validar
    # si esa ficha ya tiene un consentimiento.
    ya_respondio = session.exec(
        select(Consentimiento).where(Consentimiento.invitacion_id == invitacion.id)
    ).first()

    if ya_respondio is not None:
        # 409: el recurso ya existe y choca con lo que se intenta guardar otra vez.
        raise HTTPException(
            status_code=409, detail="Esta invitación ya respondio el aviso"
        )

    # Si no acepta, el proceso de esta ficha se detiene.
    if not datos.acepta:
        invitacion.estado = "sin_autorizacion"

    ficha = Consentimiento(
        # Aqui utilizamos el modelo: invitacion_id sale de la fila que acabamos de buscar.
        invitacion_id=invitacion.id,
        # Aqui utilizamos el schema: acepta y texto_aviso vienen del JSON del POST.
        acepta=datos.acepta,
        texto_aviso=datos.texto_aviso,
    )

    session.add(ficha)
    session.commit()
    return {"acepta": datos.acepta, "estado": invitacion.estado}


@router.post("/postular/{token}/hoja")
def recibir_hoja(token: str, datos: HojaVidaEntrada, session: SessionDep):
    # Traemos la ficha de ANA por el token de la URL.
    invitacion = obtener_invitacion(session, token)

    # Confirmamos si hay un consentimiento y que acepta sea verdadero.
    # Sin ese aviso aceptado, Ana no puede cargar la hoja.
    aviso = session.exec(
        select(Consentimiento).where(Consentimiento.invitacion_id == invitacion.id)
    ).first()
    if aviso is None or not aviso.acepta:
        # 403: la invitación sí existe, pero esta persona no tiene permiso de seguir.
        raise HTTPException(status_code=403, detail="El Candidato no autorizo el aviso")

    # Miramos si la ficha tiene Hoja de vida. Cada invitación solo puede tener una.
    ya_cargo = session.exec(
        select(HojaVida).where(HojaVida.invitacion_id == invitacion.id)
    ).first()
    if ya_cargo is not None:
        # 409: la hoja ya existe y no se guarda otra para esta misma invitación.
        raise HTTPException(status_code=409, detail="Esta invitacion ya cargo la hoja")

    # Si todo pasa, el estado cambia a cv_recibido y se guarda el contenido del JSON.
    invitacion.estado = "cv_recibido"
    ficha = HojaVida(invitacion_id=invitacion.id, contenido=datos.contenido)
    session.add(ficha)
    session.commit()
    return {"estado": invitacion.estado}
