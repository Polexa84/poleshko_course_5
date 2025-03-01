# Импортируем необходимые библиотеки и модули
import pytest
import psycopg2
import os
from dotenv import load_dotenv

# Импортируем нужные классы и методы
from scr.create_db import DatabaseCreator



# Загружаем переменные окружения из .env файла
load_dotenv()

TEST_DB_NAME = 'test_db_creator_test_db'  # Уникальное имя для тестовой БД
TEST_DB_PARAMS = {
    'host': '127.0.0.1',
    'port': '5432',
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD')  # Пароль из .env
}

@pytest.fixture(scope="module")
def db_creator():
    """Фикстура, создающая экземпляр DatabaseCreator."""
    creator = DatabaseCreator(TEST_DB_NAME, TEST_DB_PARAMS)
    return creator

@pytest.fixture(scope="module", autouse=True)
def setup_teardown_db(db_creator):
    """Фикстура для создания и удаления тестовой базы данных."""
    try:
        # Подключение к postgres для создания/удаления БД
        conn = psycopg2.connect(dbname='postgres', **TEST_DB_PARAMS)
        conn.autocommit = True
        cur = conn.cursor()

        # Удаляем БД, если она существует
        cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        cur.close()
        conn.close()

        # Создаем БД
        db_creator.create_database()
        db_creator.create_tables() # Create tables

    except psycopg2.Error as e:
        pytest.fail(f"Ошибка при настройке тестовой базы данных: {e}")

    yield

    try:
        # Удаляем БД после тестов
        conn = psycopg2.connect(dbname='postgres', **TEST_DB_PARAMS)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"DROP DATABASE {TEST_DB_NAME}")
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        pytest.fail(f"Ошибка при удалении тестовой базы данных: {e}")

def test_create_database_success(db_creator):
    """Проверяет, что база данных успешно создается."""
    try:
        # Пытаемся подключиться к созданной базе данных
        test_params = TEST_DB_PARAMS.copy()
        test_params['dbname'] = TEST_DB_NAME
        conn = psycopg2.connect(**test_params)
        conn.close()
        assert True # Успешное подключение означает, что тест пройден
    except psycopg2.Error as e:
        pytest.fail(f"Не удалось подключиться к базе данных после создания: {e}")

def test_create_tables_success(db_creator):
    """Проверяет, что таблицы успешно создаются."""
    try:
        # Подключаемся к тестовой базе данных
        test_params = TEST_DB_PARAMS.copy()
        test_params['dbname'] = TEST_DB_NAME
        conn = psycopg2.connect(**test_params)
        cur = conn.cursor()

        # Проверяем, существуют ли таблицы (простой запрос)
        cur.execute("SELECT * FROM employers LIMIT 0") # Check employers table
        cur.execute("SELECT * FROM vacancies LIMIT 0")  # Check vacancies table
        cur.close()
        conn.close()
        assert True #Если дошли до сюда, таблицы есть
    except psycopg2.Error as e:
        pytest.fail(f"Ошибка при проверке создания таблиц: {e}")