# create_bd.py
def check_db_exists(db_name: str):
    """
    Возвращает SQL-запрос для проверки существования базы данных с заданным именем.
    """
    return f"SELECT 1 FROM pg_database WHERE datname='{db_name}'"

def create_db(db_name: str):
    """
    Возвращает SQL-запрос для создания базы данных с заданным именем.
    """
    return f"CREATE DATABASE {db_name}"

def create_employers_table():
    """
    Возвращает SQL-запрос для создания таблицы 'employers'.
    Таблица 'employers' содержит информацию о работодателях.
    """
    return """
        CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL
        );
    """

def create_vacancies_table():
    """
    Возвращает SQL-запрос для создания таблицы 'vacancies'.
    Таблица 'vacancies' содержит информацию о вакансиях.
    """
    return """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            vacancy_name VARCHAR(255) NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            currency VARCHAR(50),
            vacancy_url TEXT,
            description TEXT
        );
    """

# db_manager.py
def get_companies_and_vacancies_count():
    """
    Возвращает SQL-запрос для получения списка компаний и количества вакансий у каждой компании.
    """
    return """
        SELECT employer_name, COUNT(vacancy_id) AS vacancies_count
        FROM employers
        LEFT JOIN vacancies USING(employer_id)
        GROUP BY employer_name
        ORDER BY vacancies_count DESC
    """

def get_all_vacancies():
    """
    Возвращает SQL-запрос для получения списка всех вакансий.
    """
    return """
        SELECT employer_name, vacancy_name, salary_from, salary_to, currency, vacancy_url
        FROM vacancies
        JOIN employers USING(employer_id)
    """

def get_avg_salary():
    """
    Возвращает SQL-запрос для получения средней зарплаты по вакансиям.
    """
    return """
        SELECT AVG(salary_from)
        FROM vacancies
        WHERE salary_from IS NOT NULL
    """

def get_vacancies_with_higher_salary():
    """
    Возвращает SQL-запрос для получения списка вакансий с зарплатой выше средней.
    """
    return """
        SELECT employer_name, vacancy_name, salary_from, salary_to, currency, vacancy_url
        FROM vacancies
        JOIN employers USING(employer_id)
        WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL)
    """

def get_vacancies_with_keyword():
    """
    Возвращает SQL-запрос для получения списка вакансий, содержащих ключевое слово.
    Используем ILIKE для регистронезависимого поиска
    """
    return """
        SELECT employer_name, vacancy_name, salary_from, salary_to, currency, vacancy_url
        FROM vacancies
        JOIN employers USING(employer_id)
        WHERE vacancy_name ILIKE %s 
    """