from typing import Optional

from fastapi import FastAPI, APIRouter, HTTPException, Cookie, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from routers import user, users, activity, auth, cron
import cruds

from setting import session, ENGINE, Base

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from urllib import parse

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
import cruds.user as user_cruds
from setting import session as db
from fastapi.middleware.cors import CORSMiddleware

import schemas

Base.metadata.create_all(bind=ENGINE, checkfirst=True)

# Slack

bot = App()
bot_handler = SlackRequestHandler(bot)

# @bot.event("message")
# def welcome_message(event, say):
#     print(event)
@bot.message(r"register|Register")
def show_help(event, say):
    if event["channel_type"] != "im":
        pass
    user_id = event["user"]
    query_param = parse.urlencode(
        [
            ("userid", user_id),
        ]
    )
    healthercise_url = f'https://healthercise.k1h.dev/login?{query_param}'
    text = f"Welcome Message, <@{user_id}>! 🎉 Please access below link to use Healthercise.\n{healthercise_url}"
    say(text=text)


@bot.message(r"Help|help")
def show_help(event, say):
    user_id = event["user"]
    text = '''
    These are possible messages to use with SlackBotTest.

    Messages:
    Help or help:    Show possible commands.
    Init or init:    Get register link of Healthercise.
    Finish or finish: Report whether exercise or not.
    '''.format(user_id=user_id)
    say(text=text)


@bot.message(r"Init|init")
@bot.event("im_created")
def ask_for_login(event, say):
    user_id = event["user"]
    query_param = parse.urlencode(
        [
            ("userid", user_id),
        ]
    )
    healthercise_url = f'https://healthercise.k1h.dev/login?{query_param}'
    text = f"Welcome to the team, <@{user_id}>! 🎉 Please access below link to use Healthercise.\n{healthercise_url}"
    say(text=text)


@bot.message(r"Finish|finish")
def finish_report(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hi <@{message['user']}>!\nDo you complete today's exercise?"},
                "accessory":
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Yes"},
                        "action_id": "button_click_yes",
                    },
            },
            # {
            #     "type": "section",
            #     "text": {"type": "mrkdwn", "text": f"Hi <@{message['user']}>!\nDo you complete today's exercise?"},
            #     "accessory":
            #         {
            #             "type": "button",
            #             "text": {"type": "plain_text", "text": "No"},
            #             "action_id": "button_click_no",
            #         },
            # },
        ],
        text=f"Hey there <@{message['user']}>!",
    )


# Listens to incoming messages that contain "hello"
# To learn available listener method arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@bot.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click",
                },
            }
        ],
        text=f"Hey there <@{message['user']}>!",
    )


@bot.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@bot.action("button_click_yes")
async def action_button_yes_click(body, ack, say):
    # Acknowledge the action
    ack()
    activity_cruds.update_recent_activity_finished_bySlack(db,body['user']['id'])
    say(f"Nice, <@{body['user']['id']}>! Congraturations!!")


@bot.action("button_click_no")
def action_button_no_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"Ok, <@{body['user']['id']}>. Please try next action!!")

# Fast API

app = FastAPI()
app.include_router(user.router)
app.include_router(users.router)
app.include_router(activity.router)
app.include_router(auth.router)
app.include_router(cron.router)

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

@app.post("/slack/events")
async def endpoint(req: Request):
    print(req)
    return await bot_handler.handle(req)