import psycopg2
from vacancy import Vacancy

class DBManager:
    def __init__(self, host, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()

        # Проверка наличия таблицы vacancies и создание, если ее нет
        self.cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'vacancies')")
        if not self.cursor.fetchone()[0]:
            self.cursor.execute("""
                CREATE TABLE vacancies (
                    id SERIAL PRIMARY KEY,
                    employer_name TEXT,
                    name TEXT,
                    salary NUMERIC,
                    alternate_url TEXT
                )
            """)
            self.connection.commit()

        # Проверка наличия столбцов в таблице vacancies
        self.cursor.execute("SELECT * FROM information_schema.columns WHERE table_name = 'vacancies'")
        existing_columns = [column[3] for column in self.cursor.fetchall()]

        if 'employer_name' not in existing_columns:
            self.cursor.execute("ALTER TABLE vacancies ADD COLUMN employer_name TEXT")
        if 'name' not in existing_columns:
            self.cursor.execute("ALTER TABLE vacancies ADD COLUMN name TEXT")
        if 'salary' not in existing_columns:
            self.cursor.execute("ALTER TABLE vacancies ADD COLUMN salary NUMERIC")
        if 'alternate_url' not in existing_columns:
            self.cursor.execute("ALTER TABLE vacancies ADD COLUMN alternate_url TEXT")

        self.connection.commit()



    def save_vacancies(self, vacancies):
        """Сохранение списка вакансий в базу данных"""
        values = [(v.employer_name, v.name, v.salary, v.alternate_url) for v in vacancies]
        self.cursor.executemany("""
            INSERT INTO vacancies (employer_name, name, salary, alternate_url)
            VALUES (%s, %s, %s, %s)
        """, values)
        self.connection.commit()

