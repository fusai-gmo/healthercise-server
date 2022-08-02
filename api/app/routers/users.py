from fastapi import APIRouter
from typing import List
import schemas.user as user_schema

router = APIRouter()


@router.get('/users/{userId}', response_model=List[user_schema.UserCreateResponse])
async def get_user_info(userId: str):
    return [user_schema.UserCreateResponse(
        id=int(userId),
        userName="Koichi",
        gender="male",
        age=13,
        height=130,
        weight=130,
        activeLevel=3,
        commutingTime=13,
        includeCommutingTime=True
    )]


@router.patch('/users/{userId}')
async def update_user_info():
    pass


@router.get('/users/{userId}/achievement')
async def get_achievement():
    pass


@router.get('/users/{userId}/todo/done/{taskId}')
async def complete_task():
    pass
