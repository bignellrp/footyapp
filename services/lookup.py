import json
import os
import sys
from pathlib import Path

def lookup(value):
    original_stdout = sys.stdout
    path_to_file = '../tokens/tokens.json'
    path = Path(path_to_file)

    if path.is_file():
        print(f'The file {path_to_file} exists')
        with open(path_to_file, "r") as handler:
            info = json.load(handler)
    else:
        print('Tokens do not exist. Creating tokens!')
        session = os.urandom(24).hex()
        auth = os.urandom(12)
        with open(path_to_file, 'w+') as f:
            sys.stdout = f
            dictionary = {
                'session':session, 
                'slack_token':'', 
                'discord_token':'',
                'discord_token_dev':'',
                'discord_webhook':'',
                'discord_webhook_dev':'',
                'SPREADSHEET_ID':'',
                'channel_id':'',
                'channel_id_dev':'',
                'gitbranchdev':'main',
                'httpauth_admin':auth
                }
            jsonString = json.dumps(dictionary, indent=4)
            print(jsonString)
        with open(path_to_file, "r") as handler:
            info = json.load(handler)
    return info[value]