# Импортируем необходимые библиотеки и модули
import requests
import json
from typing import List, Dict, Optional

class HHApi:
    """Класс для взаимодействия с API HH.ru."""

    def __init__(self):
        """Инициализируем экземпляр класса. Устанавливает базовый URL API."""
        self.base_url = "https://api.hh.ru"
        self.max_vacancies = 10  # Максимальное количество вакансий

    def get_employer_vacancies(self, employer_id: int) -> List[Dict]:
        """Получает список вакансий работодателя с HH.ru с учетом пагинации."""
        url = f"{self.base_url}/vacancies"
        vacancies = []
        page = 0
        per_page = 100
        total_vacancies = 0  # Счетчик полученных вакансий

        try:
            while total_vacancies < self.max_vacancies:
                params = {"employer_id": employer_id, "per_page": per_page, "page": page}
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                items = data.get("items", [])

                if not items:
                    break  # Если нет вакансий на текущей странице
                vacancies.extend(items[:self.max_vacancies - total_vacancies]) # Добавляем вакансии с учетом лимита
                total_vacancies += len(items)

                if len(items) < per_page:
                    break  # Если на странице меньше, чем per_page, значит, это последняя страница
                page += 1

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении вакансий для работодателя {employer_id}: {e}")
        except json.JSONDecodeError as e:
            print(f"Ошибка при разборе JSON: {e}")

        return vacancies

    def get_employer_name(self, employer_id: int) -> Optional[str]:
        """Получает имя работодателя по его ID."""
        url = f"{self.base_url}/employers/{employer_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            employer_data = response.json()
            return employer_data.get('name')
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Ошибка при получении данных о работодателе {employer_id}: {e}")
            return None