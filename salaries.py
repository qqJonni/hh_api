import requests
import os
from dotenv import load_dotenv, find_dotenv
from statistics import mean
from terminaltables import AsciiTable

load_dotenv(find_dotenv())

languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
vacancies_salary_stats_hh = {}
vacancies_salary_stats_sj = {}

headers = {
    'X-Api-App-Id': os.environ.get('SUPERJOB_SECRET_KEY')
}

for language in languages:
    # HeadHunter API request
    url = "https://api.hh.ru/vacancies?text=программист {}&area=1".format(language)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies_found = data['found']
        vacancies = data['items']
        salaries = []
        for vacancy in vacancies:
            salary = vacancy.get('salary')
            if salary and salary.get('from') is not None and salary.get('to') is not None:
                salaries.append((salary['from'] + salary['to']) / 2)
        average_salary = int(mean(salaries)) if salaries else 0

        vacancies_salary_stats_hh[language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": len(vacancies),
            "average_salary": average_salary
        }
    else:
        print("Ошибка при выполнении запроса:", response.status_code)

    # SuperJob API request
    url = "https://api.superjob.ru/2.0/vacancies/"
    params = {
        'catalogues': 48,
        'town': 4,
        'keyword': "программист {}".format(language)
    }
    response_sj = requests.get(url, headers=headers, params=params)

    if response_sj.status_code == 200:
        data_sj = response_sj.json()
        vacancies_found_sj = len(data_sj['objects'])
        salaries_sj = []
        for vacancy in data_sj['objects']:
            if vacancy['payment_from'] and vacancy['payment_to']:
                salaries_sj.append((vacancy['payment_from'] + vacancy['payment_to']) / 2)
        average_salary_sj = int(mean(salaries_sj)) if salaries_sj else 0

        vacancies_salary_stats_sj[language] = {
            "vacancies_found": vacancies_found_sj,
            "vacancies_processed": len(salaries_sj),
            "average_salary": average_salary_sj
        }
    else:
        print("Ошибка при выполнении запроса:", response_sj.status_code)

# Output
table_data_hh = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]
for lang, data in vacancies_salary_stats_hh.items():
    table_data_hh.append((lang, data['vacancies_found'], data['vacancies_processed'], data['average_salary']))
table_hh = AsciiTable(table_data_hh,"+HeadHunter Moscow------")
print(table_hh.table)

table_data_sj = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]
for lang, data in vacancies_salary_stats_sj.items():
    table_data_sj.append((lang, data['vacancies_found'], data['vacancies_processed'], data['average_salary']))
table_sj = AsciiTable(table_data_sj,"+SuperJob Moscow--------")
print(table_sj.table)
