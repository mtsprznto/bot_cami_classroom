import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from .constantes import TOKEN_ANUNCIO

load_dotenv()

def obtener_token(token_path: str, scopes: list[str]) -> Credentials:
    """
    Valida o genera las credenciales OAuth para el scope indicado.
    Guarda el token en disco para reuso futuro.
    """

    creds = None
    print("🔍 GOOGLE_REDIRECT_URI:", repr(os.getenv("GOOGLE_REDIRECT_URI")))

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                {
                    "installed": {
                        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                        "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                        "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                        "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
                    }
                },
                scopes=scopes
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return creds



def get_credentials(scopes: list[str]) -> Credentials:
    """
    Valida o genera las credenciales OAuth para el scope indicado.
    Guarda el token en disco para reuso futuro.
    """
    try:
        creds = None

        if os.path.exists(TOKEN_ANUNCIO):
            creds = Credentials.from_authorized_user_file(TOKEN_ANUNCIO, scopes)

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
                    scopes=scopes
                )
                creds = flow.run_local_server(port=0)

            with open(TOKEN_ANUNCIO, "w") as token:
                token.write(creds.to_json())

        return creds
    except Exception as error:
        print("Error en get_credentials", error)
        return None
