import pytest
import allure
import requests
import endpoints

#Создание пользователя
class TestCrearionUser:

    @allure.title('Успешное создание уникального пользователя и верный код')
    def test_create_user_success_correct_answer_code(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert response.status_code == 200


    @allure.title('Успешное создание пользователя, верное тело ответа')
    def test_create_user_success_correct_answer_body(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        response_data = response.json()

        with allure.step('Удаление пользователя'):
            delete_user.append(response_data["accessToken"])
        
        assert (response_data["success"] == True) and "accessToken", "refreshToken" in response_data


    @allure.title('Нельзя создать двух одинаковых пользователей, верный код ответа')
    def test_create_duplicate_courier_correct_answer_code(self, user_data, delete_user):
        
        with allure.step('Создание первого пользователя через API'):
            response1 = requests.post(endpoints.USER_CREATE, data=user_data)

        with allure.step('Создание второго пользователя через API'):
            response2 = requests.post(endpoints.USER_CREATE, data=user_data)

        with allure.step('Удаление пользователя'):
            response_data = response1.json()
            delete_user.append(response_data["accessToken"])

        assert response2.status_code == 403

    
    @allure.title('Нельзя создать двух одинаковых пользователей, верное тело ответа')
    def test_create_duplicate_courier_correct_answer_body(self, user_data, delete_user):
        
        with allure.step('Создание первого пользователя через API'):
            response1 = requests.post(endpoints.USER_CREATE, data=user_data)

        with allure.step('Создание второго пользователя через API'):
            response2 = requests.post(endpoints.USER_CREATE, data=user_data)

        with allure.step('Удаление пользователя'):
            response_data = response1.json()
            delete_user.append(response_data["accessToken"])

        assert response2.json() == {'success': False, 'message': 'User already exists'}

    
    @allure.title('Нельзя создать пользователя без логина, верное тело ответа')
    def test_create_user_missing_login_correct_answer_body(self, user_data):
        
        payload = user_data.copy()
        del payload["email"]
        
        with allure.step('Попытка создание пользователя через API без логина'):
            response = requests.post(endpoints.USER_CREATE, data=payload)
        
        assert response.json() == {'message': 'Email, password and name are required fields', 'success': False,}

    @allure.title('Нельзя создать пользователя без логина, верный код ответа')
    def test_create_user_missing_login_correct_answer_code(self, user_data):
        
        payload = user_data.copy()
        del payload["email"]
        
        with allure.step('Попытка создание пользователя через API без логина'):
            response = requests.post(endpoints.USER_CREATE, data=payload)
        
        assert response.status_code == 403
    

    @allure.title('Нельзя создать пользователя без пароля, верное тело ответа')
    def test_create_user_missing_password_correct_answer_body(self, user_data):
        
        payload = user_data.copy()
        del payload["password"]
        
        with allure.step('Попытка создание пользователя через API без пароля'):
            response = requests.post(endpoints.USER_CREATE, data=payload)
        
        assert response.json() == {'message': 'Email, password and name are required fields',  'success': False,}

    @allure.title('Нельзя создать пользователя без пароля, верный код ответа')
    def test_create_user_missing_password_correct_answer_code(self, user_data):
        
        payload = user_data.copy()
        del payload["password"]
        
        with allure.step('Попытка создание пользователя через API без пароля'):
            response = requests.post(endpoints.USER_CREATE, data=payload)
        
        assert response.status_code == 403


    @allure.title('Нельзя создать пользователя без имени, верное тело ответа')
    def test_create_user_missing_name_correct_answer_body(self, user_data):
        
        payload = user_data.copy()
        del payload["name"]
        
        with allure.step('Попытка создание пользователя через API без имени'):
            response = requests.post(endpoints.USER_CREATE, data=payload)
        
        assert response.json() == {'message': 'Email, password and name are required fields',  'success': False,}

    
    @allure.title('Нельзя создать пользователя без имени, верный код ответа')
    def test_create_user_missing_name_correct_answer_code(self, user_data):
        
        payload = user_data.copy()
        del payload["name"]
        
        with allure.step('Попытка создание пользователя через API без имени'):
            response = requests.post(endpoints.USER_CREATE, data=payload)
        
        assert response.status_code == 403

