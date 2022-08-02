from typing import Optional

from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str = Field(None, description="タスクID", example="13444")
    event: str = Field(None, description="実施する種目", example="ランニング")
    startTime: str = Field(None, description="タスクの開始時刻", example="2022-08-02T07:12:13.152Z")
    duration: int = Field(0, description="タスクの時間", example=30)
    isFinished: bool = Field(False, description="タスクが終了したか", example=True)
    calorie: int = Field(0, description="運動によって消費するカロリー(kcal)", example=10)


class CompleteTask(BaseModel):
    id: str = Field(None, description="タスクID", example="13444")
