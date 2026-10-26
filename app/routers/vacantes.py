import json
import secrets

from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from app.consultas import obtener_invitacion
from app.database.database import SessionDep
from app.models.caracteristica import Caracteristica
from app.models.evaluacion import Evaluacion
from app.models.hojavida import HojaVida
from app.models.invitacion import Invitacion
from app.models.vacante import Vacante
from app.schemas import InvitacionEntrada, VacanteEntrada
from app.services.evaluacion import evaluar_hoja

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/vacantes", status_code=status.HTTP_201_CREATED)
def crear_vacante(datos: VacanteEntrada, session: SessionDep):
    vacante = Vacante(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        ciudad=datos.ciudad,
        modalidad=datos.modalidad,
    )
    session.add(vacante)
    session.commit()
    session.refresh(vacante)

    for item in datos.caracteristicas:
        session.add(
            Caracteristica(
                vacante_id=vacante.id,
                tipo=item.tipo,
                valor=item.valor,
                texto=item.texto,
            )
        )
    session.commit()

    return {
        "id": vacante.id,
        "titulo": vacante.titulo,
        "estado": vacante.estado,
        "cantidad_caracteristicas": len(datos.caracteristicas),
    }


@router.get("/vacantes")
def listar_vacantes(session: SessionDep):
    return session.exec(select(Vacante)).all()


# Invitacion
@router.post("/vacantes/{vacante_id}/invitar")
def invitar(vacante_id: int, datos: InvitacionEntrada, session: SessionDep):
    vacante = session.get(Vacante, vacante_id)

    # Validamos que el id de la ruta este en Vacante
    if vacante is None:
        raise HTTPException(status_code=404, detail="La vacante no existe")

    respuestas = []
    for correo in datos.correos:
        # Generacion de Token
        token = f"VAC-{vacante_id}-{secrets.token_hex(3)}"
        # Invitacion la Clase Modelo
        ficha = Invitacion(vacante_id=vacante_id, correo=correo, token=token)
        session.add(ficha)
        # Agregamos las repuestas a la lista
        respuestas.append(
            {
                "correo": correo,
                "enlace": f"http://127.0.0.1:8000/postular/{token}",
                "asunto": f"Vacante {vacante.titulo} {token}",
            }
        )
    session.commit()
    return respuestas


# Evaluar la CV. Lo dispara el admin, por eso vive en este router y la URL lleva /admin.
@router.post("/invitaciones/{token}/evaluar")
def evaluar(token: str, session: SessionDep):
    # Traemos la ficha completa. Si el token no existe, obtener_invitacion responde 404.
    invitacion = obtener_invitacion(session, token)
    if invitacion.estado != "cv_recibido":
        # 409: la ficha existe, pero todavía no tiene una hoja lista para evaluar.
        raise HTTPException(
            status_code=409, detail="La hoja todavía no está lista para evaluar"
        )

    # select arma la consulta. exec la corre en la base. first() toma la primera fila o None.
    # first() va después de exec. Si se pone dentro del select, esa consulta no se ejecuta.
    ya = session.exec(
        select(Evaluacion).where(Evaluacion.invitacion_id == invitacion.id)
    ).first()
    if ya is not None:
        # 409: esta invitación ya tiene evaluación y no se guarda otra.
        raise HTTPException(status_code=409, detail="Esta invitación ya fue evaluada")

    hoja_fila = session.exec(
        select(HojaVida).where(HojaVida.invitacion_id == invitacion.id)
    ).first()
    # all() trae todas las filas que coinciden, no solo la primera.
    # Una vacante puede tener varias características.
    caracteristicas = session.exec(
        select(Caracteristica).where(Caracteristica.vacante_id == invitacion.vacante_id)
    ).all()

    # Lista por comprensión: un diccionario por cada característica.
    # La evaluación recibe tipo, valor y texto, no el objeto de la tabla.
    requisitos = [
        {"tipo": car.tipo, "valor": car.valor, "texto": car.texto}
        for car in caracteristicas
    ]

    # evaluar_hoja manda los requisitos y la hoja ATS a RescueAI y devuelve el JSON.
    resultado = evaluar_hoja(requisitos, hoja_fila.contenido)
    # El JSON de la IA es un diccionario. ["fase_final"] saca esa clave.
    fase_final = resultado["fase_final"]
    # not in comprueba que el valor no sea ninguno de esos dos.
    if fase_final not in ("pasa", "no_pasa"):
        # 502: nuestro servidor llamó a la IA, pero la respuesta no sirve.
        raise HTTPException(
            status_code=502, detail="La evaluacion no trae una fase valida"
        )

    invitacion.estado = "evaluada"
    session.add(
        Evaluacion(
            invitacion_id=invitacion.id,
            fase_final=fase_final,
            # int() convierte el número del JSON (a veces llega como 3.0) en entero.
            puntaje=int(resultado["puntaje"]),
            # dumps pasa la lista de Python a un texto JSON, porque detalle es str.
            # ensure_ascii=False deja tildes y eñes tal cual: "Bogotá".
            # Con True (el valor por defecto) las cambiaría por códigos \u00f3, \u00e1.
            detalle=json.dumps(resultado["detalle"], ensure_ascii=False),
        )
    )

    session.commit()
    return resultado
