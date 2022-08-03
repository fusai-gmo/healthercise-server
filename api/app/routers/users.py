from fastapi import APIRouter, HTTPException
from typing import List
import schemas.user as user_schema
import cruds.user as user_cruds
from setting import session as db

router = APIRouter()


@router.get('/users/{userId}')
async def get_user_info(userId: int):
    print("OK")
    print("userID", userId)
    db_user = await user_cruds.get_user(db, userId)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


# @router.patch('/users/{userId}')
# async def update_user_info():
#     pass


# @router.get('/users/{userId}/achievement')
# async def get_achievement():
#     pass


# @router.get('/users/{userId}/todo/done/{taskId}')
# async def complete_task():
#     pass
