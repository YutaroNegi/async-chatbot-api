from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from botocore.exceptions import ClientError

client = TestClient(app)

# Mock data
valid_user = {"email": "testuser@example.com", "password": "Password123"}

existing_user = {"email": "existinguser@example.com", "password": "Password123"}

invalid_password_user = {"email": "newuser@example.com", "password": "pass"}


@patch("app.routers.users.cognito_client")
def test_register_user_success(mock_cognito_client):
    mock_cognito_client.admin_create_user.return_value = {}
    mock_cognito_client.admin_set_user_password.return_value = {}
    mock_cognito_client.admin_confirm_sign_up.return_value = {}

    response = client.post("/users/register", json=valid_user)
    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully"}


@patch("app.routers.users.cognito_client")
def test_register_user_existing_email(mock_cognito_client):
    mock_cognito_client.admin_create_user.side_effect = ClientError(
        {
            "Error": {
                "Code": "UsernameExistsException",
                "Message": "User already exists",
            }
        },
        "AdminCreateUser",
    )

    response = client.post("/users/register", json=existing_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_user_invalid_password():
    response = client.post("/users/register", json=invalid_password_user)
    assert response.status_code == 422


def test_register_user_invalid_email():
    invalid_email_user = {"email": "invalidemail", "password": "Password123"}
    response = client.post("/users/register", json=invalid_email_user)
    assert response.status_code == 422
