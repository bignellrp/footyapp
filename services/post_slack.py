import json
from slack import WebClient
from services.lookup import lookup

# path_to_token = "./services/tokens.json"
# with open(path_to_token, "r") as handler:
#     info = json.load(handler)
# slack_token = info["slack_token"]
slack_token = lookup("slack_token")
client = WebClient(token=slack_token)

def _message_slack_channel(text):
    '''Sends a slack message to the footy channel'''
    print("Slack Message Sent!")
    return client.chat_postMessage(channel="footy", text=text)