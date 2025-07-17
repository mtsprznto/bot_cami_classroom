import os

from google_auth_oauthlib.flow import Flow
from fastapi import FastAPI, Request
from pydantic import BaseModel

from .publicar_anuncio import publicar_anuncios_con_links
from .utils.auth import exchange_code_for_token,get_auth_url
from .utils.constantes import TOKEN_ANUNCIO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o ["*"] para dev, pero no en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





SCOPES = ["https://www.googleapis.com/auth/classroom.announcements"]

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
            "QUINTO_PROYECTO": data.canva_5_proyecto,
            "QUINTO_ORIENTACION": data.canva_5_orientacion,
            "SEXTO": data.canva_6,
            "SEXTO_B": data.canva_6
        }

        publicar_anuncios_con_links(links)
        return {"status": "ok", "detalle": "Anuncios publicados exitosamente"}
    
    except Exception as e:
        return {"error": str(e)}
    







@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Código de autorización no recibido"}

    try:
        creds = exchange_code_for_token(code)
        #test
        return RedirectResponse(url="http://localhost:3000")  # ⬅️ redirige al frontend
    except Exception as e:
        return {"error": str(e)}
