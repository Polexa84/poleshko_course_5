# Импортируем необходимые библиотеки и модули
import psycopg2
from typing import Dict, Optional
from sql_queries import check_db_exists, create_db, create_employers_table, create_vacancies_table

class DatabaseCreator:
    """
    Класс для создания базы данных и таблиц в PostgreSQL.
    """
    def __init__(self, db_name: str, params: Dict[str, str]):
        """
        Инициализирует экземпляр класса.
        """
        self.db_name = db_name
        # Создаем копию параметров, чтобы не изменять исходные
        self.params: Dict[str, str] = params.copy()
        self.conn: Optional[psycopg2.connection] = None  # Выносим conn в __init__

    def create_database(self) -> None:
        """Создает базу данных, если она не существует."""
        try:
            # Подключаемся к базе данных postgres для создания новой
            self.conn = psycopg2.connect(database='postgres', **self.params)
            self.conn.autocommit = True  # Включаем автокоммит для выполнения команд DDL
            cur = self.conn.cursor()

            # Проверяем, существует ли база данных
            cur.execute(check_db_exists(self.db_name))
            exists = cur.fetchone()
            if not exists:
                # Создаем базу данных
                cur.execute(create_db(self.db_name))
                print(f"База данных '{self.db_name}' успешно создана.")
            else:
                print(f"База данных '{self.db_name}' уже существует.")

        except psycopg2.Error as e:
            print(f"Ошибка при создании базы данных: {e}")
        finally:
            if self.conn:
                cur.close()
                self.conn.close()

    def create_tables(self) -> None:
        """Создает таблицы employers и vacancies."""
        try:
            # Подключаемся к созданной базе данных
            self.conn = psycopg2.connect(dbname=self.db_name, **self.params)  # используем dbname
            cur = self.conn.cursor()

            # SQL-запрос для создания таблицы employers
            cur.execute(create_employers_table())

            # SQL-запрос для создания таблицы vacancies
            cur.execute(create_vacancies_table())

            self.conn.commit()
            print("Таблицы 'employers' и 'vacancies' успешно созданы или уже существуют.")

        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            if self.conn:
                cur.close()
                self.conn.close()