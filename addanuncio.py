import os.path
from ia.bot import teacher_bot
import asyncio

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from dinamic_announ import create_announcement
from utils import validate_announcement_payload

SCOPES = ["https://www.googleapis.com/auth/classroom.announcements"]
TOKEN_SCOPE = "token_addanuncio.json"

# Texto tiene que ser generado por un bot de ia
# los link tienen que ser las presentaciones de canvas, con url solo para poder ver

"""
Conseguirme las id de los courses que tiene que subir 
"""
# Name: SextoB, ID: 789412787024
# Name: SextoA, ID: 789412726197
# Name: QuintoB, ID: 789412718429
# Name: QuintoA, ID: 789411510193
# Name: CuartoB, ID: 782388106581
# Name: CuartoA, ID: 700371563603

CUARTO_A = "700371563603"
CUARTO_B= "782388106581"
QUINTO_A = "789411510193"
QUINTO_B="789412718429"
SEXTO_A="789412726197"
SEXTO_B="789412787024"

ID_COURSES = [CUARTO_A,CUARTO_B,QUINTO_A,QUINTO_B,SEXTO_A,SEXTO_B]




# Crear un bot personalido para que hable como una profesora de enseñanza básica


# Estos link se actualizan cada semana

links_canva = [
    "https://www.canva.com/design/DAGrMu_ZU6I/nFICmZivipwHKXfFQksaog/edit?utm_content=DAGrMu_ZU6I&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton",
    "https://www.canva.com/design/DAGrMu_ZU6I/nFICmZivipwHKXfFQksaog/edit?utm_content=DAGrMu_ZU6I&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton",
    "https://www.canva.com/design/DAGrMu_ZU6I/nFICmZivipwHKXfFQksaog/edit?utm_content=DAGrMu_ZU6I&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton"
]
INPUT_LINK_CANVA_4 = str(input("Ingrese link canva 4 básico: "))
INPUT_LINK_CANVA_5 = str(input("Ingrese link canva 5 básico: "))
INPUT_LINK_CANVA_6 = str(input("Ingrese link canva 6 básico: "))


bot_texts = [
    asyncio.run(teacher_bot()),
    asyncio.run(teacher_bot()),
    asyncio.run(teacher_bot()),
    asyncio.run(teacher_bot()),
    asyncio.run(teacher_bot()),
    asyncio.run(teacher_bot())
]

announcements = [
    create_announcement(
        text=bot_texts[0],
        add_link=True,
        link_url=INPUT_LINK_CANVA_4,
        link_title="Presentación Lenguaje"
    ),
    create_announcement(
        text=bot_texts[1],
        add_link=True,
        link_url=INPUT_LINK_CANVA_4,
        link_title="Presentación Lenguaje"
    ),
    create_announcement(
        text=bot_texts[2],
        add_link=True,
        link_url=INPUT_LINK_CANVA_5,
        link_title="Presentación Lenguaje"
    ),
    create_announcement(
        text=bot_texts[3],
        add_link=True,
        link_url=INPUT_LINK_CANVA_5,
        link_title="Presentación Lenguaje"
    ),
    create_announcement(
        text=bot_texts[4],
        add_link=True,
        link_url=INPUT_LINK_CANVA_6,
        link_title="Presentación Lenguaje"
    ),
    create_announcement(
        text=bot_texts[5],
        add_link=True,
        link_url=INPUT_LINK_CANVA_6,
        link_title="Presentación Lenguaje"
    )
]




#----------------------



def main():
  creds = None
 
  if os.path.exists(TOKEN_SCOPE):
    creds = Credentials.from_authorized_user_file(TOKEN_SCOPE, SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret_603744710152.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(TOKEN_SCOPE, "w") as token:
      token.write(creds.to_json())

  try:
    service = build("classroom", "v1", credentials=creds)

    # Call the Classroom API
    
    for course_id, announcement in zip(ID_COURSES, announcements):
      try:
        validate_announcement_payload(announcement)
        result = service.courses().announcements().create(courseId=course_id, body=announcement).execute()
        print(f"Publicado en curso {course_id}: {result['text']}")
      except ValueError as err:
        print(f"Anuncio omitido para curso {course_id}: {err}")
      except HttpError as error:
        print(f"Error en curso {course_id}: {error}")

            

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()