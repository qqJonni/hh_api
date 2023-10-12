import requests

languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
vacancies_count = {}
vacancies_salaries = {}

for language in languages:
    url = "https://api.hh.ru/vacancies?text=программист {}&area=1".format(language)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies_count[language] = data['found']
        vacancies_salaries[language] = []
        vacancies = data['items']
        for vacancy in vacancies:
            if vacancy['salary'] is not None:
                vacancies_salaries[language].append(vacancy['salary'])
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

print("Количество вакансий:", vacancies_count)
print("Вакансии Зарплаты:", vacancies_salaries)

