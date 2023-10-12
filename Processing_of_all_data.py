import requests
from statistics import mean

languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
vacancies_salary_stats = {}

for language in languages:
    url = f"https://api.hh.ru/vacancies?text=программист%20{language}&area=1"
    response = requests.get(url)
    vacancies_salary_stats[language] = {
        "vacancies_found": 0,
        "vacancies_processed": 0,
        "average_salary": 0
    }

    if response.status_code == 200:
        data = response.json()
        vacancies_found = data['found']
        vacancies = data['items']
        page = 0
        shown_vacancies = []

        while len(shown_vacancies) < min(1000, vacancies_found):
            page += 1
            url = f"https://api.hh.ru/vacancies?text=программист%20{language}&area=1&page={page}"
            response = requests.get(url)

            if response.status_code == 200:
                page_data = response.json()
                shown_vacancies.extend(page_data['items'])
                print(f"Скачивание вакансий для {language}. Страница {page} скачен.")
            else:
                print(f"Ошибка получения данных для {language}. Страница {page}")

        salaries = []
        for vacancy in shown_vacancies:
            salary = vacancy.get('salary')
            if salary and salary.get('from') is not None and salary.get('to') is not None:
                salaries.append((salary['from'] + salary['to']) / 2)

        average_salary = int(mean(salaries)) if salaries else 0
        vacancies_salary_stats[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(shown_vacancies),
            "average_salary": average_salary
        }

        print(f"Статистика по {language}.")
    else:
        print(f"Ошибка получения данных для {language}")

print(vacancies_salary_stats)
