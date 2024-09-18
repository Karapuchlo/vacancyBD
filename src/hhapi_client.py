import requests
from src.vacancy import Vacancy

class HHAPIClient:
    """Клиент для работы с API hh.ru"""
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.headers = headers

    def fetch_vacancies(self):
        """Получение вакансий для указанной компании"""
        vacancies = []
        for i in range(10):
            params = {
                'text': 'Python разработчик',
                'area': 113,  # 113 - Россия
                'page': i,
                'per_page': 100  # количество возвращаемых вакансий на странице
            }

            response = requests.get(self.api_url, headers=self.headers, params=params)
            data = response.content.decode()
            response.close()

            for vacancy_data in response.json()['items']:
                if vacancy_data['salary'] is not None:
                    vacancy = Vacancy(
                        vacancy_data["name"],
                        vacancy_data["employer"]["name"],
                        vacancy_data['salary'],
                        vacancy_data["alternate_url"]
                    )
                    vacancies.append(vacancy)

        return vacancies
