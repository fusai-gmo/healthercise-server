from typing import Optional
from typing import List

from pydantic import BaseModel, Field

class TimeDuration(BaseModel):
    start: str = Field(None,example="2022-08-03T06:22:39.543Z")
    finish: str = Field(None,example="2022-08-03T06:22:39.543Z")


class UserBase(BaseModel):
    userName: str = Field(None, example="Mike")
    firebaseId: str = Field(None, example="012")
    email: str = Field(None, example="eaxmple.com")
    gender: str = Field(None, example="male")
    age: int = Field(0, example=18)
    height: int = Field(0, example=133, description="身長(cm)")
    weight: int = Field(0, example=200, description="体重(kg)")
    activeLevel: int = Field(0, example=1, description="身体活動レベル(1~3)")
    includeCommutingTime: Optional[bool] = Field(False, example=True, description="通勤時間を運動時間に含めるか")
    goWorkTime: TimeDuration = Field(None, deacription="通勤時間")
    leaveWorkTime: TimeDuration = Field(None, deacription="退勤時間")
    activeTime: TimeDuration = Field(None, deacription="提案をする時間")
    slackId: str = Field(None)


class UserCreate(UserBase):
    pass


class UserCreateResponse(UserCreate):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(UserBase):
    userId: str = Field(None)

class UserResponse(BaseModel):
    id: int
    userName: str = Field(None, example="Mike")
    email: str = Field(None, example="eaxmple.com")
    age: int = Field(0, example=18)
    height: int = Field(0, example=133, description="身長(cm)")
    weight: int = Field(0, example=200, description="体重(kg)")
    class Config:
        orm_mode = True
