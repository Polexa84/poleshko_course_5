#                                        develop by Polexa

# Импортируем необходимые библиотеки и модули
import os
from dotenv import load_dotenv
import psycopg2

# Импортируем нужные классы и методы
from api_function import HHApi
from create_db import DatabaseCreator
from db_manager  import DBManager
from sql_queries import get_insert_vacancy_query

# Добавляем список работодателей с их ID
employer_ids = [
    80,      # Альфа-Банк
    1740,    # Яндекс
    2180,    # Ozon
    2748,    # Ростелеком
    3529,    # Сбер
    3776,    # МТС
    4233,    # X5 Group
    15478,   # VK (Mail.ru)
    39305,   # Газпром нефть
    78638,   # Тинькофф (Т-банк)
]

# Загружаем переменные окружения из .env файла
load_dotenv()

# Параметры подключения к базе данных (из .env)
DB_NAME = "hh_database"  # Имя базы данных

PARAMS = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD')  # Пароль из .env
}

# Проверка, что пароль установлен
if PARAMS['password'] is None:
    raise ValueError("Необходимо установить переменную окружения POSTGRES_PASSWORD в .env файле.")

# Создаем экземпляр класса DatabaseCreator для создания базы данных и таблиц
db_creator = DatabaseCreator(DB_NAME, PARAMS)
db_creator.create_database()
db_creator.create_tables()

# Создаем экземпляр класса HHApi для работы с API HH.ru
hh_api = HHApi()

def fill_employers_table(cur, employer_ids, hh_api):
    """Заполняет таблицу employers информацией о работодателях."""
    for employer_id in employer_ids:
        employer_name = hh_api.get_employer_name(employer_id)

        if not employer_name:
            continue

        cur.execute("SELECT employer_id FROM employers WHERE employer_id = %s", (employer_id,))
        if not cur.fetchone():
            cur.execute("INSERT INTO employers (employer_id, employer_name) VALUES (%s, %s)",
                        (employer_id, employer_name))
            print(f"Добавлена компания: {employer_name} (ID: {employer_id})")
        else:
            print(f"Компания {employer_name} (ID: {employer_id}) уже существует в базе данных.")


def fill_vacancies_table(cur, employer_ids, hh_api):
    """Заполняет таблицу vacancies."""
    insert_vacancy_query = get_insert_vacancy_query()

    for employer_id in employer_ids:
        vacancies = hh_api.get_employer_vacancies(employer_id)
        if vacancies:
            for vacancy in vacancies:
                vacancy_id = vacancy.get("id")
                cur.execute("SELECT vacancy_id FROM vacancies WHERE vacancy_id = %s", (vacancy_id,))
                if not cur.fetchone():
                    cur.execute(insert_vacancy_query, (
                        vacancy_id, employer_id, vacancy.get("name"),
                        vacancy.get("salary", {}).get("from"), vacancy.get("salary", {}).get("to"),
                        vacancy.get("salary", {}).get("currency"), vacancy.get("alternate_url"),
                        vacancy.get("snippet", {}).get("requirement")
                    ))
                    print(f"Добавлена вакансия: {vacancy.get('name')} от {hh_api.get_employer_name(employer_id)}")
                else:
                    print(f"Вакансия {vacancy.get('name')} уже существует в базе данных.")

# Подключаемся к базе данных и заполняем таблицы
try:
    with psycopg2.connect(dbname=DB_NAME, **PARAMS) as conn:
        with conn.cursor() as cur:
            fill_employers_table(cur, employer_ids, hh_api)
            fill_vacancies_table(cur, employer_ids, hh_api)
            conn.commit()  # Сохраняем изменения
except psycopg2.Error as e:
    print(f"Ошибка при работе с базой данных: {e}")
print("Заполнение базы данных завершено.")

# Создаем экземпляр класса DBManager
db_manager = DBManager(DB_NAME, PARAMS)

def print_vacancies(vacancies):
    """Выводит информацию о вакансиях."""
    if not vacancies:
        print("Нет данных о вакансиях.")
        return

    for vacancy in vacancies:
        employer_name = vacancy['employer_name']
        vacancy_name = vacancy['vacancy_name']
        salary_from = vacancy['salary_from']
        salary_to = vacancy['salary_to']
        currency = vacancy['currency']
        vacancy_url = vacancy['vacancy_url']

        if salary_from and salary_to:
            salary_info = f"Зарплата: от {salary_from} до {salary_to} {currency}"
        elif salary_from:
            salary_info = f"Зарплата: от {salary_from} {currency}"
        elif salary_to:
            salary_info = f"Зарплата: до {salary_to} {currency}"
        else:
            salary_info = "Зарплата не указана"

        print(f"Компания: {employer_name}\nВакансия: {vacancy_name}\n{salary_info}\nURL: {vacancy_url}\n")

def user_interaction():
    """Функция для взаимодействия с пользователем."""
    while True:
        print("\nВыберите действие:")
        print("1 - Получить список всех компаний и количество вакансий у каждой компании.")
        print("2 - Получить список всех вакансий.")
        print("3 - Получить среднюю зарплату по вакансиям.")
        print("4 - Получить список вакансий с зарплатой выше средней.")
        print("5 - Получить список вакансий по ключевому слову.")
        print("0 - Выйти")

        choice = input("Введите номер действия: ")

        if choice == '1':
            companies = db_manager.get_companies_and_vacancies_count()
            if companies:
                print("\nКомпании и количество вакансий:")
                for company in companies:
                    print(f"{company['employer_name']}: {company['vacancies_count']}")
            else:
                print("Не удалось получить данные.")
        elif choice == '2':
            vacancies = db_manager.get_all_vacancies()
            if vacancies:
                print("\nВсе вакансии:")
                print_vacancies(vacancies)  # Используем вынесенную функцию
            else:
                print("Не удалось получить данные.")
        elif choice == '3':
            avg_salary = db_manager.get_avg_salary()
            if avg_salary is not None:
                print(f"\nСредняя зарплата: {round(avg_salary)}")
            else:
                print("Не удалось получить данные.")
        elif choice == '4':
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if higher_salary_vacancies:
                print("\nВакансии с зарплатой выше средней:")
                print_vacancies(higher_salary_vacancies)  # Используем вынесенную функцию
            else:
                print("Не удалось получить данные.")
        elif choice == '5':
            keyword = input("Введите ключевое слово: ")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            if keyword_vacancies:
                print(f"\nВакансии, содержащие '{keyword}':")
                print_vacancies(keyword_vacancies)  # Используем вынесенную функцию
            else:
                print("Не удалось получить данные.")
        elif choice == '0':
            print("Выход.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите действие из списка.")

# Вызываем функцию взаимодействия с пользователем
if __name__ == '__main__':
    user_interaction()