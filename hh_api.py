import requests


def predict_rub_salary(vacancy):
    url = "https://api.hh.ru/vacancies?text={}&area=1".format(vacancy)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        vacancies = data['items']

        expected_salaries = []
        for vacancy in vacancies:
            salary = vacancy['salary']
            if salary and salary['currency'] == 'RUR' and salary['gross'] is False:
                if salary['from'] and salary['to']:
                    expected_salaries.append((salary['from'] + salary['to']) / 2)
                elif salary['from']:
                    expected_salaries.append(salary['from'] * 1.2)
                elif salary['to']:
                    expected_salaries.append(salary['to'] * 0.8)

        return expected_salaries
    else:
        print("Ошибка выполнения запроса:", response.status_code)


expected_salaries = predict_rub_salary('Python')

print("Ожидаемые зарплаты:", len(expected_salaries))
print(expected_salaries[:20])


