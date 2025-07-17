import os
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
from .constantes import TOKEN_ANUNCIO



load_dotenv()
SCOPES = ["https://www.googleapis.com/auth/classroom.announcements"]


def get_auth_url():
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    if not redirect_uri:
        raise RuntimeError("Falta definir GOOGLE_REDIRECT_URI en el entorno")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "redirect_uris": [redirect_uri]  # esto es parte del client_config
            }
        },
        scopes=["https://www.googleapis.com/auth/classroom.announcements"],
        redirect_uri=redirect_uri  # ⬅️ esto es clave
    )

    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return auth_url


def exchange_code_for_token(code: str):
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
    if not redirect_uri:
        raise RuntimeError("Falta definir GOOGLE_REDIRECT_URI en el entorno")

    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": os.getenv("GOOGLE_AUTH_URI", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": os.getenv("GOOGLE_TOKEN_URI", "https://oauth2.googleapis.com/token"),
                "redirect_uris": [redirect_uri]
            }
        },
        scopes=SCOPES,
        redirect_uri=redirect_uri  # 👈 esto es clave para evitar el error
    )

    flow.fetch_token(code=code)
    creds = flow.credentials

    with open(TOKEN_ANUNCIO, "w") as token:
        token.write(creds.to_json())

    return creds

