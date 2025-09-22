import pytest
import string
import random
import requests
import endpoints

@pytest.fixture()
#Уникальные данные для пользователя
def user_data():
        
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    return {
        "email": f"{generate_random_string()}@example.com",
        "password": generate_random_string(8),
        "name": generate_random_string()
    }

#Cоздание пользователя и получения токена
@pytest.fixture()
def created_user(user_data):
    
    response = requests.post(f"{endpoints.BASE_URL}/auth/register", data=user_data)
    
    user_response = response.json()
    
    return {
        "user_data": user_data,
        "access_token": user_response.get("accessToken"),
        "refresh_token": user_response.get("refreshToken")
    }

#Удаление пользователя
@pytest.fixture()
def delete_user():
    
    access_tokens = []
    
    yield access_tokens
    
    # После теста удаляем всех пользователей из списка
    for token in access_tokens:
        clean_token = token.replace("Bearer ", "")
        headers = {"Authorization": f"Bearer {clean_token}"}
        requests.delete(f"{endpoints.BASE_URL}/auth/user", headers=headers)