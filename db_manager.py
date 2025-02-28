import psycopg2
from typing import List, Dict, Optional
from sql_queries import (
    get_companies_and_vacancies_count,
    get_all_vacancies,
    get_avg_salary,
    get_vacancies_with_higher_salary,
    get_vacancies_with_keyword
)

class DBManager:
    """
    Класс для работы с базой данных PostgreSQL, содержащей информацию о компаниях и вакансиях.
    """

    def __init__(self, db_name: str, params: Dict[str, str]):
        """
        Инициализирует экземпляр класса.
        db_namе: Имя базы данных.
        params: Параметры подключения к базе данных.
        """
        self.db_name: str = db_name
        self.params: Dict[str, str] = params

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = None
        try:
            conn = psycopg2.connect(dbname=self.db_name, **self.params)
            cur = conn.cursor()

            cur.execute(get_companies_and_vacancies_count())

            result: List[Dict] = []
            for row in cur:
                result.append({'employer_name': row[0], 'vacancies_count': row[1]})
            return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка компаний и количества вакансий: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_all_vacancies(self) -> List[Dict]:
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(dbname=self.db_name, **self.params)
            cur = conn.cursor()

            cur.execute(get_all_vacancies())

            result: List[Dict] = []
            for row in cur:
                result.append({
                    'employer_name': row[0],
                    'vacancy_name': row[1],
                    'salary_from': row[2],
                    'salary_to': row[3],
                    'currency': row[4],
                    'vacancy_url': row[5]
                })
            return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка всех вакансий: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_avg_salary(self) -> Optional[float]:
        """
        Получает среднюю зарплату по вакансиям.
        Рассчитывает среднее арифметическое по всем вакансиям, для которых указана зарплата (salary_from).
        """
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(dbname=self.db_name, **self.params)
            cur = conn.cursor()

            cur.execute(get_avg_salary())

            avg_salary: Optional[float] = cur.fetchone()[0]
            return float(avg_salary) if avg_salary is not None else None
        except psycopg2.Error as e:
            print(f"Ошибка при получении средней зарплаты: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(dbname=self.db_name, **self.params)
            cur = conn.cursor()

            cur.execute(get_vacancies_with_higher_salary())

            result: List[Dict] = []
            for row in cur:
                result.append({
                    'employer_name': row[0],
                    'vacancy_name': row[1],
                    'salary_from': row[2],
                    'salary_to': row[3],
                    'currency': row[4],
                    'vacancy_url': row[5]
                })
            return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка вакансий с зарплатой выше средней: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        conn = None
        cur = None
        try:
            conn = psycopg2.connect(dbname=self.db_name, **self.params)
            cur = conn.cursor()

            cur.execute(get_vacancies_with_keyword(), ('%' + keyword + '%',))

            result: List[Dict] = []
            for row in cur:
                result.append({
                    'employer_name': row[0],
                    'vacancy_name': row[1],
                    'salary_from': row[2],
                    'salary_to': row[3],
                    'currency': row[4],
                    'vacancy_url': row[5]
                })
            return result
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка вакансий с ключевым словом '{keyword}': {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()