# permite manejar datos en formato estructurado (JSON)
import json

# os y dotenv nos permiten leer creedenciales en formato de texto estructurado (JSON)
import os

from dotenv import load_dotenv

# OpenAI es una libreria que nos permite conectarnos a con el cerebo de la inteligencia artificial
from openai import OpenAI

# Lee el archivo .env y deja RESCUEAI_BASE_URL y RESCUEAI_API_KEY en el entorno.
load_dotenv()

SISTEMA = """
Eres el evaluador de selección de HA Bicicletas. Responde en español (Colombia).
Compara la hoja de vida ATS con los requisitos de la vacante.
Responde solo JSON válido, sin markdown, con esta forma:
{
  "fase_final": "pasa" o "no_pasa",
  "puntaje": número de requisitos que sí cumplió,
  "detalle": [
    {"tipo": "", "valor": "", "cumple": true, "evidencia": "frase corta de la hoja"}
  ]
}
fase_final es "pasa" solo si todos los requisitos se cumplieron.
Si no hay requisitos, fase_final es "no_pasa" y detalle es [].
""".strip()
# strip() quita espacios y saltos de línea al inicio y al final del texto.


def evaluar_hoja(requisitos: list[dict], hoja_ats: str) -> dict:
    # OpenAI es el cliente HTTP. Aquí no habla con OpenAI.com:
    # base_url apunta al servidor de RESCUE y api_key lo autoriza.
    # timeout=120 corta la espera a 120 segundos si la IA no responde.
    # os.environ["NOMBRE"] lee esa variable; si no existe, lanza error.
    client = OpenAI(
        base_url=os.environ["RESCUEAI_BASE_URL"],
        api_key=os.environ["RESCUEAI_API_KEY"],
        timeout=120,
    )
    # dumps convierte el diccionario en texto JSON para mandarlo en el mensaje.
    # ensure_ascii=False conserva tildes y eñes. Con True saldrían como \u00f3.
    # Serializacion
    pedido = json.dumps(
        {"requisitos": requisitos, "hoja_ats": hoja_ats}, ensure_ascii=False
    )

    # cliente es el telefono la conexion que abirmos para comunicarnos con la AI
    # chat informa al sistema que queremos usar
    # completions significa completar texto, le damos un texto inicial y ellas calculan como completar el resto de la historia.
    # create es la funcion de python que empaqueta y lo manda por internet al servidor de la IA
    resp = client.chat.completions.create(
        model="rescue-reason",
        # temperature mide qué tan aleatoria es la respuesta: 0 casi fija, 1 más variada.
        # 0.2 deja la evaluación estable entre una llamada y otra.
        temperature=0.2,
        messages=[
            # system: las reglas fijas del evaluador. user: los datos de esta hoja.
            # le informamos que el va hacer sistema y se comporta como SISTEMA
            {"role": "system", "content": SISTEMA},
            # Aqui informamos los requisistos del user
            {"role": "user", "content": pedido},
        ],
    )
    # choices es la lista de respuestas. [0] es la primera.
    # message.content es el texto. strip() le quita espacios de más.
    # resp.choices: Las IA son capaces de generar varias respuestas diferentes a la vez si se lo pides.
    # El sistema las guarda en una lista llamada choices (opciones).
    # [0]: Como casi siempre solo le pedimos una respuesta, tomamos la primera opción de la lista
    # (en programación, el primer elemento siempre es el número 0).

    texto = resp.choices[0].message.content.strip()
    # A veces el modelo envuelve el JSON en ```json ... ```. Eso no es JSON válido.

    if texto.startswith("```"):
        # strip("`") saca las comillas invertidas de las puntas.
        texto = texto.strip("`")
        # removeprefix("json") quita la palabra json solo si está al inicio.
        texto = texto.removeprefix("json").strip()
    # loads hace lo contrario de dumps: el texto JSON vuelve a ser un diccionario.
    return json.loads(texto)
