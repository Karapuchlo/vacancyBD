import os
from dotenv import load_dotenv
from src.db_manager import DBManager
from src.hhapi_client import HHAPIClient
from src.vacancy import Vacancy

# Загружаем переменные среды из .env файла
load_dotenv()
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
    # Представьте, что у вас есть список вакансий, как уже показано
    vacancies = [
        Vacancy('Компания A', 'Разработчик', '50000', 'http://example.com/a'),
        Vacancy('Компания B', 'Тестировщик', '40000', 'http://example.com/b'),
        Vacancy('Компания A', 'Системный администратор', '60000', 'http://example.com/a_sysadmin')
    ]

    # Группируем вакансии по компаниям
    companies_dict = {}
    for vacancy in vacancies:
        if vacancy.employer_name not in companies_dict:
            companies_dict[vacancy.employer_name] = []
        companies_dict[vacancy.employer_name].append({
            'name': vacancy.name,
            'salary': vacancy.salary,
            'alternate_url': vacancy.alternate_url
        })

    # Формируем список для передачи в метод insert_companies_and_vacancies
    companies_list = [{'name': name, 'vacancies': v} for name, v in companies_dict.items()]

    # Теперь передаем правильно сформированный список в ваш метод
    db_manager.insert_companies_and_vacancies(companies_list)

    # Не забудьте закрыть соединение
    db_manager.close()

    # Получение информации о компаниях и количестве вакансий
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    for company_name, vacancies_count in companies_and_vacancies_count:
        print(f"Компания: {company_name}, Вакансий: {vacancies_count}")

    db_manager.close()

if __name__ == "__main__":
    main()
