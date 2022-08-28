import os
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