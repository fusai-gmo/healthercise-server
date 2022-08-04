from fastapi import FastAPI
from routers import user, users, activity
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

import schemas

Base.metadata.create_all(bind=ENGINE, checkfirst=True)

app = FastAPI()
app.include_router(user.router)
app.include_router(users.router)
app.include_router(activity.router)

"""
Ping :　応答確認用
"""

@app.get('/ping')
def ping():
    return 'pong!'
