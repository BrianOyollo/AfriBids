import pytest
from app import schemas, models


def test_get_all_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(),list)

def test_create_user(client):
    dummy_user = {
        "email":"testuser@gmail.com",
        "display_name":"testuser_123",
        "password": "TestPassword123"
    }
    response = client.post("/users/new", json=dummy_user)
    created_user = response.json()
    assert response.status_code == 201
    assert created_user['email'] == dummy_user['email']
    assert created_user['display_name'] == dummy_user['display_name']
    assert created_user['password'] == dummy_user['password']


@pytest.mark.parametrize("email,display_name,password,response_code",[
    ('testuser@gmail.com','testuser',None,422),
    ('testuser@gmail.com',None,'TestPassword123',422),
    (None,'testuser','TestPassword123',422)
])
def test_create_user_with_missing_details(client, email,display_name, password,response_code):
    response = client.post("/users/new", json={'email':email, 'display_name':display_name,'password':password})
    assert response.status_code == response_code

def test_creating_user_with_exisiting_email(client, test_user):
    dummy_user = {
        "email":"testuser@gmail.com",
        "display_name":"testuser_123",
        "password": "TestPassword123"
    }
    response = client.post("/users/new", json=dummy_user)
    assert response.status_code == 409
    

def test_get_existing_user(client, test_user):
    response = client.get(f"/users/{test_user['user_id']}")
    user = schemas.UserOut(**response.json())

    assert response.status_code == 200
    assert user.user_id == test_user['user_id']
    assert user.username == test_user['username']
    assert user.display_name == test_user['display_name']

def test_nonexistent_user(client):
    response = client.get("/users/132322442")
    assert response.status_code == 404

