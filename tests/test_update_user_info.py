import allure
import pytest
import requests
from faker import Faker

from endpoints import Url, Endpoints


@allure.suite('Изменение данных пользователя')
class TestUpdateUserInfo:

    @allure.title('Изменение данных авторизованного пользователя')
    @allure.description('Запрос проверяет изменение поля {changed_data} у авторизованного пользователя')
    @pytest.mark.parametrize('changed_data', ['{"email": fake.email(), "password": data[1],"name": data[2]}',
                                              '{"email": data[0], "password": fake.password(), "name": data[2]}',
                                              '{"email": data[0], "password":data[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_updated_authorized_user(self, register_new_user_return_response, changed_data):
        data = register_new_user_return_response
        fake = Faker()
        payload = changed_data
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.patch(f'{Url.BASE_URL}{Endpoints.UPDATE_USER}', data=payload, headers=headers)
        email = response.json()['user']['email']
        name = response.json()['user']['name']

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"user":{{"email":"{email}","name":"{name}"}}}}'

    @allure.title('Изменение данных для не авторизованного пользователя')
    @allure.description('Запрос проверяет ошибку изменения поля {changed_data} у неавторизованного пользователя')
    @pytest.mark.parametrize('changed_data', ['{"email": fake.email(), "password": data[1],"name": data[2]}',
                                              '{"email": data[0], "password": fake.password(), "name": data[2]}',
                                              '{"email": data[0], "password":data[1], "name":fake.name()}'],
                             ids=['email', 'password', 'name'])
    def test_update_info_non_authorized_user(self, register_new_user_return_response, changed_data):
        data = register_new_user_return_response
        fake = Faker()
        payload = changed_data
        response = requests.patch(f'{Url.BASE_URL}{Endpoints.UPDATE_USER}', data=payload)

        assert response.status_code == 401 and response.text == \
               '{"success":false,"message":"You should be authorised"}'

    @allure.title('Изменение поля почты')
    @allure.description('Запрос проверяет ошибку изменения поля email, на почту, которая уже используется')
    def test_changed_email_to_email_already_use(self, register_new_user_return_response):
        data = register_new_user_return_response
        payload = {"email": "test-data@yandex.ru"}
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        response = requests.patch(f'{Url.BASE_URL}{Endpoints.UPDATE_USER}', data=payload, headers=headers)

        assert response.status_code == 403 and response.text == \
               '{"success":false,"message":"User with such email already exists"}'
