from setting import session as Session
import models.user as user_model
import models.sex as sex_model
import models.commute as commute_model
import models.activity_level as activity_level_model
import schemas.user as user_schema
# from cruds.token import get_access_token
from schemas.user import UserCreate, TimeDuration
from sqlalchemy.sql import text as sql_text
from sqlalchemy import Time
from datetime import datetime as dt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json
import pprint
import os
import requests
import random
from setting import session as Session
from models.access_token import access_token as access_token_model
from sqlalchemy.sql import text as sql_text
import models.user as user_model
# from cruds.user import create_user
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

async def get_user(db: Session, user_id: int):
    user = db.query(user_model.user).get(user_id)
    if user is None:
        return None
    sex_dic={"1":"male","2":"female","3":"other"}
    
    print("user.activity_log=====================")
    print(user.activity_log)
    print("user.activity_log=====================")

    return {
        "id":user.id,
        "userName":user.name,
        "email":user.email,
        "gender": "male" if len(user.sex) == 0  else sex_dic[user.sex[0].sex],
        "age":user.age,
        "height":user.height,
        "weight":user.weight,
        "activeLevel": 1 if len(user.activity_level) == 0  else user.activity_level[0].level,
        "includeCommutingTime": False if len(user.commute) == 0  else user.commute[0].commute_is_activity,
        "slackId":user.slack_id,
        "goWorkTime":{
            "start": "08:00:00" if len(user.commute) == 0  else user.commute[0].commute_start_time,
            "finish":"09:00:00" if len(user.commute) == 0  else user.commute[0].commute_finish_time
        },
        "leaveWorkTime":{
            "start": "18:00:00" if len(user.commute) == 0  else user.commute[1].commute_start_time,
            "finish": "19:00:00" if len(user.commute) == 0 else user.commute[1].commute_finish_time
        },
        "activeTime":{
            "start":user.notify_start_time,
            "finish":user.notify_finish_time
        },
        "activity_log": user.activity_log,
        "todos":get_users_calendar(user_id),
    }

async def get_user_by_firebase_id(db: Session, firebase_id: str):
    return db.query(user_model.user).filter(user_model.user.firebase_id == firebase_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.user).filter(user_model.user.email == email).first()

def get_user_by_slackId(db: Session, slackId: str):
    return db.query(user_model.user).filter(user_model.user.slack_id == slackId).first()

def update_user(db:Session,new_user:user_schema.UserCreate, user_id):
    user = db.query(user_model.user).get(user_id)
    if user is None:
        return None
    print(user)
    user.name = new_user.userName
    user.email = new_user.email
    sex_dic={"male":1,"female":2,"other":3}
    # user.sex[0].sex = sex_dic[new_user.gender]
    user.age = new_user.age
    user.height = new_user.height
    user.weight = new_user.weight
    user.slack_id = new_user.slackId
    # user.activity_level[0].level = new_user.activeLevel
    # user.commute[0].commute_is_activity=new_user.includeCommutingTime
    # user.commute[1].commute_is_activity=new_user.includeCommutingTime
    # user.commute[0].commute_start_time = new_user.goWorkTime.start
    # user.commute[0].commute_start_time = new_user.goWorkTime.finish
    # user.commute[1].commute_start_time = new_user.leaveWorkTime.start
    # user.commute[1].commute_start_time = new_user.leaveWorkTime.finish
    db.commit()


async def create_user(db: Session, user: user_schema.UserCreate):
    new_id = False
    # User Table
    db_user = user_model.user(
        firebase_id=user.firebaseId,
        name=user.userName,
        email=user.email,
        age=user.age,
        height=user.height,
        weight=user.weight,
        notify_start_time=(dt.strptime(user.activeTime.start,"%H:%M")).time(),
        notify_finish_time=(dt.strptime(user.activeTime.finish,"%H:%M")).time(),
        slack_id=user.slackId,
    )
    db.add(db_user)
    db.commit()

    # UserId
    user_id = db_user.id

    # Sex Table
    sex_dic={"male":1,"female":2,"other":3}
    db_sex = sex_model.sex(
        user_id=user_id,
        sex=sex_dic[user.gender]
    )
    db.add(db_sex)

    # Commute Table
    db_commute = commute_model.commute(
        user_id=user_id,
        commute_start_time = (dt.strptime(user.goWorkTime.start,"%H:%M")).time(),
        commute_finish_time = (dt.strptime(user.goWorkTime.finish,"%H:%M")).time(),
        isCommute = True,
        commute_is_activity = user.includeCommutingTime
    )
    db.add(db_commute)

    db_commute2 = commute_model.commute(
        user_id=user_id,
        commute_start_time = (dt.strptime(user.leaveWorkTime.start,"%H:%M")).time(),
        commute_finish_time = (dt.strptime(user.leaveWorkTime.finish,"%H:%M")).time(),
        isCommute = False,
        commute_is_activity = user.includeCommutingTime
    )
    db.add(db_commute2)

    # Active Level Table
    db_activity_level = activity_level_model.activity_level(
        user_id = user_id,
        level = user.activeLevel
    )
    db.add(db_activity_level)
    db.commit()

    return db_user


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
  

def get_access_token(db: Session, user_id: str):
    # DBからuserのrefresh token を取得
    refresh_token = db.query(access_token_model.access_token).filter(access_token_model.access_token.user_id == user_id).all()[0].token

    # return (refresh_token)

    # POST
    data = {
        'client_id': os.environ.get('GOOGLE_API_CLIENT_ID'),
        'client_secret': os.environ.get('GOOGLE_API_CLIENT_SECRET'),
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