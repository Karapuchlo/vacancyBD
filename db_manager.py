import psycopg2

class DBManager:
    def __init__(self, host, database, user, password):
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        self.cursor.execute("""
            SELECT c.company_name, COUNT(v.id) AS vacancies_count
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.company_name
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        self.cursor.execute("""
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        self.cursor.execute("""
            SELECT AVG(salary) AS avg_salary
            FROM vacancies
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.salary > %s
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        self.cursor.execute("""
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.title ILIKE %s
        """, (f'%{keyword}%',))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
