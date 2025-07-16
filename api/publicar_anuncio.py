# api/publicar_anuncio.py

import os
import asyncio
from ia.bot import teacher_bot
from utils import validate_announcement_payload
from dinamic_announ import create_announcement

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/classroom.announcements"]
TOKEN_SCOPE = "token_addanuncio.json"
CLIENT_SECRET_FILE = "client_secret_603744710152.json"

def get_credentials():
    creds = None

    if os.path.exists(TOKEN_SCOPE):
        creds = Credentials.from_authorized_user_file(TOKEN_SCOPE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_SCOPE, "w") as token:
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