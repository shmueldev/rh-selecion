1. BD
2. Modelos
3. Main Import models
4. Schemas


requirements.txt
.env
app/main.py                 # arranque y rutas
app/config.py               # lee el .env
app/db.py                   # SQLite
app/models.py               # tablas
app/schemas.py              # cuerpos JSON
app/deps.py                 # admin o reclutador según el token de sesión
app/routers/auth.py
app/routers/vacantes.py
app/routers/postulacion.py
app/routers/reclutador.py
app/services/correo.py      # consola ahora; Graph después
app/services/evaluacion.py  # IA falsa ahora; HTTP después
app/services/reglas.py      # años, idioma, ciudad, habilidad
app/templates/aviso.html
app/templates/formato_cv.html
app/templates/resultados.html
app/templates/vacante_nueva.html