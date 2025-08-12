from models.chat import Global
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from models.user import User
from typing import Optional
from zoneinfo import ZoneInfo

class GlobalSchema(BaseModel):
    id: int
    message: str
    user_full_name: str
    sendet_data: str