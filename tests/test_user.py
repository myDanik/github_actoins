from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={
        'email': 'nonexisted.email@example.com'
    })
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
    

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    response = client.post("/api/v1/user", json={
        'name': 'example name',
        'email': 'valid.email@valid.com'
    })
    assert response.status_code == 201
    assert client.get("api/v1/user", params={'email': 'valid.email@valid.com'}).status_code == 200

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    response = client.post("/api/v1/user", json={
        'name': 'example name',
        'email': users[0]['email']
    })
    assert response.status_code == 409
    assert client.get("api/v1/user", params={'email': users[0]['email']}).json()['name'] == users[0]['name']
    

def test_delete_user():
    '''Удаление пользователя'''
    response = client.delete("/api/v1/user", params={
        'email': users[0]['email']
    })
    assert response.status_code == 204
    assert client.get("api/v1/user", params={'email': users[0]['email']}).status_code == 404
