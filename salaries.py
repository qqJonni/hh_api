import requests
import os
from dotenv import load_dotenv, find_dotenv
from statistics import mean
from terminaltables import AsciiTable

AREA_MOSCOW_HH = 1
CATALOGUE_PROGRAMMING_SJ = 48
TOWN_MOSCOW_SJ = 4


def get_hh_vacancy_salaries(language):
    base_url = "https://api.hh.ru/vacancies"
    vacancies_found = 0
    salaries = []

    page = 0
    while True:
        params = {
            'text': f"программист {language}",
            'area': AREA_MOSCOW_HH,
            'page': page
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raises an HTTPError for bad responses
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка при выполнении запроса (HH) для {language}: {e}")
            break

        content = response.json()
        vacancies_found = content['found']
        vacancies = content['items']
        for vacancy in vacancies:
            salary = vacancy.get('salary')
            if salary and salary.get('from') and salary.get('to'):
                salaries.append((salary['from'] + salary['to']) / 2)
            if salary and salary.get('from'):
                salaries.append((salary['from']*1.2))
            if salary and salary.get('to'):
                salaries.append((salary['to']*0.8))
        page += 1
        if not content['pages'] or page >= content['pages']:
            break

    average_salary = int(mean(salaries)) if salaries else 0
    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }


def get_sj_vacancy_salaries(language, sj_secret_key):
    base_url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_found_sj = 0
    salaries_sj = []

    page = 0
    while True:
        params = {
            'catalogues': CATALOGUE_PROGRAMMING_SJ,
            'town': TOWN_MOSCOW_SJ,
            'keyword': f"программист {language}",
            'page': page,
            'period': 1
        }
        headers = {
            'X-Api-App-Id': sj_secret_key
        }
        try:
            response_sj = requests.get(base_url, headers=headers, params=params)
            response_sj.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка при выполнении запроса (SuperJob) для {language}: {e}")
            break

        content_sj = response_sj.json()
        vacancies_found_sj = content_sj.get('total', 0)

        for vacancy in content_sj.get('objects', []):
            if vacancy.get('payment_from') and vacancy.get('payment_to'):
                salaries_sj.append((vacancy['payment_from'] + vacancy['payment_to']) / 2)
            elif vacancy.get('payment_from'):
                salaries_sj.append(vacancy['payment_from'] * 1.2)
            elif vacancy.get('payment_to'):
                salaries_sj.append(vacancy['payment_to'] * 0.8)

        page += 1
        if not content_sj.get('more') or not content_sj.get('objects'):
            break

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
        try:
            hh_content = get_hh_vacancy_salaries(language)
            if hh_content:
                vacancies_salary_stats_hh[language] = hh_content

            sj_content = get_sj_vacancy_salaries(language, sj_secret_key)
            if sj_content:
                vacancies_salary_stats_sj[language] = sj_content
        except Exception as e:
            print(f"Exception while processing language {language}: {e}")

    # Output
    table_content_hh = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]
    for lang, content in vacancies_salary_stats_hh.items():
        table_content_hh.append((lang, content['vacancies_found'], content['vacancies_processed'], content['average_salary']))
    table_hh = AsciiTable(table_content_hh, "+HeadHunter Moscow------")
    print(table_hh.table)

    table_content_sj = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]
    for lang, content in vacancies_salary_stats_sj.items():
        table_content_sj.append((lang, content['vacancies_found'], content['vacancies_processed'], content['average_salary']))
    table_sj = AsciiTable(table_content_sj, "+SuperJob Moscow--------")
    print(table_sj.table)


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    main()
