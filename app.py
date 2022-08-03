import logging
import os

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from slack_sdk.web import WebClient

import os
from slack_bolt import App

# Initialize a Bolt for Python app
app_token = os.environ.get("SLACK_APP_TOKEN")
bot_token = os.environ.get("SLACK_BOT_TOKEN")
secret = os.environ.get("SLACK_SIGNING_SECRET")

channel_id = "C03RXBYEVQA"

# Initializes your Bolt app with a bot token and signing secret
app = App(
    token=bot_token,
    signing_secret=secret
)


def send_post_message():
    client = WebClient(token=bot_token)
    response = client.api_call(
        api_method='chat.postMessage',
        json={'channel': channel_id, 'text': "Hello world!"}
    )
    assert response["ok"]
    assert response["message"]["text"] == "Hello world!"

    prev_message = response['message']['text']
    response = client.conversations_history(channel=channel_id)
    print(response['messages'])


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

