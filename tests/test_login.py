import pytest
import requests
import allure
from faker import Faker

from endpoints import Url, Endpoints


@allure.suite('Авторизация пользователя')
class TestLoginUser:

    @allure.title('Авторизация зарегистрированного существующего пользователя')
    @allure.description('Запрос проверяет авторизацию существующего пользователя с валидными данными')
    def test_login_registered_user_success(self, register_new_user_return_login_and_password):
        data = register_new_user_return_login_and_password
        payload = {
            "email": data[0],
            "password": data[1]
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.LOGIN}', data=payload)
        email = response.json()["user"]["email"]
        name = response.json()["user"]["name"]
        access_token = response.json()["accessToken"]
        refresh_token = response.json()["refreshToken"]

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"accessToken":"{access_token}","refreshToken":"{refresh_token}",' \
               f'"user":{{"email":"{email}","name":"{name}"}}}}'

    @allure.title('Авторизация с неверным {email} пользователя ')
    @allure.description('Запрос проверяет авторизацию с несуществующей почтой пользователя, но с корректным паролем')
    @pytest.mark.parametrize('email', ['faker.email()', ' '], ids=['incorrect_email', 'empty_email'])
    def test_login_user_incorrect_email_and_correct_password(self, register_new_user_return_login_and_password,
                                                             email):
        faker = Faker()
        data = register_new_user_return_login_and_password
        payload = {
            "email": email,
            "password": data[1]
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.LOGIN}', data=payload)
        assert response.status_code == 401 and response.text == \
               '{"success":false,"message":"email or password are incorrect"}'

    @allure.title('Авторизация с неверным {password} пользователя ')
    @allure.description('Запрос проверяет авторизацию с корренктной почтой пользователя, но с не верным паролем')
    @pytest.mark.parametrize('password', ['faker.password()', ' '], ids=['incorrect password', 'empty password'])
    def test_login_user_correct_email_incorrect_password(self, register_new_user_return_login_and_password, password):
        faker = Faker()
        data = register_new_user_return_login_and_password
        payload = {
            "email": data[0],
            "password": password
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.LOGIN}', data=payload)
        assert response.status_code == 401 and response.text == \
               '{"success":false,"message":"email or password are incorrect"}'