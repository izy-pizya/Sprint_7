import allure
import requests

from links import Endpoints
from main import MethodGenerate


@allure.feature('Логин курьера')
class TestLogIn:

    @allure.title('Тест: курьер может авторизоваться')
    def test_courier_login(self):

        methodgenerate = MethodGenerate()
        login, password, _ = methodgenerate.register_new_courier_and_return_login_password()
        response = requests.post(Endpoints.LOGIN, data={"login": login, "password": password})
        assert response.status_code == 200

    @allure.title('Тест: для авторизации нужно передать все обязательные поля')
    def test_courier_login_all_fields(self):

        response = requests.post(Endpoints.LOGIN, data={})
        assert response.status_code == 504

    @allure.title('Тест: система вернёт ошибку, если неправильно указать логин или пароль')
    def test_courier_login_error_login(self):

        response = requests.post(Endpoints.LOGIN, data={"login": "fake_login", "password": "fake_password"})
        assert response.status_code == 404

    @allure.title('Тест: если какого-то поля нет, запрос возвращает ошибку')
    def test_courier_login_error_not_all_fields(self):

        response = requests.post(Endpoints.LOGIN, data={"login": "fake_login"})
        assert response.status_code == 504

    @allure.title('Тест: если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_courier_login_non_existent_user(self):

        response = requests.post(Endpoints.LOGIN, data={"login": "nonexistent_user", "password": "fake_password"})
        assert response.status_code == 404

