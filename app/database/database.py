from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy import event
from sqlmodel import SQLModel, Session, create_engine

import app.models

sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(
    sqlite_url,
    echo=True,
    connect_args={"check_same_thread": False}
)

# SQLite no activa las llaves foraneas por defecto
@event.listens_for(engine, "connect")
def activar_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# LIFESPAN controla el ciclo de vida (crea tablas al arrancar)
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
