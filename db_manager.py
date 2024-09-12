import psycopg2
from vacancy import Vacancy

class DBManager:
    """Менеджер для работы с базой данных PostgreSQL"""
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()

    def save_vacancies(self, vacancies):
        """Сохранение списка вакансий в базу данных"""
        for vacancy in vacancies:
            self.cursor.execute("""
                INSERT INTO vacancies (employer_name, name, salary, alternate_url)
                VALUES (%s, %s, %s, %s)
            """, (vacancy.employer_name, vacancy.name, vacancy.salary, vacancy.alternate_url))
        self.connection.commit()
