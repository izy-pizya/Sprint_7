import allure

from helpers import *


@allure.feature('Логин курьера')
class TestLogIn:

    @allure.title('Тест: курьер может авторизоваться')
    def test_courier_login(self):

        methodgenerate = MethodGenerate()
        login, password, _ = methodgenerate.register_new_courier_and_return_login_password()
        response = requests.post(Endpoints.LOGIN, data={"login": login, "password": password})
        success_message = '{"id":27'
        assert response.status_code == 200 and success_message in response.text

    @allure.title('Тест: для авторизации нужно передать все обязательные поля')
    def test_courier_login_all_fields(self):

        response = requests.post(Endpoints.LOGIN, data={})
        message = 'Service unavailable'
        assert response.status_code == 504 and message in response.text

    @allure.title('Тест: система вернёт ошибку, если неправильно указать логин или пароль')
    def test_courier_login_error_login(self):

        response = requests.post(Endpoints.LOGIN, data={"login": "fake_login", "password": "fake_password"})
        message = '"Учетная запись не найдена"'
        assert response.status_code == 404 and message in response.text

    @allure.title('Тест: если какого-то поля нет, запрос возвращает ошибку')
    def test_courier_login_error_not_all_fields(self):

        response = requests.post(Endpoints.LOGIN, data={"login": "fake_login"})
        message = 'Service unavailable'
        assert response.status_code == 504 and message in response.text

    @allure.title('Тест: если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_courier_login_non_existent_user(self):

        response = requests.post(Endpoints.LOGIN, data={"login": "nonexistent_user", "password": "fake_password"})
        message = '"Учетная запись не найдена"'
        assert response.status_code == 404 and message in response.text

