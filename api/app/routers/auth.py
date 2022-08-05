from typing import Optional
from fastapi import APIRouter, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from auth.id_token import verify_id_token
from cruds.user import get_user_by_firebase_id
from setting import session as db
from cruds.user import save_refresh_token
import requests
import os

client_id = os.getenv("GOOGLE_API_CLIENT_ID", "not set")
client_secret = os.getenv("GOOGLE_API_CLIENT_SECRET", "not set")
redirect_uri = os.getenv("GOOGLE_API_REDIRECT_URI", "not set")
app_redirect_uri = os.getenv("APP_REDIRECT_URI", "not set")


router = APIRouter()

@router.get('/auth/callback')
async def auth_callback(code: str = ''):
    url = 'https://accounts.google.com/o/oauth2/token'
    payload = {
      'code': code,
      'client_id': client_id,
      'client_secret': client_secret,
      'redirect_uri': redirect_uri,
      'grant_type': 'authorization_code',
    }
    print(payload)

    res = requests.post(url, json = payload)

    if res.status_code != 200:
      print(res)
      raise HTTPException(status_code=500, detail="Something goes wrong.")

    data = res.json()
    
    id_token = data['id_token']
    # access_token = data['access_token']
    id_info = google_id_token.verify_oauth2_token(id_token, google_requests.Request(), client_id)
    user = await get_user_by_firebase_id(db, id_info['sub'])
    print(id_info)
    
    if user is not None:
      user.email = id_info['email']
    
    if 'refresh_token' in data:
      refresh_token = data['refresh_token']
      await save_refresh_token(db, refresh_token, id_info['sub'], user)

    response = RedirectResponse(url=app_redirect_uri)
    response.set_cookie(key="id_token", value=id_token, httponly=True, secure=True)

    return response

@router.get('/auth/me')
async def auth_me(id_token: Optional[str] = Cookie(None)):
    user_info = verify_id_token(id_token)
    user_id = user_info['uid']
    res = await get_user_by_firebase_id(db, user_id)
    if res is None:
      raise HTTPException(status_code=404, detail="User not found")
    return res