from dotenv import load_dotenv
import os
from src.hhapi_client import HHAPIClient
from src.db_manager import DBManager


# Загрузка переменных окружения из .env файла
load_dotenv()
def main():
    # Настройка подключения к API hh.ru
    api_url = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'HH-User-Agent',
        'accept': 'application/json, text/plain, */*'
    }
    hh_api_client = HHAPIClient(api_url, headers)

    # Настройка подключения к базе данных
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    db_manager = DBManager(db_host, db_name, db_user, db_password)

    # Получение вакансий

    vacancies = hh_api_client.fetch_vacancies()

    # Сохранение вакансий в базе данных
    for vacancy in vacancies:
        # Сохранение данных в базу
        pass

    # Получение дополнительной информации
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    # Обработка и вывод результатов

    db_manager.close()


if __name__ == '__main__':
    main()
