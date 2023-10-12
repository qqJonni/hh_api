import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

headers = {
    'X-Api-App-Id': os.environ.get('SUPERJOB_SECRET_KEY')
}

url = "https://api.superjob.ru/2.0/vacancies/"

params = {
    'catalogues': 48,
    'town': 4,
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    for vacancy in data['objects']:
        print(vacancy['profession'])
else:
    print("Ошибка при выполнении запроса:", response.status_code)