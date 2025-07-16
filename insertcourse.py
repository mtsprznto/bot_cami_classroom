import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/classroom.courseworkmaterials"]
material = {
    "title": "Lectura sobre APIs REST",
    "description": "Lee el artículo y prepárate para discutirlo en clase.",
    "materials": [
        {
            "link": {
                "url": "https://developer.mozilla.org/es/docs/Web/HTTP/Overview",
                "title": "Introducción a HTTP"
            }
        }
    ]
}







# If modifying these scopes, delete the file token.json.


def main():
  """Shows basic usage of the Classroom API.
  Prints the names of the first 10 courses the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "client_secret_603744710152.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("classroom", "v1", credentials=creds)

    # Call the Classroom API
    
    course_id = "700371563603"
    results = service.courses().courseWorkMaterials().create(courseId=course_id, body=material).execute()
    print(results)
    

    

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()