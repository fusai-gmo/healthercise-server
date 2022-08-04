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