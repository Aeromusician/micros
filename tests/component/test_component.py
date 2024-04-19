import requests

# URL-адреса для сервиса управления треками
track_service_url = 'http://localhost:8000'
get_tracks_url = f'{track_service_url}/get_tracks'
get_track_by_id_url = f'{track_service_url}/get_track_by_id'
add_track_url = f'{track_service_url}/add_track'
delete_track_url = f'{track_service_url}/delete_track'

# Эндпоинты для поиска музыки
search_service_url = 'http://localhost:8001'
search_artists_url = f'{search_service_url}/search_artists'
search_tracks_url = f'{search_service_url}/search_tracks'
search_albums_url = f'{search_service_url}/search_albums'
search_years_url = f'{search_service_url}/search_years'

# API Key для доступа к Deezer API
api_key = 'a7bc42ee80msh0d4ff0350852678p195558jsnf7e258d86683'


# Тестовые данные
new_track = {
    "id": 1,
    "title": "Imagine",
    "artist": "John Lennon",
    "release_date": "1971-10-11",
    "genre": "Pop"
}

def test_add_track():
    res = requests.post(f"{add_track_url}", json=new_track)
    assert res.status_code == 200

def test_get_tracks():
    res = requests.get(f"{get_tracks_url}")
    assert res.status_code == 200
    assert len(res.json()) > 0

def test_get_track_by_id():
    res = requests.get(f"{get_track_by_id_url}?track_id=1")
    assert res.status_code == 200
    assert res.json()['id'] == new_track['id']

def test_delete_track():
    res = requests.delete(f"{delete_track_url}?track_id=1")
    assert res.status_code == 200
    assert res.text == '"Success"'

def test_search_tracks():
    res = requests.get(f"{search_tracks_url}?query=Bohemian Rhapsody")
    assert res.status_code == 200
    assert any('Bohemian Rhapsody' in track['track'] for track in res.json())
