import requests
import uvicorn
import os

from fastapi import FastAPI, HTTPException, status

app = FastAPI()
api_key = api_key = "a7bc42ee80msh0d4ff0350852678p195558jsnf7e258d86683"

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

@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {'message': 'service alive'}

# Эндпоинт для поиска по трекам
@app.get("/search_tracks/")
async def search_tracks(query: str):
    try:
        results = search_deezer(query, "track")
        tracks = [{'artist': result['artist']['name'], 'track': result['title']} for result in results]
        return tracks
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))