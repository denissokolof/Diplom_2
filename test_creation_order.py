import pytest
import allure
import requests
import endpoints

#Создание заказа
class TestCreationOrder:

    @allure.title('Проверка создания заказа с авторизацией')

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


    @allure.title('Проверка создания заказа без авторизации') 
    def test_creation_order_without_auth_and_ingridients(self):
        
        with allure.step('Получение данных об ингредиентах'):
            ingredients_response = requests.get(endpoints.DATE_INGREDIENTS)
            ingredients_data = ingredients_response.json()
   
            valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data["data"][:2]]
            order_data = {"ingredients": valid_ingredients}
        
        response = requests.post(endpoints.ORDER_CREATE, data = order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 401


    @allure.title('Проверка создания заказа без ингредиентов')
    def test_creation_order_without_ingredients(self, created_user, delete_user):
        
        with allure.step('Добавление пользователя в список на удаление'):
            delete_user.append(created_user["access_token"])

        with allure.step('Создание заказа без ингредиентов'):
            headers = {"Authorization": created_user["access_token"]}
            order_data = {"ingredients": []}
            response = requests.post(endpoints.ORDER_CREATE,  headers = headers, data = order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 400


    @allure.title('Проверка создания заказа с неверным хэшем ингредиентов')
    def test_creation_order_with_invalid_ingredient(self, created_user, delete_user):
        
        with allure.step('Добавление пользователя в список на удаление'):
            delete_user.append(created_user["access_token"])

        with allure.step('Создание заказа с неверным id ингредиента'):
            headers = {"Authorization": created_user["access_token"]}
            order_data = {"ingredients": ["dgbdhbskksk"]}
            response = requests.post(endpoints.ORDER_CREATE,  headers = headers, data = order_data)

        with allure.step('Проверка кода ответа'):
            assert response.status_code == 500