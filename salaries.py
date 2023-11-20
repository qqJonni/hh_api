import requests
import os
from dotenv import load_dotenv, find_dotenv
from statistics import mean

from requests import HTTPError
from terminaltables import AsciiTable

AREA_MOSCOW_HH = 1
CATALOGUE_PROGRAMMING_SJ = 48
TOWN_MOSCOW_SJ = 4
PERIOD = 1


def generate_salary_table(stats, title):
    table_content = [('Язык программирования', 'Найдено вакансий', 'Обработано вакансий', 'Средняя зарплата')]

    for lang, content in stats.items():
        table_content.append(
            (lang, content['vacancies_found'], content['vacancies_processed'], content['average_salary']))

    table = AsciiTable(table_content, title)
    return table.table


def extract_salary(salary_info):
    from_salary = salary_info.get('from')
    to_salary = salary_info.get('to')

    if from_salary is not None and to_salary is not None:
        return (from_salary + to_salary) / 2
    if from_salary is not None:
        return from_salary * 1.2
    if to_salary is not None:
        return to_salary * 0.8

    return None


def get_hh_vacancy_statistic(language):
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
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка при выполнении запроса (HH) для {language}: {e}")
            break

        response_hh = response.json()
        vacancies_found = response_hh['found']
        vacancies = response_hh['items']
        for vacancy in vacancies:
            salary = vacancy.get('salary')
            salaries.extend(extract_salary(salary))
        page += 1
        if not response_hh['pages'] or page >= response_hh['pages']:
            break

    average_salary = int(mean(salaries)) if salaries else 0
    return {
        "vacancies_found": vacancies_found,
        "vacancies_processed": len(salaries),
        "average_salary": average_salary
    }


def get_sj_vacancy_statistic(language, sj_secret_key):
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
            'period': PERIOD
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
            payment_from = vacancy.get('payment_from')
            payment_to = vacancy.get('payment_to')
            salaries_sj.extend(extract_salary({'from': payment_from, 'to': payment_to}))

        page += 1
        if not content_sj.get('more') or not content_sj.get('objects'):
            break

    average_salary_sj = int(mean(salaries_sj)) if salaries_sj else 0
    return {
        "vacancies_found": vacancies_found_sj,
        "vacancies_processed": len(salaries_sj),
        "average_salary": average_salary_sj
    }


def start():
    load_dotenv(find_dotenv())
    languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
    vacancies_salary_stats_hh = {}
    vacancies_salary_stats_sj = {}
    sj_secret_key = os.environ.get('SUPERJOB_SECRET_KEY')

    for language in languages:
        try:
            hh_statistic = get_hh_vacancy_statistic(language)
            vacancies_salary_stats_hh[language] = hh_statistic

            sj_statistic = get_sj_vacancy_statistic(language, sj_secret_key)
            vacancies_salary_stats_sj[language] = sj_statistic
        except HTTPError as e:
            print(f"Exception while processing language {language}: {e}")

    # Output
    table_hh = generate_salary_table(vacancies_salary_stats_hh, "+HeadHunter Moscow------")
    print(table_hh)

    table_sj = generate_salary_table(vacancies_salary_stats_sj, "+SuperJob Moscow--------")
    print(table_sj)


if __name__ == "__main__":
    start()
