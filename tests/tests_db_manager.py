import pytest
import psycopg2
import os
from dotenv import load_dotenv
from scr.db_manager import DBManager
from scr.sql_queries import create_employers_table, create_vacancies_table

load_dotenv()

# Параметры для тестовой базы данных (замените на свои)
TEST_DB_NAME = 'test_db_manager_test_db'
TEST_DB_PARAMS = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD')  # Пароль из .env
}

# Sample data for testing
SAMPLE_EMPLOYERS = [
    ("Employer A",),
]

SAMPLE_VACANCIES = [
    (1, "Vacancy 1 for A", 1000, 2000, "USD", "http://example.com/a1"),
]

@pytest.fixture(scope="module")
def db_manager():
    """Фикстура для создания экземпляра DBManager."""
    test_params = TEST_DB_PARAMS.copy()
    test_params['dbname'] = TEST_DB_NAME
    manager = DBManager(TEST_DB_NAME, test_params)
    return manager

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_db(db_manager):
    """Фикстура для создания и удаления тестовой базы данных и таблиц."""
    conn = None
    try:
        # Connect to postgres to drop/create database
        test_params_no_db = TEST_DB_PARAMS.copy()
        test_params_no_db['dbname'] = 'postgres'
        conn = psycopg2.connect(**test_params_no_db)
        conn.autocommit = True
        cur = conn.cursor()

        # Drop test database if it exists
        cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")

        # Create test database
        cur.execute(f"CREATE DATABASE {TEST_DB_NAME}")
        cur.close()
        conn.close()

        # Connect to the new database
        test_params = TEST_DB_PARAMS.copy()
        test_params['dbname'] = TEST_DB_NAME
        conn = psycopg2.connect(**test_params)
        conn.autocommit = True
        cur = conn.cursor()

        # Create employers and vacancies tables
        cur.execute(create_employers_table())
        cur.execute(create_vacancies_table())

        # Insert sample data
        for employer in SAMPLE_EMPLOYERS:
            cur.execute("INSERT INTO employers (employer_name) VALUES (%s)", employer)
        for vacancy in SAMPLE_VACANCIES:
            cur.execute("INSERT INTO vacancies (employer_id, vacancy_name, salary_from, salary_to, currency, vacancy_url) VALUES (%s, %s, %s, %s, %s, %s)", vacancy)

        conn.commit()
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        pytest.fail(f"Error setting up test database: {e}")

    yield

    try:
        # Connect to postgres to drop the database
        test_params_no_db = TEST_DB_PARAMS.copy()
        test_params_no_db['dbname'] = 'postgres'
        conn = psycopg2.connect(**test_params_no_db)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE {TEST_DB_NAME}")
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        pytest.fail(f"Error tearing down test database: {e}")

def test_get_companies_and_vacancies_count(db_manager):
    """Проверяет, что метод get_companies_and_vacancies_count возвращает правильные результаты."""
    result = db_manager.get_companies_and_vacancies_count()
    assert isinstance(result, list)
    assert len(result) == 1  # One company