# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Flask using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by cloning this repo and modifying the docker-compose.yml

BRANCH = Must match the branch you are cloning e.g preprod
IPV4_ADDR = Edit the network accordingly
LOCAL_TOKENS = 3 local tokens are required for Discord, Google Sheets and Slack (see below)
Add the local folder where the tokens are saved. e.g /mnt/user/share/tokens/

```
version: '3'
services:
  footyapp:
    image: ghcr.io/bignellrp/footyapp:${BRANCH}
    container_name: footyapp-${BRANCH}
    networks:
      br0:
        ipv4_address: ${IPV4_ADDR}
    ports:
      - "80:80"
    restart: always
    environment:
      - WEB_CONCURRENCY=1
      - PYTHONUNBUFFERED=1
    volumes:
      - ${LOCAL_TOKENS}:/tokens
networks:
  br0:
    external: true
    name: br0
```

# Tokens

The secrets for this app must be loaded as a volume to /tokens and contain two files; tokens.json and keys.json
To generate the empty tokens.json use services/generate_tokens.py
To generate the keys.json follow the Google Sheets Token Guide below and import the csv data from the csv folder.

# Google Sheets Token

This branch adds google sheets support to have the player list generated from a
google sheet. Submit allows the user to push the results back to google sheets. 

The score page allows the user to update the score from that weeks game.

To test the google sheet function you need to follow this
[guide](https://www.youtube.com/watch?v=4ssigWmExak)
to work with the google sheets api. For this you need to have the credentials (keys)
json. Save the keys.json to the services folder.

If you prefer not to use google for the data checkout the [static branch](https://github.com/bignellrp/footyapp/tree/static) **Note** the static branch is now a few versions behind the latest.

# Discord Token

In the latest version of the app a Discord helper bot is included that is integrated with the Flask webapp.

A guide for creating the bot can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html)

Save the token in the tokens.json file in the services folder.

# Slack Token

The slack token is optional as by default the slack post section routes/results.py is commented out. 

If you wish to use slack to notify when the teams have been posted uncomment and add the slack token to the tokens.json