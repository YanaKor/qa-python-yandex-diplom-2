import allure
import pytest
import requests

from endpoints import Url, Endpoints
import api


@pytest.fixture(scope='function')
def register_new_user_return_response():
    with allure.step('Получение данных о зарегистрированном пользователе'):
        data = api.register_new_user_and_return_login_password()

        yield data[1]

    with allure.step('Получение токена созданного пользователя'):
        access_token = data[1].json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})


@pytest.fixture(scope='function')
def register_new_user_return_login_and_password():
    with allure.step('Получение логина и пароля зарегистрированного пользователя'):
        data = api.register_new_user_and_return_login_password()

        yield data[0]

    with allure.step('Получение токена созданного пользователя'):
        access_token = data[1].json()["accessToken"]
    with allure.step('Удаление созданного пользователя'):
        requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})
