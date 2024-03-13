import json
import allure
import data_for_tests
import pytest as pytest
import requests

from links import Endpoints


@allure.feature('Создание заказа')
class TestOrders:

    @allure.title('Тест с параметрами: успешный ответ с разными входными данными ')
    @pytest.mark.parametrize('list_color', [
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    @allure.title('')
    def test_make_an_order(self, list_color):
        data_for_tests.order_data["color"] = list_color
        payload = data_for_tests.order_data

        headers = {'Content-Type': 'application/json'}

        response = requests.post(Endpoints.ORDER, data=json.dumps(payload), headers=headers)

        assert response.status_code == 201 and 'track' in response.json()

