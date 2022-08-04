from fastapi import APIRouter, HTTPException
import schemas.activity as activity_schema
import cruds.activity as activity_cruds
from setting import session as db

router = APIRouter()

@router.post('/activity')
async def add_new_user(activity: activity_schema.Activity):
    return activity_cruds.create_activity(db=db,activity=activity)