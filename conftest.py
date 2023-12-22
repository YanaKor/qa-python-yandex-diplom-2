import pytest
import requests

from endpoints import Url, Endpoints
import api


@pytest.fixture
def register_new_user_return_response():
    data = api.register_new_user_and_return_login_password()

    yield data[1]

    access_token = data[1].json()["accessToken"]
    requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})


@pytest.fixture
def register_new_user_return_login_and_password():
    data = api.register_new_user_and_return_login_password()

    yield data[0]

    access_token = data[1].json()["accessToken"]
    requests.delete(f"{Url.BASE_URL}{Endpoints.DELETE_USER}", headers={'Authorization': f'{access_token}'})
