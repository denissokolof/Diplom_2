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
        

    @allure.title('Пользователь может авторизоваться, верное тело ответа')
    def test_login_user_success_correct_answer(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"], "password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        response_data = login_response.json()
        assert response_data == {
        'success': True,
        'accessToken': response_data['accessToken'],
        'refreshToken': response_data['refreshToken'],
        'user': {
            'email': user_data['email'],
            'name': response_data['user']['name']
        }
    }
    

    @allure.title('Нельзя авторизоваться без логина, правильный код ответа')
    def test_login_user_missing_login(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)    

        with allure.step('Повытка авторизации без логина'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.status_code == 401
    

    @allure.title('Нельзя авторизоваться без логина, правильное тело ответа')
    def test_login_user_missing_login_correct_body(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)    

        with allure.step('Повытка авторизации без логина'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title('Нельзя авторизоваться без пароля, правильный код ответа')
    def test_login_user_missing_password(self, user_data, delete_user):

        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Повытка авторизации без пароля'):
            password_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert password_response.status_code == 401


    @allure.title('Нельзя авторизоваться без пароля, правильное тело ответа')
    def test_login_user_missing_password_correct_answer(self, user_data, delete_user):

        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Повытка авторизации без пароля'):
            password_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert password_response.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title('Нельзя авторизоваться если логин не правильный, правильный код ответа')
    def test_login_user_wrong_login(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)
        
        with allure.step('Повытка авторизации с неправильным логином'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"email" : "wronglogin", "password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.status_code == 401

    
    @allure.title('Нельзя авторизоваться если логин не правильный, правильное тело ответа')
    def test_login_user_wrong_login_correct_answer(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)
        
        with allure.step('Повытка авторизации с неправильным логином'):
            login_response = requests.post(endpoints.USER_LOGIN, data={"email" : "wronglogin", "password" : user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert login_response.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title('Нельзя авторизоваться если пароль неправильный, правильный код ответа')
    def test_login_user_wrong_password(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)
        
        with allure.step('Повытка авторизации с неправильным паролем'):
            password_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"], "password" :  "wrongpassword"})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert password_response.status_code == 401

    
    @allure.title('Нельзя авторизоваться если пароль неправильный, правильное тело ответа')
    def test_login_user_wrong_password_correct_answer(self, user_data, delete_user):
        
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)
        
        with allure.step('Повытка авторизации с неправильным паролем'):
            password_response = requests.post(endpoints.USER_LOGIN, data={"email" : user_data["email"], "password" :  "wrongpassword"})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])
        
        assert password_response.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title('Нельзя авторизоваться под несуществующим пользователем, правильный код ответа')
    def test_login_courier_wrong_user(self):
        
        with allure.step('Повытка авторизации с несуществующим пользователем'):
            response = requests.post(endpoints.USER_LOGIN, data={"login" : "wronglogin1985", "password" :  "wrongpassword1074"})
        
        assert response.status_code == 401


    @allure.title('Нельзя авторизоваться под несуществующим пользователем, правильное тело ответа')
    def test_login_courier_wrong_user_correct_answer(self):
        
        with allure.step('Повытка авторизации с несуществующим пользователем'):
            response = requests.post(endpoints.USER_LOGIN, data={"login" : "wronglogin1985", "password" :  "wrongpassword1074"})
        
        assert response.json() == {'success': False, 'message': 'email or password are incorrect'}
    

    @allure.title("Система вернёт ошибку, если логин пустой, правильный код ответа")
    def test_login_with_empty_login(self, user_data, delete_user):
    
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация с пустым логином'):
            response_login = requests.post(endpoints.USER_LOGIN, data={"email": "","password": user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])

        assert response_login.status_code == 401  
     
   
    @allure.title("Система вернёт ошибку, если логин пустой, правильное тело ответа")
    def test_login_with_empty_login_correct_answer(self, user_data, delete_user):
    
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация с пустым логином'):
            response_login = requests.post(endpoints.USER_LOGIN, data={"email": "","password": user_data["password"]})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])

        assert response_login.json() == {'success': False, 'message': 'email or password are incorrect'}


    @allure.title("Система вернёт ошибку, если пароль пустой, правильный код ответа")
    def test_login_with_empty_password(self, user_data, delete_user):
    
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация с пустым паролем'):
            response_login = requests.post(endpoints.USER_LOGIN, data={"email": user_data["email"], "password": ""})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])

        assert response_login.status_code == 401
   
   
    @allure.title("Система вернёт ошибку, если пароль пустой, правильное тело ответа")
    def test_login_with_empty_password_correct_answer(self, user_data, delete_user):
    
        with allure.step('Создание пользователя через API'):
            response = requests.post(endpoints.USER_CREATE, data = user_data)

        with allure.step('Авторизация с пустым паролем'):
            response_login = requests.post(endpoints.USER_LOGIN, data={"email": user_data["email"], "password": ""})

        with allure.step('Удаление пользователя'):
            response_data = response.json()
            delete_user.append(response_data["accessToken"])

        assert response_login.json() == {'success': False, 'message': 'email or password are incorrect'}
