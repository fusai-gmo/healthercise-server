from setting import session as Session
import models.user as user_model
import models.sex as sex_model
import models.commute as commute_model
import models.activity_level as activity_level_model
import schemas.user as user_schema
# import cruds.token as token_crud
from sqlalchemy import Time
from datetime import datetime as dt

async def get_user(db: Session, user_id: int):
    user = db.query(user_model.user).get(user_id)
    if user is None:
        return None
    sex_dic={"1":"male","2":"female","3":"other"}

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
        "todos":token_crud.get_users_calendar(user_id),
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
    user.sex[0].sex = sex_dic[new_user.gender]
    user.age = new_user.age
    user.height = new_user.height
    user.weight = new_user.weight
    user.slack_id = new_user.slackId
    user.activity_level[0].level = new_user.activeLevel
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