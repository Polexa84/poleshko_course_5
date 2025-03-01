import pytest
import psycopg2
from dotenv import load_dotenv
import os

# Импортируем классы и функции из вашего основного скрипта
from scr.api_function import HHApi
from scr.create_db import DatabaseCreator
from scr.db_manager import DBManager

# Загружаем переменные окружения
load_dotenv()

# Параметры подключения к тестовой базе данных
TEST_DB_NAME = "test_hh_database"
PARAMS = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD')
}

@pytest.fixture(scope="module")
def db_creator():
    """Фикстура для создания тестовой базы данных."""
    db_creator = DatabaseCreator(TEST_DB_NAME, PARAMS)
    db_creator.create_database()
    db_creator.create_tables()
    yield db_creator

    # Закрываем все соединения и удаляем базу данных
    conn = psycopg2.connect(dbname="postgres", **PARAMS)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE {TEST_DB_NAME}")
    conn.close()

@pytest.fixture(scope="module")
def db_manager(db_creator):
    """Фикстура для создания экземпляра DBManager."""
    return DBManager(TEST_DB_NAME, PARAMS)

@pytest.fixture(scope="module")
def hh_api():
    """Фикстура для создания экземпляра HHApi."""
    return HHApi()

def test_database_creation(db_creator):
    """Тест создания базы данных и таблиц."""
    conn = psycopg2.connect(dbname=TEST_DB_NAME, **PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()
    assert len(tables) == 2, "Должны быть созданы две таблицы: employers и vacancies"
    conn.close()

def test_db_manager_methods(db_manager):
    """Тест основных методов DBManager."""
    # Проверка метода get_companies_and_vacancies_count
    companies = db_manager.get_companies_and_vacancies_count()
    assert isinstance(companies, list), "Метод get_companies_and_vacancies_count должен возвращать список"

    # Проверка метода get_all_vacancies
    vacancies = db_manager.get_all_vacancies()
    assert isinstance(vacancies, list), "Метод get_all_vacancies должен возвращать список"

    # Проверка метода get_avg_salary
    avg_salary = db_manager.get_avg_salary()
    assert isinstance(avg_salary, (int, float)) or avg_salary is None, "Метод get_avg_salary должен возвращать число или None"

    # Проверка метода get_vacancies_with_keyword
    keyword_vacancies = db_manager.get_vacancies_with_keyword("Python")
    assert isinstance(keyword_vacancies, list), "Метод get_vacancies_with_keyword должен возвращать список"