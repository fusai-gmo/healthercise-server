from typing import Optional
from fastapi import APIRouter, HTTPException, Cookie, Header
import schemas.user as user_schema
import cruds.user as user_cruds
from setting import session as db

router = APIRouter()

@router.post('/user')
async def add_new_user(user: user_schema.UserCreate, id_token: Optional[str] = Cookie(None)):
    if id_token is None:
      raise HTTPException(status_code=403, detail="Id token is not set")
    db_user = user_cruds.get_user_by_email(db, email=user.email)
    # Emailが登録済みの場合はエラーを返す
    if db_user == '{}':
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_cruds.create_user(db=db,user=user)


@router.get('/user/getId/{slackId}')
async def get_slack_id():
    pass
