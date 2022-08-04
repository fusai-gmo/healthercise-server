from fastapi import APIRouter, HTTPException, Cookie
from typing import List, Optional
import schemas.user as user_schema
import cruds.user as user_cruds
from setting import session as db
from auth.id_token import verify_user

router = APIRouter()


@router.get('/users/{userId}')
async def get_user_info(userId: str, id_token: Optional[str] = Cookie(None)):
    verify_user(id_token, userId)
    
    db_user = await user_cruds.get_user(db, userId)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user

@router.patch('/users/{userId}')
async def update_user_info(userId: int, user: user_schema.UserCreate, id_token: Optional[str] = Cookie(None)):
    await verify_user(id_token, userId)

    db_user = await user_cruds.get_user(db, userId)
    # if not db_user:
    #     raise HTTPException(status_code=400, detail="User not found")
    return user_cruds.update_user(db, user, userId)

# @router.get('/users/{userId}/achievement')
# async def get_achievement():
#     pass


# @router.get('/users/{userId}/todo/done/{taskId}')
# async def complete_task():
#     pass
