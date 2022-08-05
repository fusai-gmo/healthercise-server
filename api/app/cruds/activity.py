from setting import session as Session
import models.user as user_model
import models.sex as sex_model
import models.commute as commute_model
import models.activity as activity_model
import models.activity_level as activity_level_model
import schemas.user
from sqlalchemy import Time
from datetime import datetime as dt
import schemas.activity as activity_schema

def get_activity_of_user(db: Session, user_id: int):
    strength_of_user = db.query(user_model.user).filter(user_model.user.id == user_id ).first().activity_level[0].level
    activity_of_user = db.query(activity_model.activity).filter(activity_model.activity.strength == strength_of_user).first()
    return activity_of_user


def create_activity(db: Session, activity: activity_schema):
    db.add(activity_model.activity(
      strength=activity.strength,
      name=activity.name,
      calory=activity.calory
    ))
    db.commit()
    return activity_model.activity(
      strength=activity.strength,
      name=activity.name,
      calory=activity.calory
    )
    
def get_recent_activity_finished(db: Session, user_id: int):
    user = db.query(user_model.user).get(user_id)
    return user.activity_log[0]
    
def update_recent_activity_finished(db: Session, user_id: int):
    user = db.query(user_model.user).get(user_id)
    user.activity_log[0].is_done = True
    db.commit()
    return user.activity_log[0]
  
def update_recent_activity_finished_bySlack(db: Session, slackId: str):
    user = db.query(user_model.user).filter(user_model.user.slack_id == slackId).first()
    user.activity_log[0].is_done = True
    db.commit()
    return user.activity_log[0]