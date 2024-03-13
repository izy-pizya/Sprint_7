import allure

from main import *


@allure.feature('Создание курьера')
class TestCreateCourier:


    @allure.title('Тест: Успешное создание курьера')
    def test_create_courier_success(self):

        methodgenerate = MethodGenerate()
        login = methodgenerate.random_generation()
        password = methodgenerate.random_generation()
        first_name = methodgenerate.random_generation()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(Endpoints.CREATE_COURIER, data=payload)
        success_message = '{"ok":true}'
        assert 201 == response.status_code and success_message in response.text

    @allure.title('Тест: нельзя создать двух одинаковых курьеров')
    def test_create_same_courier(self):

        methodgenerate = MethodGenerate()
        login, password, first_name = methodgenerate.register_new_courier_and_return_login_password()
        response = requests.post(Endpoints.CREATE_COURIER,
                                 json={'login': login, 'password': password, 'first_name': first_name})
        error_message = "Этот логин уже используется. Попробуйте другой."
        assert 409 == response.status_code and error_message in response.text

    @allure.title('Тест: чтобы создать курьера, нужно передать в ручку все обязательные поля')
    def test_create_courier_all_fields(self):

        response = requests.post(Endpoints.CREATE_COURIER, data={})
        assert response.status_code == 400

    @allure.title('Тест: запрос возвращает правильный код ответа')
    def test_create_courier_correct_response(self):

        methodgenerate = MethodGenerate()
        login = methodgenerate.random_generation()
        password = methodgenerate.random_generation()

        payload = {
            "login": login,
            "password": password,
        }

        response = requests.post(Endpoints.CREATE_COURIER, data=payload)
        message = '"ok":true'
        assert response.status_code == 201 and message in response.text

    @allure.title('Тест: если одного из полей нет, запрос возвращает ошибку')
    def test_create_courier_miss_one_field(self):

        response = requests.post(Endpoints.CREATE_COURIER, data={"login": "test_login1", "password": "test_password"})
        assert response.status_code == 409

    @allure.title('Тест: если создать пользователя с логином, который уже есть, возвращается ошибка')
    def test_create_courier_with_same_login(self):

        methodgenerate = MethodGenerate()
        login, password, first_name = methodgenerate.register_new_courier_and_return_login_password()
        response = requests.post(Endpoints.CREATE_COURIER, data={"login": login, "password": password, "firstName": first_name})
        assert response.status_code == 409