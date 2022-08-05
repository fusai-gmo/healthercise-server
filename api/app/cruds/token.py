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