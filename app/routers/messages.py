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
    id_message = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    id_user = current_user.sub

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

    return {
        "user_message": user_message_item,
        "bot_response": bot_message_item,
    }


@router.put("/{id_message}")
async def edit_message(
    id_message: str, edit: Message, current_user: User = Depends(get_current_user)
):
    try:
        response = messages_table.get_item(
            Key={"id_message": id_message, "id_user": current_user.sub}
        )
        item = response.get("Item", {})
        if not item:
            raise HTTPException(status_code=404, detail="Message not found")
        if item["id_user"] != current_user.sub:
            raise HTTPException(
                status_code=403, detail="Not authorized to edit this message"
            )
        if item.get("is_bot", False):
            raise HTTPException(status_code=400, detail="Cannot edit bot messages")

        messages_table.update_item(
            Key={"id_message": id_message, "id_user": current_user.sub},
            UpdateExpression="SET content = :val1",
            ExpressionAttributeValues={":val1": edit.content},
        )
        logger.info(f"Message {id_message} edited by user {current_user.username}")

        return {"id_message": id_message, "content": edit.content}
    except Exception as e:
        logger.error(f"Error editing message {id_message}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.delete("/{id_message}")
async def delete_message(
    id_message: str, current_user: User = Depends(get_current_user)
):
    try:
        id_user = current_user.sub
        response = messages_table.get_item(
            Key={"id_message": id_message, "id_user": id_user}
        )
        item = response.get("Item", {})
        if not item:
            raise HTTPException(status_code=404, detail="Message not found")
        if item["id_user"] != id_user:
            raise HTTPException(
                status_code=403, detail="Not authorized to delete this message"
            )
        if item.get("is_bot", False):
            raise HTTPException(status_code=400, detail="Cannot delete bot messages")

        messages_table.delete_item(Key={"id_message": id_message, "id_user": id_user})
        logger.info(f"Message {id_message} deleted by user {current_user.username}")

        return {"id_message": id_message, "status": "deleted"}
    except Exception as e:
        logger.error(f"Error deleting message {id_message}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
