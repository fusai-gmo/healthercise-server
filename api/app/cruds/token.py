import random
from setting import session as Session
from models.access_token import access_token as access_token_model
from sqlalchemy.sql import text as sql_text
import models.user as user_model
from cruds.user import create_user
from schemas.user import UserCreate, TimeDuration

async def save_refresh_token(db: Session, access_token: str, firebase_id: str, user):
  if user is None:
    user_create = UserCreate(
      userName=None,
      firebaseId=firebase_id,
      email=None,
      gender="male",
      age=20,
      height=180,
      weight=65,
      activeLevel=1,
      includeCommutingTime=False,
      goWorkTime=TimeDuration(
        start="09:00",
        finish="10:00",
      ),
      leaveWorkTime=TimeDuration(
        start="18:00",
        finish="19:00",
      ),
      activeTime=TimeDuration(
        start="10:00",
        finish="19:00",
      ),
      slackId=None,
    )
    
    res = await create_user(db, user_create)
    
    user_id = res.id

  else:
    user_id = user.id

  query = sql_text("INSERT INTO access_token VALUES (:id, :user_id, :token_type_id, :token) ON DUPLICATE KEY UPDATE token = :token2")
  db.execute(query, {"id": 0, "user_id": user_id, "token_type_id": 1, "token": access_token, "token2": access_token})
  db.commit()