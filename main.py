import psycopg2

from src.hhapi_client import HHAPIClient
from src.db_manager import DBManager

def main():
    # Настройка подключения к API hh.ru
    api_url = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'HH-User-Agent',
        'accept': 'application/json, text/plain, */*'
    }
    hh_api_client = HHAPIClient(api_url, headers)

    conn = psycopg2.connect(
        host="localhost",
        database="vacancies",
        user="postgres",
        password="240615Nastya"
    )
    cursor = conn.cursor()
    cursor.execute("""
            CREATE TABLE companies (
                id SERIAL PRIMARY KEY,
                company_name TEXT NOT NULL
            )
        """)
    cursor.execute("""
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                company_id INT NOT NULL,
                title TEXT NOT NULL,
                salary FLOAT,
                url TEXT NOT NULL,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        """)
    conn.commit()
    cursor.close()
    conn.close()

    # Настройка подключения к БД PostgreSQL
    db_host = 'localhost'
    db_name = 'vacancies'
    db_user = "postgres"
    db_password = "240615Nastya"
    db_manager = DBManager(db_host, db_name, db_user, db_password)


    # Получить список компаний и количество вакансий у каждой
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, vacancies_count in companies_and_vacancies:
        print(f"{company} has {vacancies_count} vacancies")

    # Получить список всех вакансий
    all_vacancies = db_manager.get_all_vacancies()
    for company_name, title, salary, url in all_vacancies:
        print(f"{company_name} - {title} (Salary: {salary}, URL: {url})")

    # Получить среднюю зарплату по всем вакансиям
    avg_salary = db_manager.get_avg_salary()
    print(f"Average salary: {avg_salary}")

    # Получить список вакансий с зарплатой выше средней
    high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
    for company_name, title, salary, url in high_salary_vacancies:
        print(f"{company_name} - {title} (Salary: {salary}, URL: {url})")

    # Получить список вакансий, содержащих слово "python"
    python_vacancies = db_manager.get_vacancies_with_keyword("python")
    for company_name, title, salary, url in python_vacancies:
        print(f"{company_name} - {title} (Salary: {salary}, URL: {url})")

    db_manager.close()

if __name__ == '__main__':
    main()
