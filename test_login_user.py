import pytest
import allure
import requests
import endpoints

#Авторизация пользователя
class TestLoginUser:

    @allure.title('Пользователь может авторизоваться')
    def test_login_user_success(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"], "password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.status_code == 200

    
    @allure.title('Нельзя авторизоваться без логина')
    def test_login_user_missing_login(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)    

        with allure.step('Повытка авторизации без логина'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title('Нельзя авторизоваться без пароля')
    def test_login_user_missing_password(self, user_data, delete_user):

        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Повытка авторизации без пароля'):
            password_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert password_response.status_code == 401

    
    @allure.title('Нельзя авторизоваться если логин не правильный')
    def test_login_user_wrong_login(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)
        
        with allure.step('Повытка авторизации с неправильным логином'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"email" : "wronglogin", "password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.json() == {'success': False, 'message': 'email or password are incorrect'}

    
    @allure.title('Нельзя авторизоваться если пароль неправильный')
    def test_login_user_wrong_login(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)
        
        with allure.step('Повытка авторизации с неправильным паролем'):
            password_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"], "password" :  "wrongpassword"})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert password_response.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title('Нельзя авторизоваться под несуществующим пользователем')
    def test_login_courier_wrong_user(self):
        
        with allure.step('Повытка авторизации с несуществующим пользователем'):
            response = requests.post(endpoints.USER_LOGIN, data={"login" : "wronglogin1985", "password" :  "wrongpassword1074"})
        
        assert response.json() == {'success': False, 'message': 'email or password are incorrect'}
    

    @allure.title("Система вернёт ошибку, если логин пустой")
    def test_login_with_empty_login(self, user_data, delete_user):
    
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация с пустым логином'):
            response_login = requests.post(endpoints.USER_LOGIN, data={"email": "","password": user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])

        assert response_login.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title("Система вернёт ошибку, если пароль пустой")
    def test_login_with_empty_password(self, user_data, delete_user):
    
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация с пустым паролем'):
            response_login = requests.post(endpoints.USER_LOGIN, data={"email": user_data["email"], "password": ""})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])

        assert response_login.json() == {'success': False, 'message': 'email or password are incorrect'}