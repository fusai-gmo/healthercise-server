import logging
import os
import re
from datetime import datetime

from urllib import parse
import pprint

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


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
    if event['channel_type'] != "im":
        return
    text = '''
    These are possible messages to use with SlackBotTest.

    Messages:
    Help or help:        Show possible commands.
    Init or init:        Get register link of Hefalthercise.
    Finish or finish:    Report finish exercise or not.
    '''.format(user_id=user_id)
    say(text=text)


@app.message(r"Init|init")
def ask_for_login(event, say):
    user_id = event["user"]
    if event['channel_type'] != "im":
        return
    query_param = parse.urlencode(
        [
            ("userid", user_id),
        ]
    )
    healthercise_url = f'https://healthercise.k1h.dev/login?{query_param}'
    text = f"Welcome to the team, <@{user_id}>! 🎉 Please access below link to use Healthercise.\n{healthercise_url}"
    say(text=text)


@app.message(r"Finish|finish")
def finish_report(event, say):
    user = event['user']
    if event['channel_type'] != "im":
        return
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hi <@{user}>!\nDo you complete today's exercise?"},
                "accessory":
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Yes"},
                        "action_id": "button_click_yes",
                    },
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hi <@{user}>!\nDo you complete today's exercise?"},
                "accessory":
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "No"},
                        "action_id": "button_click_no",
                    },
            },
        ],
        text=f"Hey there <@{user}>!",
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


def socket_server():
    handler = SocketModeHandler(app, app_token)
    handler.start()


# Start your app
if __name__ == "__main__":
    handler = SocketModeHandler(app, app_token)
    handler.start()
