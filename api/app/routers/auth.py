from typing import Optional
from fastapi import APIRouter, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
import requests
import os

client_id = os.getenv("GOOGLE_API_CLIENT_ID", "not set")
client_secret = os.getenv("GOOGLE_API_CLIENT_SECRET", "not set")
redirect_uri = os.getenv("GOOGLE_API_REDIRECT_URI", "not set")

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
      raise HTTPException(status_code=500, detail="Something goes wrong.")

    data = res.json()

    print(data)
    
    refresh_token = data['refresh_token']
    id_token = data['id_token']
    # access_token = data['access_token']

    # TODO: save refresh_token to db

    response = RedirectResponse(url='http://localhost:3000/profile')
    response.set_cookie(key="id_token", value=id_token, httponly=True, secure=True)

    return response

@router.get('/auth/me')
def auth_me(id_token: Optional[str] = Cookie(None)):
    if id_token is None:
        raise HTTPException(status_code=403, detail="Id token is not set")
    
    id_info = google_id_token.verify_oauth2_token(id_token, google_requests.Request(), client_id)
    user_id = id_info['sub']
    
    # TODO: fetch user data from db.
    
    return user_id