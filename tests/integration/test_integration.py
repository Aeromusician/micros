import asyncpg
import requests
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'mymusic_service/app'))
sys.path.append(str(BASE_DIR / 'tracksearch_service/app'))

from mymusic_service.app.main import service_alive as mymusic_status
from tracksearch_service.app.main import service_alive as tracksearch_status

@pytest.mark.asyncio
async def test_database_connection():
    try:
        connection = await asyncpg.connect("postgresql://secUREusER:StrongEnoughPassword)@51.250.26.59:5432/query")
        assert connection
        await connection.close()
    except Exception as e:
        assert False, f"Не удалось подключиться к базе данных: {e}"

@pytest.mark.asyncio
async def test_quotes_api():
    url = "https://deezerdevs-deezer.p.rapidapi.com/search"
    headers = {
        'x-rapidapi-host': "deezerdevs-deezer.p.rapidapi.com",
        'x-rapidapi-key': "a7bc42ee80msh0d4ff0350852678p195558jsnf7e258d86683"
    }
    response = requests.get(url, headers=headers, params={"q": "test"})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_mymusic_service_connection():
    r = await mymusic_status()
    assert r == {'message': 'service alive'}

@pytest.mark.asyncio
async def test_tracksearch_service_connection():
    r = await tracksearch_status()
    assert r == {'message': 'service alive'}