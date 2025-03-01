import pytest
from scr.api_function import HHApi
import requests

def test_hh_api_init():
    hh_api = HHApi()
    assert hh_api.base_url == "https://api.hh.ru"  # Check the default value
    assert hh_api.max_vacancies == 10

@pytest.fixture
def hh_api():
    return HHApi()

def test_get_employer_vacancies_success(mocker, hh_api):
    # Мокируем успешный ответ от API
    mock_response = {
        "items": [{"id": "123", "name": "Test Vacancy"}],
        "found": 1
    }

    # Используем mocker.patch для замены requests.get
    mocker.patch("scr.api_function.requests.get", return_value=mocker.MagicMock(json=lambda: mock_response,
                                                                            raise_for_status=lambda: None))

    vacancies = hh_api.get_employer_vacancies(12345)
    assert len(vacancies) == 1
    assert vacancies[0]["name"] == "Test Vacancy"

def test_get_employer_vacancies_failure(mocker, hh_api):
    # Имитируем ошибку API
    mocker.patch("scr.api_function.requests.get", side_effect=requests.exceptions.RequestException("API Error"))

    vacancies = hh_api.get_employer_vacancies(12345)
    assert len(vacancies) == 0  # Ожидаем пустой список в случае ошибки