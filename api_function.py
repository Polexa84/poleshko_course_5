# Импортируем необходимые библиотеки
import requests
import json
from typing import Optional, List, Dict

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

class HHApi:

    """
    Класс для взаимодействия с API HH.ru.
    """

    def __init__(self):

        """
        Инициализируем экземпляр класса.
        Устанавливает базовый URL API.
        """

        self.base_url = "https://api.hh.ru"

    def get_employer_info(self, employer_id: int) -> Optional[Dict]:

        """
        Получает информацию о работодателе по ID в формате JSON, если запрос успешен.
        Возвращает None в случае ошибки при выполнении запроса или разборе JSON.
        """

        try:
            url = f"{self.base_url}/employers/{employer_id}"  # формируем URL для запроса к API hh.ru
            with requests.get(url) as req:  # выполняем запрос к API
                req.raise_for_status()  # генерируем исключение, если статус код ответа не 200 (успешный)
                employer_data = req.json()  # преобразуем JSON-ответ в словарь Python
                return employer_data # возвращаем словарь с данными о работодателе

        # обрабатываем ошибки связанные с HTTP-запросами и связанные с разбором JSON (возвращаем None в случае ошибки)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении информации о работодателе {employer_id}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка при разборе JSON для работодателя {employer_id}: {e}")
            return None
# Создаем экземпляр класса HHApi
hh_api = HHApi()

# Вызываем метод get_employer_info на экземпляре класса
empl = hh_api.get_employer_info(employer_ids[1])

# Выводим результат
print(empl)