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
        with open(path_to_file, 'w+') as f:
            sys.stdout = f
            print('{\n'
                +'"session": "'
                +os.urandom(24).hex()
                +'",\n'
                +'"slack_token": "",\n'
                +'"discord_token": "",\n'
                +'"discord_token_dev": "",\n'
                +'"discord_webhook": "",\n'
                +'"discord_webhook_dev": "",\n'
                +'"SPREADSHEET_ID": "",\n'
                +'"channel_id": "",\n'
                +'"channel_id_dev": "",\n'
                +'"gitbranchdev": "main",\n'
                +'"httpauth_admin"'
                +os.urandom(12)
                +'",\n'
                +'}'
                )
        with open(path_to_file, "r") as handler:
            info = json.load(handler)
    return info[value]