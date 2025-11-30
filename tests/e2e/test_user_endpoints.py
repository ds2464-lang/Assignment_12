def test_register_login_endpoint(fastapi_server):
    import requests

    base_url = fastapi_server
    register_url = f"{base_url}users/register"
    login_url = f"{base_url}users/login"

    # Register
    response = requests.post(register_url, json={
        "first_name": "Bob",
        "last_name": "Jones",
        "email": "bob@example.com",
        "username": "bob",
        "password": "StrongPass123!",
        "confirm_password": "StrongPass123!"
    })
    assert response.status_code == 200
    user_id = response.json()["id"]

    # Login
    response = requests.post(login_url, json={
        "username": "bob",
        "password": "StrongPass123!"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None
