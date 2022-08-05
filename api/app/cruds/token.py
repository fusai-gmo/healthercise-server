import random
from setting import session as Session
from models.access_token import access_token as access_token_model
from sqlalchemy.sql import text as sql_text
import models.user as user_model
from cruds.user import create_user
from schemas.user import UserCreate, TimeDuration
import models.sex as sex_model
import models.commute as commute_model
import models.activity as activity_model
import models.access_token as access_token_model
import models.activity_level as activity_level_model
import schemas.user
from setting import session as db
from sqlalchemy import Time
from datetime import datetime as dt
from datetime import timedelta
import schemas.activity as activity_schema
import json
import pprint
import os
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_access_token(db: Session, user_id: str):
    # DBからuserのrefresh token を取得
    refresh_token = db.query(access_token_model.access_token).filter(access_token_model.access_token.user_id == user_id).all()[0].token

    # return (refresh_token)

    # POST
    data = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'redirect_uri': 'https://api.healthercise.k1h.dev/refresh_token',
        'grant_type': 'refresh_token',
        'access_type': 'offline',
        'refresh_token': refresh_token
    }
    url = 'https://www.googleapis.com/oauth2/v4/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post(url, data=data, headers=headers)
    pprint.pprint('1--------------------------------------')
    pprint.pprint(res.json())
    pprint.pprint('--------------------------------------')
    data['access_token'] = res.json().get('access_token', None)
    return data


def get_users_calendar(user_id: str):
  
    data = get_access_token(db=db, user_id=user_id)
  
    file_path = 'code/'+ data['client_id']+'.json'
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    creds = Credentials.from_authorized_user_file(file_path, ['https://www.googleapis.com/auth/calendar'])
    service = build('calendar', 'v3', credentials=creds)
    now = dt.utcnow()
    events_result = service.events().list(calendarId='primary', timeMin=now.isoformat() + 'Z', timeMax = (now + timedelta(days=1)).isoformat() + 'Z',
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events

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