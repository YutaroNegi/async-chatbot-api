from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.auth import get_current_user
from app.models.users import User
from app.utils.chatbot import generate_bot_response
from app import config
import uuid
import boto3
from datetime import datetime
import logging

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    dependencies=[Depends(get_current_user)],
)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# DynamoDB client
dynamodb = boto3.resource("dynamodb")
messages_table = dynamodb.Table(config.DYNAMO_MESSAGES_TABLE)


class Message(BaseModel):
    content: str


@router.post("/")
async def send_message(
    message: Message, current_user: User = Depends(get_current_user)
):
    # Generate unique message ID
    id_message = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    id_user = current_user.sub

    # Store the user's message in DynamoDB
    user_message_item = {
        "id_message": id_message,
        "id_user": id_user,
        "content": message.content,
        "timestamp": timestamp,
        "is_bot": False,
    }

    try:
        messages_table.put_item(Item=user_message_item)
        logger.info(f"User message stored: {user_message_item}")
    except Exception as e:
        logger.error(f"Error storing user message: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Generate bot response
    bot_response_content = generate_bot_response(message.content)
    bot_id_message = str(uuid.uuid4())
    bot_timestamp = datetime.utcnow().isoformat()

    bot_message_item = {
        "id_message": bot_id_message,
        "id_user": id_user,
        "content": bot_response_content,
        "timestamp": bot_timestamp,
        "is_bot": True,
    }

    try:
        messages_table.put_item(Item=bot_message_item)
        logger.info(f"Bot message stored: {bot_message_item}")
    except Exception as e:
        logger.error(f"Error storing bot message: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Return both messages
    return {
        "user_message": user_message_item,
        "bot_response": bot_message_item,
    }


@router.put("/{message_id}")
async def edit_message(message_id: int, new_content: str):
    # Implement message editing logic here
    return {"message_id": message_id, "new_content": new_content}


@router.delete("/{message_id}")
async def delete_message(message_id: int):
    # Implement message deletion logic here
    return {"message_id": message_id, "status": "deleted"}
