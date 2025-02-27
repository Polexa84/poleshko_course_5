# Импортируем необходимые библиотеки и модули
import psycopg2
from typing import Dict

class DatabaseCreator:
    """
    Класс для создания базы данных и таблиц в PostgreSQL.
    """

    def __init__(self, db_name: str, params: Dict[str, str]):
        """
        Инициализирует экземпляр класса.
        db_name: Имя базы данных.
        params: Параметры подключения к базе данных (без имени БД).
        """
        self.db_name = db_name
        # Создаем копию параметров, чтобы не изменять исходные
        self.params: Dict[str, str] = params.copy()

    def create_database(self) -> None:
        """Создает базу данных, если она не существует."""
        conn = None
        try:
            # Подключаемся к базе данных postgres для создания новой
            conn = psycopg2.connect(database='postgres', **self.params)
            conn.autocommit = True  # Включаем автокоммит для выполнения команд DDL
            cur = conn.cursor()

            # Проверяем, существует ли база данных
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname='{self.db_name}'")
            exists = cur.fetchone()
            if not exists:
                # Создаем базу данных
                cur.execute(f"CREATE DATABASE {self.db_name}")
                print(f"База данных '{self.db_name}' успешно создана.")
            else:
                print(f"База данных '{self.db_name}' уже существует.")

        except psycopg2.Error as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()

    def create_tables(self) -> None:
        """Создает таблицы employers и vacancies."""
        conn = None
        try:
            # Подключаемся к созданной базе данных
            conn = psycopg2.connect(dbname=self.db_name, **self.params)  # используем dbname
            cur = conn.cursor()

            # SQL-запрос для создания таблицы employers
            cur.execute("""
                CREATE TABLE employers (
                    employer_id SERIAL PRIMARY KEY,
                    employer_name VARCHAR(255) NOT NULL
                );
            """)

            # SQL-запрос для создания таблицы vacancies
            cur.execute("""
                CREATE TABLE vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(employer_id),
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(50),
                    vacancy_url TEXT,
                    description TEXT
                );
            """)

            conn.commit()
            print("Таблицы 'employers' и 'vacancies' успешно созданы.")

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            if conn:
                cur.close()
                conn.close()