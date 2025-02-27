#                                        develop by Polexa

# Импортируем необходимые библиотеки и модули
import os
from dotenv import load_dotenv

# Импортируем нужные классы и методы
from api_function import HHApi
from create_db import DatabaseCreator

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

# Создаем экземпляр класса DatabaseCreator
db_creator = DatabaseCreator(DB_NAME, PARAMS)

# Создаем базу данных и таблицы
db_creator.create_database()
db_creator.create_tables()