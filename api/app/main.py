from fastapi import FastAPI
from routers import user, users

app = FastAPI()
app.include_router(user.router)
app.include_router(users.router)


@app.get('/ping')
def ping():
    return 'pong!'
