from typing import Optional

from fastapi import FastAPI, APIRouter, HTTPException, Cookie, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import user, users, activity, auth
import cruds

from setting import session, ENGINE, Base

# モデル読み込み
import models.user
import models.sex
import models.commute
import models.activity_level
import models.token_type
import models.access_token
import models.activity_log
import models.activity_summary
import cruds.activity as activity_cruds
from setting import session as db
from fastapi.middleware.cors import CORSMiddleware

import schemas

Base.metadata.create_all(bind=ENGINE, checkfirst=True)

app = FastAPI()
app.include_router(user.router)
app.include_router(users.router)
app.include_router(activity.router)
app.include_router(auth.router)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
Ping : 応答確認用
"""

@app.get('/ping')
def ping():
    return 'pong!'
