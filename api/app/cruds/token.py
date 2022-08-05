import random
from setting import session as Session
from models.access_token import access_token as access_token_model
from sqlalchemy.sql import text as sql_text
import models.user as user_model

def save_refresh_token(db: Session, access_token: str, firebase_id: str, user):
  if user is None:
    db_user = user_model.user(
        firebase_id=firebase_id,
        name=None,
        email=None,
        age=None,
        height=None,
        weight=None,
        notify_start_time=None,
        notify_finish_time=None,
        slack_id=None,
    )
    db.add(db_user)
    db.commit()
    
    user_id = db_user.id
  else:
    user_id = user.id

  query = sql_text("INSERT INTO access_token VALUES (:id, :user_id, :token_type_id, :token) ON DUPLICATE KEY UPDATE token = :token2")
  db.execute(query, {"id": 0, "user_id": user_id, "token_type_id": 4, "token": access_token, "token2": access_token})
  db.commit()