from fastapi import APIRouter, HTTPException, Cookie
from typing import List, Optional
import schemas.user as user_schema
import cruds.user as user_cruds
from setting import session as db
from auth.id_token import verify_user
from cruds.activity import create_activity, get_activity_of_user
import datetime
import pandas as pd


router = APIRouter()

def calc_bmr(user: dict):
    men_bmr = (0.0481*user["weight"]+0.0234*user["height"]-0.0138*user["age"]-0.4235)*1,000/4.186
    women_bmr = (0.0481*user["weight"]+0.0234*user["height"]-0.0138*user["age"]-0.9708)*1,000/4.186
    other_bmr = (men_bmr+women_bmr)/2
    
    bmr_dic = {"men": men_bmr, "women": women_bmr, "other": other_bmr}
    return bmr_dic[user["gender"]]

def get_active_level(user: dict):
    active_level = {
        "1or2": {"1": 1, "2": 1.35, "3": 1},
        "3to5": {"1": 1, "2": 1.45, "3": 1},
        "6or7": {"1": 1.35, "2": 1.55, "3": 1.75},
        "8or9": {"1": 1.40, "2": 1.60, "3": 1.80},
        "10or11": {"1": 1.45, "2": 1.65, "3": 1.85},
        "12to14": {"1": 1.50, "2": 1.70, "3": 1.90},
        "15to17": {"1": 1.55, "2": 1.75, "3": 1.95},
        "18to29": {"1": 1.50, "2": 1.75, "3": 2.00},
        "30to49": {"1": 1.50, "2": 1.75, "3": 2.00},
        "50to64": {"1": 1.50, "2": 1.75, "3": 2.00},
        "65to74": {"1": 1.45, "2": 1.70, "3": 1.95},
        "upto75": {"1": 1.40, "2": 1.65, "3": 1.00},
    }
    if user["age"] >= 75:
        return active_level["upto75"][user["activeTable"]]
    elif user["age"] >= 65:
        return active_level["65to74"][user["activeTable"]]
    elif user["age"] >= 50:
        return active_level["50to64"][user["activeTable"]]
    elif user["age"] >= 30:
        return active_level["30to49"][user["activeTable"]]
    elif user["age"] >= 18:
        return active_level["18to29"][user["activeTable"]]
    elif user["age"] >= 15:
        return active_level["15to17"][user["activeTable"]]
    elif user["age"] >= 12:
        return active_level["12to14"][user["activeTable"]]
    elif user["age"] >= 10:
        return active_level["10or11"][user["activeTable"]]
    elif user["age"] >= 8:
        return active_level["8or9"][user["activeTable"]]
    elif user["age"] >= 6:
        return active_level["6or7"][user["activeTable"]]
    elif user["age"] >= 3:
        return active_level["3to5"][user["activeTable"]]
    else:
        return active_level["1to2"][user["activeTable"]]


def calc_ideal_calorie(user: dict):
    bmr = calc_bmr(user)
    return bmr*get_active_level(user["activeLevel"])


def calc_consumption_calorie(user: dict):
    ideal_calorie = calc_ideal_calorie(user)
    if not user["includeCommutingTime"]:
        return ideal_calorie
    
    #TODO commute_excersize_time: hour
    #TODO 3.5 * user["weight"] * hour * 1.05
    commute_excersize_time = abs(user["goWorkTime"]["end"]-user["goWorkTime"]["start"])+abs(user["leaveWorkTime"]["end"]-user["leaveWorkTime"]["start"])      
    commute_consumption_calorie = 3.5 * user["weight"] * commute_excersize_time * 1.05
    return ideal_calorie-commute_consumption_calorie


def compare_time(time1: datetime, time2: datetime):
    return time1 == time2

def recommend_activity_schedule(user: dict):
    consumptin_calorie = calc_consumption_calorie(user)
    recommend_activity = get_activity_of_user(db=db, user_id=user["id"])

    hour = consumptin_calorie / recommend_activity["calorie"]

    dt_list = pd.date_range(start=user["activeTime"], periods=30, freq='30min')
    for dt in dt_list:
        compare_time(user["goWorkTime"], dt)
        compare_time(user["goWorkTime"], dt+hour) 
    # TODO Google CalenderAPI から予定を取得
    # Activity log Table (Start, End, calorie)
    create_activity(db, activity=recommend_activity)


@router.get('/users/{userId}')
async def get_user_info(userId: str, id_token: Optional[str] = Cookie(None)):
    verify_user(id_token, userId)
    
    db_user = await user_cruds.get_user(db, userId)

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user

@router.patch('/users/{userId}')
async def update_user_info(userId: int, user: user_schema.UserCreate, id_token: Optional[str] = Cookie(None)):
    await verify_user(id_token, userId)

    db_user = await user_cruds.get_user(db, userId)
    # if not db_user:
    #     raise HTTPException(status_code=400, detail="User not found")
    return user_cruds.update_user(db, user, userId)

@router.get('/users/{userId}/today')
async def get_user_activity_schedule(userId: int):
    db_user = await user_cruds.get_user(db, userId)

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return {"recommend_activity_schedule": recommend_activity_schedule(db_user)}

@router.get('/users/{userId}/consumption')
async def get_user_consumption_calorie(userId: int):
    db_user = await user_cruds.get_user(db, userId)

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return {"consumption_calorie": calc_consumption_calorie(db_user)}

@router.get('/users/{userId}/calorie')
async def get_user_ideal_calorie(userId: int):
    db_user = await user_cruds.get_user(db, userId)

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return {"ideal_calorie": get_user_ideal_calorie(db_user)}
# @router.get('/users/{userId}/achievement')
# async def get_achievement():
#     pass


# @router.get('/users/{userId}/todo/done/{taskId}')
# async def complete_task():
#     pass

