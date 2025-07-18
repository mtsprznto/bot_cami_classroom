
import os
from dotenv import load_dotenv


#Vercel funciona con /tmp y en local con tmp

load_dotenv()

token_anuncio = os.getenv("TOKEN_ANUNCIO")

TOKEN_ANUNCIO = token_anuncio

SCOPES = [
    "https://www.googleapis.com/auth/classroom.announcements",
    "https://www.googleapis.com/auth/classroom.courses.readonly"
]

