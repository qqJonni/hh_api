import requests

headers = {"User-Agent": "api-test-agent"}
response = requests.get(url='https://api.hh.ru/vacancies')

print(response.text)
