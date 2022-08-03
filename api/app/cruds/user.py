from setting import session as Session
import models.user as user_model
import models.sex as sex_model
import models.commute as commute_model
import models.activity_level as activity_level_model
import schemas.user
from sqlalchemy import Time
from datetime import datetime as dt

async def get_user(db: Session, user_id: int):
    output = {}
    user = db.get(user_model.user, user_id)
    sex = db.get(sex_model.sex, user_id)
    commute = db.get(commute_model.commute, user_id)
    go_commute = db.query(commute_model.commute).filter(commute_model.commute.isCommute == True)
    leave_commute = db.query(commute_model.commute).filter( mute_model.commute.isCommute == True)
    activity_level = db.get(activity_level_model.activity_level,user_id)
    return {
        "userName": user.name,
        "email": user.email,
        "gender": sex.sex,
        "age": user.age,
        "height": user.height,
        "weight": user.weight,
        "activeLevel": activity_level.level,
        "includeCommutingTime": go_commute.commute_is_activity,
        "goWorkTime": {
            "start":go_commute.commute_start_time,
            "finish":go_commute.commute_finish_time,
        },
        "leaveWorkTime":
        {
            "start":go_commute.commute_start_time,
            "finish":go_commute.commute_finish_time,
        },
        "slackId": "NONE"
    }

def get_user_by_email(db: Session, email: str):
    # return db.query(user_model.user).filter(user_model.user.email == email).first()
    pass

def create_user(db: Session, user: schemas.user.UserCreate):
    new_id = False
    # User Table
    db_user = user_model.user(
        name=user.userName,
        email=user.email,
        age=user.age,
        height=user.height,
        weight=user.weight
    )
    print(db.query(user_model.user))
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

    # Commute Table
    db_commute = commute_model.commute(
        user_id=user_id,
        commute_start_time = (dt.strptime(user.goWorkTime.start,"%H:%M")).time(),
        commute_finish_time = (dt.strptime(user.goWorkTime.finish,"%H:%M")).time(),
        isCommute = True,
        commute_is_activity = user.includeCommutingTime
    )
    db.add(db_commute)
    db.commit()

    db_commute = commute_model.commute(
        user_id=user_id,
        commute_start_time = (dt.strptime(user.goWorkTime.start,"%H:%M")).time(),
        commute_finish_time = (dt.strptime(user.goWorkTime.finish,"%H:%M")).time(),
        isCommute = False,
        commute_is_activity = user.includeCommutingTime
    )
    db.add(db_commute)
    db.commit()

    # Active Level Table
    db_activity_level = activity_level_model.activity_level(
        user_id = user_id,
        level = user.activeLevel
    )
    db.add(db_activity_level)
    db.commit()

    return db_user
