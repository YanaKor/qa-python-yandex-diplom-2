import allure
import pytest
import requests

from endpoints import Url, Endpoints


@allure.suite('Регистрация нового пользователя')
class TestRegisterUser:

    @allure.title('Успешная регистрация пользователя')
    @allure.description('Запрос проверяет создание пользователя с заполнением всех обязательных полей')
    def test_register_new_user_success(self, register_new_user_return_response):
        response = register_new_user_return_response

        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}},' \
               f'"accessToken":"{access_token}","refreshToken":"{refresh_token}"}}'

    @allure.title('Повторная регистрация существующего пользователя')
    @allure.description('Запрос проверяет повторную регистрацию уже существующего пользователя')
    def test_register_same_user(self, register_new_user_return_login_and_password):
        data = register_new_user_return_login_and_password
        email = data[0]
        password = data[1]
        name = data[2]
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.REGISTER_USER}', data=payload)

        assert response.status_code == 403 and response.text == '{"success":false,"message":"User already exists"}'

    @allure.title('Регистрация пользователя без обязательного поля {deleted_field}')
    @allure.description('Запрос проверяет регистрацию пользователя с пустым обязательным полем {deleted_field}')
    @pytest.mark.parametrize('deleted_field', ['email', 'password', 'name'])
    def test_register_new_user_without_required_field(self, register_new_user_return_login_and_password, deleted_field):
        data = register_new_user_return_login_and_password
        email = data[0]
        password = data[1]
        name = data[2]
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        del payload[deleted_field]
        response = requests.post(f'{Url.BASE_URL}{Endpoints.REGISTER_USER}', data=payload)
        assert response.status_code == 403 and response.text ==\
               '{"success":false,"message":"Email, password and name are required fields"}'
