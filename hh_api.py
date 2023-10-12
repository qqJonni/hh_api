import requests

url = "https://api.hh.ru/vacancies?text=программист"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

else:
    print("Ошибка при выполнении запроса:", response.status_code)

print(response.text)

