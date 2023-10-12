
import requests
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def predict_rub_salary_sj(vacancy):
    headers = {
        'X-Api-App-Id': os.environ.get('SUPERJOB_SECRET_KEY')
    }
    url = "https://api.superjob.ru/2.0/vacancies/"
    params = {
        'catalogues': 48,
        'town': 4,
        'keyword': vacancy
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        salaries = []

        for vacancy in data['objects']:
            if vacancy['payment_from'] and vacancy['payment_to']:
                salary = (vacancy['payment_from'] + vacancy['payment_to']) / 2
                salaries.append(salary)

        if salaries:
            average_salary = sum(salaries) / len(salaries)
            return average_salary
        else:
            return None
    else:
        print("Ошибка при выполнении запроса:", response.status_code)
        return None


vacancy = "Python Developer"
average_salary = predict_rub_salary_sj(vacancy)
print("Средняя зарплата для вакансии", vacancy, ":", average_salary)