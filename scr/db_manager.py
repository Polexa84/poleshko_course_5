# Импортируем необходимые библиотеки и модули
import psycopg2
from typing import List, Dict, Optional

# Импортируем нужные методы
from scr.sql_queries import (
    get_companies_and_vacancies_count,
    get_all_vacancies,
    get_avg_salary,
    get_vacancies_with_higher_salary,
    get_vacancies_with_keyword
)

class DBManager:
    """Класс для работы с базой данных PostgreSQL, содержащей информацию о компаниях и вакансиях."""

    def __init__(self, db_name: str, params: Dict[str, str]):
        """
        Инициализирует экземпляр класса.
        db_namе: Имя базы данных.
        params: Параметры подключения к базе данных.
        """
        self.db_name: str = db_name
        self.params: Dict[str, str] = params
        self.conn: Optional= None # Инициализируем соединение
        self.cur: Optional = None # Инициализируем курсор

    def _connect(self):
        """Устанавливает соединение с базой данных и создает курсор."""
        try:
            self.conn = psycopg2.connect(dbname=self.db_name, **self.params)
            self.cur = self.conn.cursor()
        except psycopg2.Error as e:
            print(f"Ошибка при подключении к базе данных: {e}")
            raise

    def _close(self):
        """Закрывает соединение и курсор, если они были открыты."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    @staticmethod
    def _process_vacancy_rows(cursor) -> List[Dict]:
        """Преобразует строки из курсора в список словарей о вакансиях."""
        result: List[Dict] = []
        for row in cursor:
            result.append({
                'employer_name': row[0],
                'vacancy_name': row[1],
                'salary_from': row[2],
                'salary_to': row[3],
                'currency': row[4],
                'vacancy_url': row[5]
            })
        return result

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        try:
            self._connect()
            self.cur.execute(get_companies_and_vacancies_count())

            result: List[Dict] = []
            for row in self.cur:
                result.append({'employer_name': row[0], 'vacancies_count': row[1]})
            return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка компаний и количества вакансий: {e}")
            return []
        finally:
            self._close()

    def get_all_vacancies(self) -> List[Dict]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        try:
            self._connect()
            self.cur.execute(get_all_vacancies())
            return DBManager._process_vacancy_rows(self.cur)  # Pass the cursor directly
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка всех вакансий: {e}")
            return []
        finally:
            self._close()

    def get_avg_salary(self) -> Optional[float]:
        """Получает среднюю зарплату по вакансиям."""
        try:
            self._connect()
            self.cur.execute(get_avg_salary())

            avg_salary: Optional[float] = self.cur.fetchone()[0]
            return float(avg_salary) if avg_salary is not None else None
        except psycopg2.Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return None
        finally:
            self._close()

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        try:
            self._connect()
            self.cur.execute(get_vacancies_with_higher_salary())
            return DBManager._process_vacancy_rows(self.cur)  # Pass the cursor directly
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка вакансий с зарплатой выше средней: {e}")
            return []
        finally:
            self._close()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""
        try:
            self._connect()
            self.cur.execute(get_vacancies_with_keyword(), ('%' + keyword + '%',))
            return DBManager._process_vacancy_rows(self.cur)  # Pass the cursor directly
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка вакансий с ключевым словом '{keyword}': {e}")
            return []
        finally:
            self._close()