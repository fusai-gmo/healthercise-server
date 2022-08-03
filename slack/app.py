import logging
import os
import re

from urllib import parse

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import os
from slack_bolt import App

# Initialize a Bolt for Python app
app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")
secret = os.environ.get("SLACK_SIGNING_SECRET")

# Initializes your Bolt app with a bot token and signing secret
app = App(
    token=bot_token,
    signing_secret=secret
)


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


# Start your app
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()

