#                                        develop by Polexa

# Импортируем необходимые библиотеки и модули
import psycopg2
import os
from dotenv import load_dotenv

# Импортируем нужные классы и методы
from api_hh import HHApi

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

DB_NAME = "hh_database"  # Имя базы данных

# Параметры подключения к базе данных (из .env)
PARAMS = {
    'host': '127.0.0.1',
    'port': '5432',
    'database': DB_NAME,
    'user': 'postgres',
    'password': os.getenv('POSTGRES_PASSWORD')  # Пароль из .env
}

# Проверка, что пароль установлен
if PARAMS['password'] is None:
    raise ValueError("Необходимо установить переменную окружения POSTGRES_PASSWORD в .env файле.")