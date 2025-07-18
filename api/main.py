import os
from dotenv import load_dotenv

from google_auth_oauthlib.flow import Flow

from pydantic import BaseModel

from .publicar_anuncio import publicar_anuncios_con_links
from .utils.auth import exchange_code_for_token,get_auth_url
from .utils.constantes import TOKEN_ANUNCIO

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .obtener_cursos_id import obtener_cursos_id

app = FastAPI()

frontend_url = os.getenv("URL_FRONTEND")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url,"http://localhost:3000"],  # o ["*"] para dev, pero no en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()



@app.get("/")
def home():
    return {"status": "ok", "detalle": "Bienvenido al API de Anuncios"}


class LinksInput(BaseModel):
    canva_4: str
    canva_5: str
    canva_5_proyecto: str
    canva_5_orientacion: str
    canva_6: str

@app.post("/publicar")
def publicar_links(data: LinksInput):
    try:
        if not os.path.exists(TOKEN_ANUNCIO):
            auth_url = get_auth_url()
            return {
                "status": "oauth_required",
                "message": "No hay token, autorizá primero",
                "auth_url": auth_url
            }



        links = {
            "CUARTO": data.canva_4,
            "CUARTO_B": data.canva_4,
            "QUINTO": data.canva_5,
            "QUINTO_B": data.canva_5,
            "QUINTO_ORIENTACION": data.canva_5_orientacion,
            "QUINTO_PROYECTO": data.canva_5_proyecto,
            "QUINTO_B_PROYECTO": data.canva_5_proyecto,
            "SEXTO": data.canva_6,
            "SEXTO_B": data.canva_6
        }

        publicar_anuncios_con_links(links)
        return {"status": "ok", "detalle": "Anuncios publicados exitosamente"}
    
    except Exception as e:
        return {"[/publicar] error": str(e)}
    







@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Código de autorización no recibido"}

    try:
        creds = exchange_code_for_token(code)
        #test
        frontend_url = os.getenv("URL_FRONTEND")
        if not frontend_url:
            raise RuntimeError("No se definió URL_FRONTEND en las variables de entorno")

        return RedirectResponse(url=frontend_url)
    except Exception as e:
        return {"error": str(e)}



@app.get("/obtener_ids_cursos")
def obtener_ids_cursos():
    """
    Obtiene los ids de los cursos
    """
    try:
        if not os.path.exists(TOKEN_ANUNCIO):
            auth_url = get_auth_url()
            return {
                "status": "oauth_required",
                "message": "No hay token, autorizá primero",
                "auth_url": auth_url
            }
            
        
        resultado = obtener_cursos_id()
        return resultado
    except Exception as e:
        return {"[/obtener_ids_cursos] error": str(e)}
    