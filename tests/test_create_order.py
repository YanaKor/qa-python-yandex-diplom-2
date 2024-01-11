import allure
import requests

from endpoints import Url, Endpoints


@allure.suite('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа авторизованным пользователем')
    @allure.description('Запрос проверяет успешное создание заказа авторизованным пользователем')
    def test_create_order_for_authorized_user(self, register_new_user_return_response):
        data = register_new_user_return_response
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        payload = {
            'ingredients': ['61c0c5a71d1f82001bdaaa6c']
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.GET_ORDERS}', data=payload, headers=headers)

        assert response.status_code == 200

    @allure.title('Создание заказа не авторизованным пользователем')
    @allure.description('Запрос проверяет создание заказа пользователем, не авторизованным на сайте')
    def test_create_order_for_non_authorized_user(self):
        payload = {
            'ingredients': ['61c0c5a71d1f82001bdaaa75', '61c0c5a71d1f82001bdaaa71']
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.GET_ORDERS}', data=payload)
        name = response.json()['name']
        order_number = response.json()["order"]["number"]

        assert response.status_code == 200 and response.text == \
               f'{{"success":true,"name":"{name}","order":{{"number":{order_number}}}}}'

    @allure.title('Создание заказа без ингредиентов авторизованным пользователем')
    @allure.description('Запрос проверяет возможность создания заказа без ингредиенов пользователем, '
                        'авторизованным на сайте')
    def test_create_order_without_ingredients_for_authorized_user(self, register_new_user_return_response):
        data = register_new_user_return_response
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        payload = {
            'ingredients': ['']
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.GET_ORDERS}', data=payload, headers=headers)

        assert response.status_code == 400 and response.text == \
               '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title('Создание заказа без ингредиентов не авторизованным пользователем')
    @allure.description('Запрос проверяет возможность создания заказа без ингредиенов пользователем, '
                        'не авторзованным на сайте')
    def test_create_order_without_ingredients_for_non_authorized_user(self):
        payload = {
            'ingredients': ['']
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.GET_ORDERS}', data=payload)

        assert response.status_code == 400 and response.text == \
               '{"success":false,"message":"Ingredient ids must be provided"}'

    @allure.title('Невозможно создать заказ с невалидным хешем ингредиента')
    @allure.description('Запрос проверяет невозможность создания заказа, если указать невалидных хеш ингредиента')
    def test_create_order_wrong_ingredient_ids(self, register_new_user_return_response):
        data = register_new_user_return_response
        access_token = data.json()['accessToken']
        headers = {"Authorization": f"{access_token}"}
        payload = {
            'ingredients': ['456nfgjh978fjghjkh65']
        }
        response = requests.post(f'{Url.BASE_URL}{Endpoints.GET_ORDERS}', data=payload, headers=headers)

        assert response.status_code == 500
