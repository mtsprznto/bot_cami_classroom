import requests

CLIENT_ID = "tu_client_id"
CLIENT_SECRET = "tu_client_secret"
TOKEN_URL = "https://api.canva.com/rest/v1/oauth/token"

# Paso 1: Obtener token de acceso
response = requests.post(TOKEN_URL, data={
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "design:read design:write"
})

access_token = response.json()["access_token"]

# Paso 2: Crear un diseño
headers = {"Authorization": f"Bearer {access_token}"}
design_payload = {
    "name": "Presentación Educativa",
    "type": "presentation"
}

create_response = requests.post(
    "https://api.canva.com/rest/v1/designs",
    headers=headers,
    json=design_payload
)

print(create_response.json())