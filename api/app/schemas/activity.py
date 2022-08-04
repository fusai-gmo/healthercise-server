from typing import Optional

from pydantic import BaseModel, Field


class Activity(BaseModel):
    strength: int = Field(None, description="強度", example="1")
    name: str = Field(None, description="種目", example="ランニング")
    calory: int = Field(None, description="消費するカロリー/h", example="30")