import requests

AREA_MOSCOW_HH = 1
CATALOGUE_PROGRAMMING_SJ = 48
TOWN_MOSCOW_SJ = 4
page = 0

base_url = "https://api.superjob.ru/2.0/vacancies/"

while True:
    params = {
            'catalogues': CATALOGUE_PROGRAMMING_SJ,
            'town': TOWN_MOSCOW_SJ,
            'keyword': f"программист Python",
            'page': page
        }
    headers = {
            'X-Api-App-Id': 'v3.r.137884422.961cdbd81148582db9e6207fbebad278bac71cbe.ba2d6532707e51d059e79d37e3d4bae9b1f60467'
        }
    response_sj = requests.get(base_url, headers=headers, params=params)
    response_sj.raise_for_status()
    content_sj = response_sj.json()
    vacancies_found = content_sj.get('found', 0)
    print(vacancies_found)