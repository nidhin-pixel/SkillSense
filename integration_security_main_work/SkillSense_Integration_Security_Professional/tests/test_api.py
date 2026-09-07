from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def login(email):
    response = client.post("/api/auth/login", json={"email": email, "password": "Demo@12345"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_login_and_profile():
    token = login("official@example.com")
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["role"] == "official"

def test_rbac_denies_official_admin_route():
    token = login("official@example.com")
    response = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_department_admin_can_list_users():
    token = login("department@example.com")
    response = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 3
