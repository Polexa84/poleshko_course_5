# Импортируем необходимые библиотеки и модули
import requests
import json
from typing import Optional, List, Dict

class HHApi:
    """Класс для взаимодействия с API HH.ru."""

    def __init__(self):
        """ Инициализируем экземпляр класса. Устанавливает базовый URL API."""
        self.base_url = "https://api.hh.ru"

    @staticmethod
    def _make_request(url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Выполняет запрос к API и обрабатывает ошибки."""
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Ошибка при запросе к API: {e}")
            return None

    def get_employer_vacancies(self, employer_id: int) -> List[Dict]:
        """Получает список вакансий работодателя с HH.ru."""
        url = f"{self.base_url}/vacancies"
        params = {"employer_id": employer_id, "per_page": 100}  # Fetch up to 100 vacancies per page
        data = self._make_request(url, params=params)
        return data.get("items", []) if data else []

    def get_employer_name(self, employer_id: int) -> str | None:
        """get_employer_name"""
        url = f"{self.base_url}/employers/{employer_id}"
        data = self._make_request(url)
        return data.get('name') if data else None