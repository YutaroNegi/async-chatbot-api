from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.auth import get_current_user

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
    dependencies=[Depends(get_current_user)],
)


class Message(BaseModel):
    content: str


@router.post("/")
async def send_message(message: Message):
    # Implement message sending logic here
    return {"message": message.content}


@router.put("/{message_id}")
async def edit_message(message_id: int, new_content: str):
    # Implement message editing logic here
    return {"message_id": message_id, "new_content": new_content}


@router.delete("/{message_id}")
async def delete_message(message_id: int):
    # Implement message deletion logic here
    return {"message_id": message_id, "status": "deleted"}
