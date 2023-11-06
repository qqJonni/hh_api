import requests
import os
from dotenv import load_dotenv, find_dotenv
from statistics import mean
from terminaltables import AsciiTable

load_dotenv(find_dotenv())


def get_hh_vacancy_data(language):
    base_url = "https://api.hh.ru/vacancies"
    vacancies_found = 0
    salaries = []

    for page in range(0, 10):  # Adjust the number of pages to fetch as needed
        params = {
            'text': f"программист {language}",
            'area': 1,
            'page': page
        }
        response = requests.get(base_url, params=params)
        if response.ok:
            data = response.json()
            vacancies_found = data['found']
            vacancies = data['items']
            for vacancy in vacancies:
                salary = vacancy.get('salary')
                if salary and salary.get('from') and salary.get('to'):
                    salaries.append((salary['from'] + salary['to']) / 2)
        else:
            print(f"Ошибка при выполнении запроса (HH) для {language}: {response.status_code}")

    average_salary = int(mean(salaries)) if salaries else 0
    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }


def get_sj_vacancy_data(language, sj_secret_key):
    base_url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_found_sj = 0
    salaries_sj = []

    for page in range(0, 10):  # Adjust the number of pages to fetch as needed
        params = {
            'catalogues': 48,
            'town': 4,
            'keyword': f"программист {language}",
            'page': page
        }
        headers = {
            'X-Api-App-Id': sj_secret_key
        }
        response_sj = requests.get(base_url, headers=headers, params=params)
        if response_sj.ok:
            data_sj = response_sj.json()
            vacancies_found_sj += len(data_sj['objects'])
            for vacancy in data_sj['objects']:
                if vacancy['payment_from'] and vacancy['payment_to']:
                    salaries_sj.append((vacancy['payment_from'] + vacancy['payment_to']) / 2)
        else:
            print(f"Ошибка при выполнении запроса (SuperJob) для {language}: {response_sj.status_code}")

    average_salary_sj = int(mean(salaries_sj)) if salaries_sj else 0
    return {
        "vacancies_found": vacancies_found_sj,
        "vacancies_processed": len(salaries_sj),
        "average_salary": average_salary_sj
    }


def main():
    languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
    vacancies_salary_stats_hh = {}
    vacancies_salary_stats_sj = {}
    sj_secret_key = os.environ.get('SUPERJOB_SECRET_KEY')

    for language in languages:
        hh_data = get_hh_vacancy_data(language)
        if hh_data:
            vacancies_salary_stats_hh[language] = hh_data

        sj_data = get_sj_vacancy_data(language, sj_secret_key)
        if sj_data:
            vacancies_salary_stats_sj[language] = sj_data

    # Output
    table_data_hh = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]
    for lang, data in vacancies_salary_stats_hh.items():
        table_data_hh.append((lang, data['vacancies_found'], data['vacancies_processed'], data['average_salary']))
    table_hh = AsciiTable(table_data_hh, "+HeadHunter Moscow------")
    print(table_hh.table)

    table_data_sj = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]
    for lang, data in vacancies_salary_stats_sj.items():
        table_data_sj.append((lang, data['vacancies_found'], data['vacancies_processed'], data['average_salary']))
    table_sj = AsciiTable(table_data_sj, "+SuperJob Moscow--------")
    print(table_sj.table)


if __name__ == "__main__":
    main()
