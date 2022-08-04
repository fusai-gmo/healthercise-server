from fastapi import HTTPException
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from google.auth.transport.requests import exceptions
import os

client_id = os.getenv("GOOGLE_API_CLIENT_ID", "not set")

"""
id_tokenが正当かチェックする
"""
def verify_id_token(id_token: str):
  if id_token is None:
      raise HTTPException(status_code=401, detail="Id token is not set")
  try:
    id_info = google_id_token.verify_oauth2_token(id_token, google_requests.Request(), client_id)
  except Exception as e:
    if str(e).startswith('Token expired,'):
      raise HTTPException(status_code=401, detail="Id token is expired")
    else:
      raise HTTPException(status_code=500, detail="Unexpected error")
      
  user_info = {
    'uid': id_info['sub'],
    'email': id_info['email'],
  }
  return user_info

"""
ユーザー本人によるリクエストかチェックし、(firebaseの) user_idを返す
"""
def verify_user(id_token: str, user_id: str):
  user_info = verify_id_token(id_token)
  if user_info['uid'] != user_id:
    raise HTTPException(status_code=403, detail="Forbidden")
  return user_info

