import psycopg2
from typing import List, Tuple

from src.vacancy import Vacancy


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

    def create_database_structure(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                company_name TEXT NOT NULL
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                company_id INTEGER NOT NULL,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            );
        """)
        self.conn.commit()

    def add_vacancy_to_database(self, vacancy):
        def add_vacancy_to_database(self, vacancy):
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO vacancies (company, title, salary, url)
                VALUES (?, ?, ?, ?)''', (vacancy['company'], vacancy['title'], vacancy['salary'], vacancy['url']))
        self.conn.commit()

    def insert_companies_and_vacancies(self, companies_and_vacancies):
        from src.vacancy import Vacancy  # Импортируем здесь, чтобы избежать циклического импорта
        company: object
        for company in companies_and_vacancies:
            if 'name' not in company or 'vacancies' not in company:
                print(f"Ошибка: неверный формат данных для компании: {company}. Ожидались поля 'name' и 'vacancies'.")
                continue

            employer_name = company['name']
            vacancies = company['vacancies']

            if not isinstance(vacancies, list):
                print(f"Ожидался список вакансий для компании {employer_name}, но получено: {vacancies}.")
                continue

            for vacancy in vacancies:
                self.add_vacancy_to_database(vacancy)

            print(f"Вакансии для компании '{employer_name}' успешно добавлены.")

        self.conn.commit()

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
