import os

from src.db_manager import DBManager
from src.hhapi_client import HHAPIClient


def main():
    # Настройка подключения к API hh.ru
    api_url = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'HH-User-Agent',
        'accept': 'application/json, text/plain, */*'
    }
    hh_api_client = HHAPIClient(api_url, headers)

    # Получение вакансий
    vacancies = hh_api_client.fetch_vacancies()
    if vacancies is None:
        print("Не удалось получить вакансии из API hh.ru")
        return

    # Сохранение вакансий в базе данных
    db_manager = DBManager(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    db_manager.create_database_structure()
    db_manager.insert_companies_and_vacancies(vacancies)

    # Получение информации о компаниях и количестве вакансий
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    for company_name, vacancies_count in companies_and_vacancies_count:
        print(f"Компания: {company_name}, Вакансий: {vacancies_count}")

    db_manager.close()

if __name__ == "__main__":
    main()
