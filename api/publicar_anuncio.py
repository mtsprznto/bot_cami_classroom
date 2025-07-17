# api/publicar_anuncio.py
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google_auth_oauthlib.flow import Flow

import os
import asyncio

from dinamic_announ import create_announcement

from .ia.bot import teacher_bot
from .utils.utils import validate_announcement_payload
from .utils.constantes import TOKEN_ANUNCIO
from dotenv import load_dotenv


load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/classroom.announcements"]
#TOKEN_SCOPE = "token_addanuncio_v.json"

def get_credentials():
    creds = None

    if os.path.exists(TOKEN_ANUNCIO):
        creds = Credentials.from_authorized_user_file(TOKEN_ANUNCIO, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_config(
                {
                    "installed": {
                        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                        "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                        "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
                    }
                },
                scopes=SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_ANUNCIO, "w") as token:
            token.write(creds.to_json())

    return creds



def formatear_links_para_publicar(raw_data: dict) -> dict:
    curso_id_map = {
        "CUARTO": "700371563603",
        "QUINTO": "789411510193",
        "QUINTO_PROYECTO": "751898942407",
        "QUINTO_ORIENTACION": "751899058480",
        "SEXTO": "789412726197"
        # Agregá más si querés incluir SextoB, QuintoB, etc.
    }

    links_por_curso = {}

    for nombre_curso, url in raw_data.items():
        course_id = curso_id_map.get(nombre_curso)
        if not course_id:
            print(f"🔎 Curso desconocido: {nombre_curso}")
            continue

        links_por_curso.setdefault(course_id, []).append({
            "url": url,
            "title": f"Presentación {nombre_curso.capitalize()}"
        })

    return links_por_curso



def publicar_anuncios_con_links(links_por_curso: dict):
    """
    links_por_curso = {
        "700371563603": [
            {"url": "https://canva.com/...", "title": "Presentación Lenguaje"},
            {"url": "https://canva.com/...", "title": "Presentación Matemática"}
        ],
        "782388106581": [
            {"url": "https://canva.com/...", "title": "¿Qué es una API?"}
        ]
    }
    """
    print(links_por_curso)
    links_por_curso = formatear_links_para_publicar(links_por_curso)
    
    if not os.path.exists(TOKEN_ANUNCIO):
        raise RuntimeError("❌ No se encontró el token de autenticación. Ejecutá el flujo OAuth primero.")

    creds = get_credentials()

    try:
        service = build("classroom", "v1", credentials=creds)
        #print("LINKS POR CURSO",links_por_curso.items())
        
        
        for course_id, materiales in links_por_curso.items():
            for material in materiales:
                try:
                    texto = asyncio.run(teacher_bot())
                    print("MATERIAL ", material)
                    anuncio = create_announcement(
                        text=texto,
                        add_link=True,
                        link_url=str(material["url"]),
                        link_title=str(material["title"])
                    )
                    validate_announcement_payload(anuncio)
                    result = service.courses().announcements().create(
                        courseId=course_id, body=anuncio
                    ).execute()
                    print(f"✅ Publicado en curso {course_id}: {result['text']}")
                except ValueError as err:
                    print(f"⚠️ Anuncio omitido en curso {course_id}: {err}")
                except HttpError as error:
                    print(f"❌ Error en curso {course_id}: {error}")

    except HttpError as error:
        print(f"🚨 Error global al conectar con Classroom API: {error}")