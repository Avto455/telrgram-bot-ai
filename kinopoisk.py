import requests
import os
from dotenv import load_dotenv
from pprint import pprint

# import config

load_dotenv()
API_TOKEN = "15EC93C-AHBMA5G-J4H20FY-Z292TJJ"
BASE_URL = 'https://api.kinopoisk.dev'


def config_request(part_request, params=None):  # функция с получением параметров
    headers = {
        "accept": "application/json",
        "X-API-KEY": API_TOKEN
    }
    url = f'{BASE_URL}/v1.3/movie/{part_request}'
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Error: {response.status_code}'}

# response = config_request(666) # передаем часть адреса random для вывода случайного фильма
# pprint(response)


def print_film(movie):
    title = movie['name']
    year = movie['year']
    description = movie['description']
    rating = movie['rating']['kp']
    poster_url = movie['poster']['url']
    message = (
        f"🎬 **{title}** ({year})\n"
        f"⭐️ Рейтинг: {rating}\n"
        f"📜 Полное описание: {description}\n"
        f"\n![Постер]({poster_url})"
    )
    return message

