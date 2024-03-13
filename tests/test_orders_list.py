import requests
import allure

from links import Endpoints


@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('')
    def test_list_order(self):
        request_url = Endpoints.ORDER

        with allure.step("Шаг 1: GET-запрос на получение списка заказов"):
            response = requests.get(request_url)

        with allure.step("Шаг 2: Проверка ответа"):
            assert response.status_code == 200

        with allure.step("Шаг 3: Проверка наличия списка заказов в ответе"):
            assert "orders" in response.json() and type(response.json()["orders"]) is list
