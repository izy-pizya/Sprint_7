import random
import string

import allure
import requests

from links import *


class MethodGenerate:

    @allure.step("Random Generation")
    def random_generation(self):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(10))
        return random_string

    @allure.step("Register new courier and return login password")
    def register_new_courier_and_return_login_password(self):
        login_pass = []

        login = self.random_generation()
        password = self.random_generation()
        first_name = self.random_generation()

        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(Endpoints.CREATE_COURIER, data=payload)

        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        return login_pass