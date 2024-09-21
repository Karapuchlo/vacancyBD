import psycopg2
from typing import List, Tuple


class DBManager:
    def __init__(self, host: str, database: str, user: str, password: str):
        """
        Класс для управления подключением и взаимодействием с базой данных.

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
        self.cursor.execute("""
            SELECT c.company_name, COUNT(v.id) AS vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.company_name
        """)
        return self.cursor.fetchall()

    # Аналогичным образом добавьте документацию для других методов

    def close(self) -> None:
        """
        Закрытие соединения с базой данных.
        """
        self.cursor.close()
        self.conn.close()
