import requests
import uvicorn
import os
from keycloak import KeycloakOpenID
from fastapi import FastAPI, HTTPException, status, Form, Header

app = FastAPI()
api_key = api_key = "a7bc42ee80msh0d4ff0350852678p195558jsnf7e258d86683"

KEYCLOAK_URL = "http://keycloak:8080/"
KEYCLOAK_CLIENT_ID = "testClient"
KEYCLOAK_REALM = "testRealm"
KEYCLOAK_CLIENT_SECRET = "**********"

user_token = ""
keycloak_openid = KeycloakOpenID(server_url=KEYCLOAK_URL,
                                  client_id=KEYCLOAK_CLIENT_ID,
                                  realm_name=KEYCLOAK_REALM,
                                  client_secret_key=KEYCLOAK_CLIENT_SECRET)



from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)

@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(grant_type=["password"],
                                      username=username,
                                      password=password)
        return token
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Не удалось получить токен")

def user_is_musician(token):
    try:
        token_info = keycloak_openid.introspect(token)
        if "test" not in token_info["realm_access"]["roles"]:
            raise HTTPException(status_code=403, detail="Access denied")
        return token_info
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token or access denied")

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive(token: str = Header()):
    if (user_is_musician(token)):
        return {'message': 'service alive'}
    else:
        return "Wrong JWT Token"

# Базовая функция для отправки запросов к Deezer API
def search_deezer(query: str, search_type: str):
    url = "https://deezerdevs-deezer.p.rapidapi.com/search"
    headers = {
        'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
        'x-rapidapi-key': api_key
    }
    params = {"q": f"{search_type}:{query}"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return response.raise_for_status()

# Эндпоинт для поиска по трекам
@app.get("/search_tracks/")
async def search_tracks(query: str, token: str = Header()):
    if (user_is_musician(token)):
        try:
            results = search_deezer(query, "track")
            tracks = [{'artist': result['artist']['name'], 'track': result['title']} for result in results]
            return tracks
        except Exception as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        return "Wrong JWT Token"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))