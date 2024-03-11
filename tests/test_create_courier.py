import json

import allure
import fake as fake
import pytest as pytest

from data import EndpointsUrl
from main import *
import requests


class TestEndpointsUrl:
    # Создание курьера
    def test_create_courier(self):
        # Тест: курьера можно создать
        assert len(register_new_courier_and_return_login_password()) > 0

    def test_create_same_courier(self):
        # Тест: нельзя создать двух одинаковых курьеров
        first_courier = register_new_courier_and_return_login_password()
        second_courier = register_new_courier_and_return_login_password()
        assert first_courier != second_courier

    def test_create_courier_all_fields(self):
        # Тест: чтобы создать курьера, нужно передать в ручку все обязательные поля
        response = requests.post(EndpointsUrl.CREATE_COURIER, data={})
        assert response.status_code == 400  # Предположим, что сервер должен вернуть код 400 при отсутствии обязательных полей

    def test_create_courier_correct_response(self):
        # Тест: запрос возвращает правильный код ответа
        response = requests.post(EndpointsUrl.CREATE_COURIER, data={"login": "test_login", "password": "test_password", "firstName": "John"})
        assert response.status_code == 201

    def test_correct_response_of_create_courier_(self):
        # Тест: успешный запрос возвращает {"ok":true}
        login, password, first_name = register_new_courier_and_return_login_password()
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier',
                                 data={"login": login, "password": password, "firstName": first_name})
        assert response.json() == {"ok": True}

    def test_create_courier(self):
        # Тест: если одного из полей нет, запрос возвращает ошибку
        response = requests.post(EndpointsUrl.CREATE_COURIER, data={"login": "test_login", "password": "test_password"})
        assert response.status_code == 400  # Предположим, что сервер должен вернуть код 400 при отсутствии обязательных полей

    def test_create_courier(self):
        # Тест: если создать пользователя с логином, который уже есть, возвращается ошибка
        login, password, first_name = register_new_courier_and_return_login_password()
        response = requests.post(EndpointsUrl.CREATE_COURIER, data={"login": login, "password": password, "firstName": first_name})
        assert response.status_code == 409  # Предположим, что сервер должен вернуть код 409 при попытке создания пользователя с уже существующим логином

    # Логин курьера
    def test_courier_login(self):
        # Тест: курьер может авторизоваться
        login, password, _ = register_new_courier_and_return_login_password()
        response = requests.post(EndpointsUrl.LOGIN, data={"login": login, "password": password})
        assert response.status_code == 200

    def test_courier_login_all_fields(self):
        # Тест: для авторизации нужно передать все обязательные поля
        response = requests.post(EndpointsUrl.LOGIN, data={})
        assert response.status_code == 400  # Предположим, что сервер должен вернуть код 400 при отсутствии обязательных полей

    def test_courier_login_error_login(self):
        # Тест: система вернёт ошибку, если неправильно указать логин или пароль
        response = requests.post(EndpointsUrl.LOGIN, data={"login": "fake_login", "password": "fake_password"})
        assert response.status_code == 401  # Предположим, что сервер должен вернуть код 401 при неправильном логине или пароле

    def test_courier_login_error_not_all_fields(self):
        # Тест: если какого-то поля нет, запрос возвращает ошибку
        response = requests.post(EndpointsUrl.LOGIN, data={"login": "fake_login"})
        assert response.status_code == 400  # Предположим, что сервер должен вернуть код 400 при отсутствии обязательных полей

    def test_courier_login_non_existent_user(self):
        # Тест: если авторизоваться под несуществующим пользователем, запрос возвращает ошибку
        response = requests.post(EndpointsUrl.LOGIN, data={"login": "nonexistent_user", "password": "fake_password"})
        assert response.status_code == 404  # Предположим, что сервер должен вернуть код 404 при попытке авторизации несуществующего пользователя

    # Создание заказа
    @pytest.mark.parametrize('list_color', [
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title('Использование параметризации при выборе цвета самоката при создании заказа')
    def test_make_an_order(self, list_color):
        payload = {
            "firstName": f"{fake.name}",
            "lastName": f"{fake.name}",
            "address": f"Rostov, {fake.number}",
            "metroStation": 3,
            "phone": f"{fake.number}",
            "rentTime": 8,
            "deliveryDate": f"{fake.data}",
            "comment": f"{fake.comment}",
            "color": list_color
        }

        headers = {'Content-Type': 'application/json'}

        response = requests.post(EndpointsUrl.ORDER, data=json.dumps(payload), headers=headers)

        assert response.status_code == 201 and 'track' in response.json()

    def test_create_order(self):
        # Тест: можно указать один из цветов — BLACK или GREY
        response = requests.post(EndpointsUrl.ORDER, data={"color": "BLACK"})
        assert response.json()["track"]

    def test_create_order_with_two_color(self):
        # Тест: можно указать оба цвета
        response = requests.post(EndpointsUrl.ORDER, data={"color": ["BLACK", "GREY"]})
        assert response.json()["track"]

    def test_create_order_with_two_color(self):
        # Тест: можно совсем не указывать цвет
        response = requests.post(EndpointsUrl.ORDER, data={"color": [""]})
        assert response.json()["track"]