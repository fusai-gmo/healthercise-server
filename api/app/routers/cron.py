from typing import Optional
from fastapi import APIRouter, HTTPException, Cookie, Header
import schemas.user as user_schema
import cruds.user as user_cruds
from setting import session as db

router = APIRouter()

@router.get('/cron')
async def add_new_user( id_token: Optional[str] = Cookie(None)):
    print("Called")
    pass
