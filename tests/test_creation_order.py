import pytest
import allure
import requests
import endpoints

#Создание заказа
class TestCreationOrder:

    @allure.title('Проверка создания заказа с авторизацией, верный код ответа')
    def test_creation_order_with_auth_and_ingridients(self, created_user, delete_user):

        with allure.step('Удаление пользователя'):
            delete_user.append(created_user["access_token"])
        
        with allure.step('Получение данных об ингредиентах'):
            ingredients_response = requests.get(endpoints.DATE_INGREDIENTS)
            ingredients_data = ingredients_response.json()
            valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]
            order_data = {"ingredients": valid_ingredients}

        with allure.step('Создание заказа с авторизацией'):
            header = {"Authorization": f"{created_user['access_token']}"}    

        response = requests.post(endpoints.ORDER_CREATE, headers = header , data = order_data)
        
        with allure.step('Проверка кода ответа'):
            assert response.status_code == 200

    @allure.title('Проверка создания заказа с авторизацией, верное тело ответа')
    def test_creation_order_with_auth_and_ingridients_correcr_body(self, created_user, delete_user):

        with allure.step('Удаление пользователя'):
            delete_user.append(created_user["access_token"])
        
        with allure.step('Получение данных об ингредиентах'):
            ingredients_response = requests.get(endpoints.DATE_INGREDIENTS)
            ingredients_data = ingredients_response.json()
            valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]
            order_data = {"ingredients": valid_ingredients}

        with allure.step('Создание заказа с авторизацией'):
            header = {"Authorization": f"{created_user['access_token']}"}    

        response = requests.post(endpoints.ORDER_CREATE, headers = header , data = order_data)
        
        with allure.step('Проверка тела ответа'):
            response_data = response.json()
            assert response_data == {
        'success': True,
        'name': response_data['name'], 
        'order': {
            '_id': response_data['order']['_id'],
            'createdAt': response_data['order']['createdAt'],
            'ingredients': response_data['order']['ingredients'],
            'name': response_data['order']['name'],
            'number': response_data['order']['number'],
            'owner': {
                'createdAt': response_data['order']['owner']['createdAt'],
                'email': response_data['order']['owner']['email'],
                'name': response_data['order']['owner']['name'],
                'updatedAt': response_data['order']['owner']['updatedAt']
            },
            'price': response_data['order']['price'],
            'status': response_data['order']['status'],
            'updatedAt': response_data['order']['updatedAt']
        }
    }


    @allure.title('Проверка создания заказа без авторизации, верный код ответа') 
    def test_creation_order_without_auth_and_ingridients(self):
        
        with allure.step('Получение данных об ингредиентах'):
            ingredients_response = requests.get(endpoints.DATE_INGREDIENTS)
            ingredients_data = ingredients_response.json()
   
            valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]
            order_data = {"ingredients": valid_ingredients}
        
        response = requests.post(endpoints.ORDER_CREATE, data = order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 401

    @allure.title('Проверка создания заказа без авторизации, верное тело ответа') 
    def test_creation_order_without_auth_and_ingridients_correct_body(self):
        
        with allure.step('Получение данных об ингредиентах'):
            ingredients_response = requests.get(endpoints.DATE_INGREDIENTS)
            ingredients_data = ingredients_response.json()
   
            valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]
            order_data = {"ingredients": valid_ingredients}
        
        response = requests.post(endpoints.ORDER_CREATE, data = order_data)

        with allure.step('Проверка тела ответа'):
            assert response.json() == {'success': False}


    @allure.title('Проверка создания заказа без ингредиентов, верный код ответа')
    def test_creation_order_without_ingredients(self, created_user, delete_user):
        
        with allure.step('Добавление пользователя в список на удаление'):
            delete_user.append(created_user["access_token"])

        with allure.step('Создание заказа без ингредиентов'):
            headers = {"Authorization": created_user["access_token"]}
            order_data = {"ingredients": []}
            response = requests.post(endpoints.ORDER_CREATE,  headers = headers, data = order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 400

    @allure.title('Проверка создания заказа без ингредиентов, верное тело ответа')
    def test_creation_order_without_ingredients_correct_body(self, created_user, delete_user):
        
        with allure.step('Добавление пользователя в список на удаление'):
            delete_user.append(created_user["access_token"])

        with allure.step('Создание заказа без ингредиентов'):
            headers = {"Authorization": created_user["access_token"]}
            order_data = {"ingredients": []}
            response = requests.post(endpoints.ORDER_CREATE,  headers = headers, data = order_data)

        with allure.step('Проверка тела ответа'):
            assert response.json() == {'success': False, 'message': 'Ingredient ids must be provided'}


    @allure.title('Проверка создания заказа с неверным хэшем ингредиентов, верный код ответа')
    def test_creation_order_with_invalid_ingredient(self, created_user, delete_user):
        
        with allure.step('Добавление пользователя в список на удаление'):
            delete_user.append(created_user["access_token"])

        with allure.step('Создание заказа с неверным id ингредиента'):
            headers = {"Authorization": created_user["access_token"]}
            order_data = {"ingredients": ["dgbdhbskksk"]}
            response = requests.post(endpoints.ORDER_CREATE,  headers = headers, data = order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 500
        