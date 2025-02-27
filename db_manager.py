import psycopg2
from typing import List, Dict, Optional

class DBManager:
    """
    Класс для работы с базой данных PostgreSQL, содержащей информацию о компаниях и вакансиях.
    """

    def __init__(self, db_name: str, params: Dict[str, str]):
        """
        Инициализирует экземпляр класса.

        Args:
            db_namе: Имя базы данных.
            params: Параметры подключения к базе данных.
        """
        self.db_name: str = db_name
        self.params: Dict[str, str] = params