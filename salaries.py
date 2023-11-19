import requests
import os
from dotenv import load_dotenv, find_dotenv
from statistics import mean

from requests import HTTPError
from terminaltables import AsciiTable

AREA_MOSCOW_HH = 1
CATALOGUE_PROGRAMMING_SJ = 48
TOWN_MOSCOW_SJ = 4


def extract_salaries(salary_info, from_key, to_key):
    extracted_salaries = []

    if salary_info and salary_info.get(from_key) and salary_info.get(to_key):
        extracted_salaries.append((salary_info[from_key] + salary_info[to_key]) / 2)
    if salary_info and salary_info.get(from_key):
        extracted_salaries.append(salary_info[from_key] * 1.2)
    if salary_info and salary_info.get(to_key):
        extracted_salaries.append(salary_info[to_key] * 0.8)

    return extracted_salaries


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
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"Ошибка при выполнении запроса (HH) для {language}: {e}")
            break

        json_response = response.json()
        vacancies_found = json_response['found']
        vacancies = json_response['items']
        for vacancy in vacancies:
            salary = vacancy.get('salary')
            salaries.extend(extract_salaries(salary, 'from', 'to'))
        page += 1
        if not json_response['pages'] or page >= json_response['pages']:
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
            payment_from = vacancy.get('payment_from')
            payment_to = vacancy.get('payment_to')
            salaries_sj.extend(extract_salaries({'from': payment_from, 'to': payment_to}, 'from', 'to'))

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
    languages = ["Python", "Java", "Javascript", "Go", "PHP", "C++", "TypeScript", "C#", "Shell"]
    vacancies_salary_stats_hh = {}
    vacancies_salary_stats_sj = {}
    sj_secret_key = os.environ.get('SUPERJOB_SECRET_KEY')

    for language in languages:
        try:
            hh_salaries = get_hh_vacancy_salaries(language)
            vacancies_salary_stats_hh[language] = hh_salaries

            sj_salaries = get_sj_vacancy_salaries(language, sj_secret_key)
            vacancies_salary_stats_sj[language] = sj_salaries
        except HTTPError as e:
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
    start()
