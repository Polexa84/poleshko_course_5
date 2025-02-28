# api_function.py
import requests
import json
from typing import List, Dict

class HHApi:
    """Класс для взаимодействия с API HH.ru."""

    def __init__(self):
        """Инициализируем экземпляр класса. Устанавливает базовый URL API."""
        self.base_url = "https://api.hh.ru"  # Базовый URL API HH.ru

    def get_employer_vacancies(self, employer_id: int) -> List[Dict]:
        """ Получает список вакансий работодателя с HH.ru."""
        url = f"{self.base_url}/vacancies"  # URL для получения вакансий
        params = {"employer_id": employer_id, "per_page": 100}
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем статус код ответа (вызывает исключение при ошибке)
        return response.json().get("items", [])  # Возвращаем список вакансий из JSON-ответа

    def get_employer_name(self, employer_id: int) -> str | None:
        """Получает имя работодателя по его ID."""
        url = f"{self.base_url}/employers/{employer_id}"  # URL для получения информации о работодателе
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверяем статус код ответа (вызывает исключение при ошибке)
            employer_data = response.json()  # Преобразуем JSON-ответ в словарь
            return employer_data.get('name')  # Возвращаем имя работодателя из словаря
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Ошибка при получении данных о работодателе {employer_id}: {e}")
            return None  # Возвращаем None в случае ошибки