from fastapi import APIRouter

router = APIRouter()


@router.post('/user')
async def add_new_user():
    pass


@router.get('/user/getId/{slackId}')
async def get_slack_id():
    pass
