import requests

languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
vacancies_count = {}

for language in languages:
    url = "https://api.hh.ru/vacancies?text=программист {}&area=1".format(language)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies_count[language] = data['found']
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

print(vacancies_count)

