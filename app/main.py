from fastapi import FastAPI
from app.database.database import lifespan
from app.routers.vacantes import router
# Importamos el router de postulacion
from app.routers.postulacion import router as router_postulacion

app = FastAPI(lifespan = lifespan)
app.include_router(router)
# Agregamos el router de postulacion
app.include_router(router_postulacion)