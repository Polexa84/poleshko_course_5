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