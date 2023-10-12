import requests
from statistics import mean

languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
vacancies_salary_stats = {}

for language in languages:
    url = "https://api.hh.ru/vacancies?text=программист {}&area=1".format(language)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies_found = data['found']
        vacancies = data['items'][:20]
        salaries = []
        for vacancy in vacancies:
            salary = vacancy.get('salary')
            if salary and salary.get('from') is not None and salary.get('to') is not None:
                salaries.append((salary['from'] + salary['to']) / 2)
        average_salary = int(mean(salaries)) if salaries else 0

        vacancies_salary_stats[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(vacancies),
            "average_salary": average_salary
        }
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

print(vacancies_salary_stats)