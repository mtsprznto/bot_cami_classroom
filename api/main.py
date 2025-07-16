from fastapi import FastAPI
from pydantic import BaseModel
from .publicar_anuncio import publicar_anuncios_con_links

app = FastAPI()

class LinksInput(BaseModel):
    canva_4: str
    canva_5: str
    canva_5_proyecto: str
    canva_5_orientacion: str
    canva_6: str

@app.post("/publicar")
def publicar_links(data: LinksInput):
    links = {
        "CUARTO": data.canva_4,
        "QUINTO": data.canva_5,
        "QUINTO_PROYECTO": data.canva_5_proyecto,
        "QUINTO_ORIENTACION": data.canva_5_orientacion,
        "SEXTO": data.canva_6
    }

    publicar_anuncios_con_links(links)
    return {"status": "ok", "detalle": "Anuncios publicados exitosamente"}