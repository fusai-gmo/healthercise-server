from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
import requests
import os

client_id = os.getenv("GOOGLE_API_CLIENT_ID", "not set")
client_secret = os.getenv("GOOGLE_API_CLIENT_SECRET", "not set")
redirect_uri = os.getenv("GOOGLE_API_REDIRECT_URI", "not set")

print(client_id, client_secret, redirect_uri)

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
