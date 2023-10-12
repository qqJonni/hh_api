import requests

headers = {"User-Agent": "api-test-agent"}
params = {"areas.name": "Москва"}
response = requests.get(url='https://api.hh.ru/vacancies',params=params, headers=headers)

print(response.text)

