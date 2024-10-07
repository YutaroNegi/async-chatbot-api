import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.auth import get_current_user
from app.models.users import User
import uuid

client = TestClient(app)

test_user = User(
    sub="test-user-id",
    username="testuser",
    iss="https://cognito-idp.us-east-1.amazonaws.com/us-east-1_example",
    client_id="test-client-id",
    token_use="access",
    scope="aws.cognito.signin.user.admin",
    exp=9999999999,
    iat=0,
    jti=str(uuid.uuid4()),
)


async def mock_get_current_user():
    return test_user


mock_dynamodb_table = MagicMock()


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_dynamodb():
    with patch("app.routers.messages.messages_table", mock_dynamodb_table):
        yield


def test_list_messages():
    mock_dynamodb_table.query.return_value = {
        "Items": [
            {
                "id_message": "message1",
                "id_user": test_user.sub,
                "content": "Hello!",
                "timestamp": "2024-10-07T07:33:21.023112",
                "is_bot": False,
            },
            {
                "id_message": "message2",
                "id_user": test_user.sub,
                "content": "Hi there!",
                "timestamp": "2024-10-07T07:35:21.023112",
                "is_bot": True,
            },
        ],
        "LastEvaluatedKey": {"id_message": "message2", "id_user": test_user.sub},
    }

    response = client.get("/messages/", headers={"Authorization": "Bearer valid_token"})
    assert response.status_code == 200
    data = response.json()
    assert "messages" in data
    assert len(data["messages"]) == 2
    assert data["messages"][0]["id_message"] == "message1"
    assert data["messages"][1]["id_message"] == "message2"


def test_send_message():
    mock_dynamodb_table.put_item.return_value = {}

    with patch(
        "app.routers.messages.generate_bot_response"
    ) as mock_generate_bot_response:
        mock_generate_bot_response.return_value = "This is a bot response."

        payload = {"content": "Hello, chatbot!"}
        response = client.post(
            "/messages/",
            headers={"Authorization": "Bearer valid_token"},
            json=payload,
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_message" in data
        assert "bot_response" in data
        assert data["user_message"]["content"] == payload["content"]
        assert data["bot_response"]["content"] == "This is a bot response."


def test_delete_message():
    message_id = "message1"

    mock_dynamodb_table.get_item.return_value = {
        "Item": {
            "id_message": message_id,
            "id_user": test_user.sub,
            "content": "Message to be deleted",
            "timestamp": "2024-10-07T07:33:21.023112",
            "is_bot": False,
        }
    }

    mock_dynamodb_table.delete_item.return_value = {}

    response = client.delete(
        f"/messages/{message_id}",
        headers={"Authorization": "Bearer valid_token"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id_message"] == message_id
    assert data["status"] == "deleted"
