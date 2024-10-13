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

    def insert_companies_and_vacancies(self, companies_and_vacancies):
        for item in companies_and_vacancies:
            if isinstance(item, tuple) and len(item) == 2:
                company_name, vacancies = item
                self.cursor.execute("""
                    INSERT INTO companies (company_name)
                    VALUES (%s)
                    ON CONFLICT (company_name) DO NOTHING;
                """, (company_name,))

                company_id = self.cursor.execute("""
                    SELECT id FROM companies WHERE company_name = %s
                """, (company_name,)).fetchone()[0]

                # Проверка на то, что vacancies - это итерируемый объект
                if isinstance(vacancies, list):
                    for vacancy in vacancies:
                        self.cursor.execute("""
                            INSERT INTO vacancies (title, description, company_id)
                            VALUES (%s, %s, %s)
                        """, (vacancy.title, vacancy.description, company_id))
                else:
                    print(f"Ошибка: вакансии для компании {company_name} должны быть списком.")
            else:
                print(
                    "Ошибка: каждый элемент в companies_and_vacancies должен быть кортежем из (имя компании, список вакансий)")

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
