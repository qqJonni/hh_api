import requests
import os
from dotenv import load_dotenv, find_dotenv
from statistics import mean

load_dotenv(find_dotenv())

languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
vacancies_salary_stats = {}
headers = {
    'X-Api-App-Id': os.environ.get('SUPERJOB_SECRET_KEY')
}

for language in languages:
    url = "https://api.superjob.ru/2.0/vacancies/"
    params = {
        'catalogues': 48,
        'town': 4,
        'keyword': "программист {}".format(language)
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        vacancies_found = len(data['objects'])
        salaries = []
        for vacancy in data['objects']:
            if vacancy['payment_from'] and vacancy['payment_to']:
                salaries.append((vacancy['payment_from'] + vacancy['payment_to']) / 2)
        average_salary = int(mean(salaries)) if salaries else 0

        vacancies_salary_stats[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(salaries),
            "average_salary": average_salary
        }
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

print(vacancies_salary_stats)