from fastapi import APIRouter, HTTPException
import schemas.activity as activity_schema
import cruds.activity as activity_cruds
from setting import session as db

router = APIRouter()

@router.get('/activity/{userId}')
async def detect_user_activity(userId: int):
    return activity_cruds.get_activity_of_user(db=db, user_id = userId)


@router.post('/activity')
async def create_new_activity(activity: activity_schema.Activity):
    return activity_cruds.create_activity(db=db,activity=activity)

@router.get('/activity/{userId}/recent')
async def get_recent_user_activity(userId: int):
    return activity_cruds.get_recent_activity_finished(db=db,user_id=userId)

@router.patch('/activity/{userId}/done')
async def get_recent_user_activity(userId: int):
    return activity_cruds.update_recent_activity_finished(db=db,user_id=userId)

@router.patch('/activity/{slackId}/slack')
async def get_recent_user_activity(slackId: str):
    return activity_cruds.update_recent_activity_finished_bySlack(db,slackId)
