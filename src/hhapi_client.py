from typing import List, Tuple
import psycopg2
import requests

from src.vacancy import Vacancy
class HHAPIClient:
    """
    Клиент для работы с API hh.ru.

    Этот класс предоставляет интерфейс для взаимодействия с API hh.ru, позволяя получать вакансии.
    """

    def __init__(self, api_url: str, headers: dict):
        """
        Инициализирует экземпляр HHAPIClient.

        Args:
            api_url (str): URL API hh.ru.
            headers (dict): Заголовки HTTP-запроса.
        """
        self.api_url = api_url
        self.headers = headers

    def fetch_vacancies(self) -> List[Vacancy]:
        try:
            response = requests.get(self.api_url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            vacancies = data.get('items', [])
            return [Vacancy(
                employer_name=v['employer']['name'],
                name=v['name'],
                salary=v.get('salary', {}).get('from', 'Не указана'),
                alternate_url=v['alternate_url']
            ) for v in vacancies]
        except requests.exceptions.RequestException as e:
            print(f"Не удалось получить вакансии из API hh.ru: {e}")
            return None

class DBManager:
    """
    Класс для управления подключением и взаимодействием с базой данных.

    Этот класс предоставляет методы для подключения к базе данных, получения информации о
    компаниях и количестве вакансий, а также для закрытия соединения.
    """

    def __init__(self, host: str, database: str, user: str, password: str):
        """
        Инициализирует экземпляр DBManager.

        Args:
            host (str): Адрес хоста базы данных.
            database (str): Название базы данных.
            user (str): Имя пользователя базы данных.
            password (str): Пароль пользователя базы данных.
        """
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получение списка компаний и количества вакансий для каждой.

        Returns:
            List[Tuple[str, int]]: Список кортежей, где первый элемент - название компании, второй - количество вакансий.
        """
        try:
            self.cursor.execute("""
                SELECT employer_name, COUNT(*) as vacancies_count
                FROM vacancies
                GROUP BY employer_name
                ORDER BY vacancies_count DESC;
            """)
            result = self.cursor.fetchall()
            return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении информации о компаниях и вакансиях: {e}")
            return []

    def close(self) -> None:
        """
        Закрытие соединения с базой данных.
        """
        try:
            self.cursor.close()
            self.conn.commit()
            self.conn.close()
        except psycopg2.Error as e:
            print(f"Ошибка при закрытии соединения с базой данных: {e}")
