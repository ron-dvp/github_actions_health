from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import sys
import os 

slack_token = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=slack_token)


def send_message(info):
    try:
        client.chat_postMessage(
            channel=os.environ['CHANNEL_ID'],
            text=info
        )
    except SlackApiError as e:
        sys.stdout.write(f'[-] SLACK ERR: {e}\n')
        # You will get a SlackApiError if "ok" is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
