from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.database import lifespan

# Importamos el router de postulacion
from app.routers.postulacion import router as router_postulacion
from app.routers.vacantes import router

app = FastAPI(lifespan=lifespan)
app.include_router(router)
# Agregamos el router de postulacion
app.include_router(router_postulacion)
# La carpeta frontend está al lado de app, no dentro.
# /pantallas no tapa /admin, /postular ni /docs: esas rutas ya se registraron arriba.
carpeta_frontend = Path(__file__).resolve().parent.parent / "frontend"
app.mount(
    "/pantallas",
    StaticFiles(directory=carpeta_frontend, html=True),
    name="pantallas",
)
