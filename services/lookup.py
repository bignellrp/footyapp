import json
from pathlib import Path
import secrets

path_to_file = '../tokens/tokens.json'
path = Path(path_to_file) #Used for checking the file exists

def lookup(value):
    if path.is_file():
        print(f'The file {path_to_file} exists')
        with open(path_to_file, "r") as handler:
            info = json.load(handler)
    else:
        print('Tokens do not exist. Creating tokens!')
        session = secrets.token_urlsafe(24)
        auth = secrets.token_urlsafe(12)
        with open(path_to_file, "a+") as handler:
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
                'git_branch':'main',
                'httpauth_admin':auth
                }
            jsonString = json.dumps(dictionary, indent=4) #Format the dict into json
            handler.write(jsonString) #Write json to file
            handler.seek(0) #Move cursor back to the top once written
            info = json.load(handler) #Read requried json value into info
    return info[value]