from routers import user, users

from urllib import parse
import os

from slack_bolt import App
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi import SlackRequestHandler

api = FastAPI()
api.include_router(user.router)
api.include_router(users.router)

@api.get('/')
def hello():
    return "Hello, World!!"


@api.get('/ping')
def ping():
    return 'pong!'


# Initialize a Bolt for Python app
app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")
secret = os.environ.get("SLACK_SIGNING_SECRET")

# Initializes your Bolt app with a bot token and signing secret
app = App(
    token=bot_token,
    signing_secret=secret
)


@app.message(r"Help|help")
def show_help(event, say):
    user_id = event["user"]
    text = '''
    These are possible messages to use with SlackBotTest.

    Messages:
    Help or help:      Show possible commands.
    Init or init:      Get register link of Healthercise.
    Finish or finish:  Report whether exercise or not.
    '''.format(user_id=user_id)
    say(text=text)


@app.message(r"Init|init")
@app.event("im_created")
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


@app.message(r"Finish|finish")
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
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hi <@{message['user']}>!\nDo you complete today's exercise?"},
                "accessory":
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "No"},
                        "action_id": "button_click_no",
                    },
            },
        ],
        text=f"Hey there <@{message['user']}>!",
    )


# Listens to incoming messages that contain "hello"
# To learn available listener method arguments,
# visit https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("hello")
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


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.action("button_click_yes")
def action_button_yes_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"Nice, <@{body['user']['id']}>! Congraturations!!")


@app.action("button_click_no")
def action_button_no_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"Ok, <@{body['user']['id']}>. Please try tomorrow!!")


# Start your app
# if __name__ == "__main__":
#     handler = SocketModeHandler(app, app_token)
#     handler.start()

handler = SlackRequestHandler(app)


@api.post("/slack/events")
async def endpoint(request: Request):
    # handler runs App's dispatch method
    return await handler.handle(request)

# uvicorn app:api --reload --port 3000 --log-level warning
