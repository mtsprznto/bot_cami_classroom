# api/obtener_cursos.py
import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

from .utils.constantes import SCOPES
from .utils.get_credentials import get_credentials

load_dotenv()


def obtener_cursos_id():
    try:
        creds = get_credentials(SCOPES)  # ya gestiona el token
        service = build("classroom", "v1", credentials=creds)
        results = service.courses().list(pageSize=50).execute()
        courses = results.get("courses", [])

        if not courses:
            return {"cursos": [], "mensaje": "No se encontraron cursos."}

        cursos_info = [{"name": c["name"], "id": c["id"]} for c in courses]
        return {"cursos": cursos_info}

    except Exception as error:
        return {"error": f"❌ Error al obtener cursos: {error}"}
