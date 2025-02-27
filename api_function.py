# Импортируем необходимые библиотеки
import requests
import json
from typing import Optional, List, Dict

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

    def get_employer_vacancies(self, employer_id: int, limit: int = 100, page: int = 0) -> Optional[List[Dict]]:

        """
        Получает список вакансий работодателя по ID.
        """
        vacancies: List[Dict] = []  # инициализируем пустой список для хранения вакансий
        try:
            url = f"{self.base_url}/vacancies"  # формируем базовый URL для запроса вакансий
            params = {  # формируем словарь с параметрами запроса
                "employer_id": employer_id,  # ID работодателя
                "per_page": limit,  # количество вакансий на странице
                "page": page  # номер страницы
            }
            with requests.get(url, params=params) as req:  # выполняем запрос с параметрами
                req.raise_for_status()  # генерируем исключение, если статус код ответа не 200(успешно)
                data = req.json()  # преобразуем JSON-ответ в словарь
                vacancies.extend(data['items'])  # добавляем вакансии из текущей страницы в список

                total_pages = data['pages']  # получаем общее количество страниц с вакансиями
                current_page = data['page']  # получаем номер текущей страницы

                while current_page < total_pages - 1:  # цикл для перебора всех страниц
                    params['page'] += 1  # увеличиваем номер страницы
                    current_page += 1  # обновляем текущий номер страницы

                    with requests.get(url, params=params) as req_next:  # выполняем запрос для следующей страницы
                        req_next.raise_for_status()  # генерируем исключение, если статус код ответа не 200
                        data_next = req_next.json()  # преобразуем JSON-ответ в словарь
                        vacancies.extend(data_next['items'])  # добавляем вакансии со следующей страницы в список
            return vacancies  # возвращаем список всех вакансий


        # обрабатываем ошибки связанные с HTTP-запросами и связанные с разбором JSON (возвращаем None в случае ошибки)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при получении вакансий работодателя {employer_id}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Ошибка при разборе JSON вакансий для работодателя {employer_id}: {e}")
            return None