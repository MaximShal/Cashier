def test_registration(client):
    response = client.post("/api/user", json={
        "login": "test_user",
        "password": "test_password",
        "name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["login"] == "test_user"


def test_login(client):
    response = client.post("/api/user/token", json={
        "login": "test_user",
        "password": "test_password"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
