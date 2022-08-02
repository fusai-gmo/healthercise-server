from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    userName: str = Field(None, example="Mike")
    gender: str = Field(None, example="male")
    age: int = Field(0, example=18)
    height: int = Field(0, example=133, description="身長(cm)")
    weight: int = Field(0, example=200, description="体重(kg)")
    activeLevel: int = Field(0, example=1, description="身体活動レベル(1~3)")
    commutingTime: int = Field(0, example=13, description="通勤時間(分)")
    includeCommutingTime: Optional[bool] = Field(False, example=True, description="通勤時間を運動時間に含めるか")


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    userId: str = Field(None)
    slackId: str = Field(None)
