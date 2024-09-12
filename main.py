from hhapi_client import HHAPIClient
from db_manager import DBManager

def main():
    # Настройка подключения к API hh.ru
    api_url = 'https://api.hh.ru/vacancies'
    headers = {
        'User-Agent': 'HH-User-Agent',
        'accept': 'application/json, text/plain, */*'
    }
    hh_api_client = HHAPIClient(api_url, headers)

    # Настройка подключения к БД PostgreSQL
    db_host = 'localhost'
    db_name = 'vacancies'
    db_user = "postgres"
    db_password = "240615Nastya"
    db_manager = DBManager(db_host, db_name, db_user, db_password)

    # Получение данных о вакансиях и сохранение в БД
    vacancies = hh_api_client.fetch_vacancies()
    db_manager.save_vacancies(vacancies)

if __name__ == '__main__':
    main()
