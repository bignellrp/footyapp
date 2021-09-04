# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Flask using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by installing this docker image and cloning this repo to
replace the contents of the /app folder

tiangolo/meinheld-gunicorn-flask

```bash
docker pull tiangolo/meinheld-gunicorn-flask
docker run -t -i -e WEB_CONCURRENCY="1" -p 80:80 tiangolo/meinheld-gunicorn-flask
docker exec -it flask /bin/bash
rm -rf /app
mkdir app
cd app
git clone https://github.com/bignellrp/footyapp.git .
python3 services/generate_tokens.py > services/tokens.json
pip3 install -r requirements.txt
```

or if you're using Docker on Unraid add these parameters to the "Advanced View" of the add container page.

```
Repository: tiangolo/meinheld-gunicorn-flask
Extra Parameters: -e WEB_CONCURRENCY="1"
Post Arguments: ;sleep 2;docker start flaskdev3;sleep 2;docker exec flaskdev3 bash -c "sleep 5;rm -rf /app/*;cd /app;git clone https://github.com/bignellrp/footyapp.git .;git checkout pre;python3 services/generate_tokens.py > /tokens/tokens.json;pip3 install -r requirements.txt";docker restart flaskdev3
Tokens(Custom Folder): Container Path: /tokens
```

This branch adds google sheets support to have the player list generated from a
google sheet. Submit allows the user to push the results back to google sheets. 

The score page allows the user to update the score from that weeks game.

To test the google sheet function you need to follow this
[guide](https://www.youtube.com/watch?v=4ssigWmExak)
to work with the google sheets api. For this you need to have the credentials (keys)
json. Save the keys.json to the services folder.

If you prefer not to use google for the data checkout the [static branch](https://github.com/bignellrp/footyapp/tree/static)

In the latest version of the app a Discord helper bot is included that is integrated with the Flask webapp.

A guide for creating the bot can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html)

Save the token in the tokens.json file in the services folder.