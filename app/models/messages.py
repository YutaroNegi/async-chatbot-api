from pydantic import BaseModel
from typing import List
from datetime import datetime


class MessageTableItem(BaseModel):
    id_message: str
    id_user: str
    content: str
    timestamp: str
    is_bot: bool


class MessageTableList(BaseModel):
    messages: List


class MessagePayload(BaseModel):
    content: str
