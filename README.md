# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Flask using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by installing this docker image and cloning this repo to
replace the contents of the /app folder

[tiangolo/meinheld-gunicorn-flask](https://github.com/tiangolo/meinheld-gunicorn-flask-docker)

Using the below Dockerfile

```
FROM tiangolo/meinheld-gunicorn-flask

# set environment variables
ENV WEB_CONCURRENCY 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app
RUN mkdir /tokens
RUN /start.sh
```

or if you're using Docker on Unraid add these parameters to the "Advanced View" of the add container page.

```
Name:flaskpro
Repository: tiangolo/meinheld-gunicorn-flask
Extra Parameters: -e WEB_CONCURRENCY="1" -e PYTHONUNBUFFERED="1"
Post Arguments: ;sleep 2;docker start flaskpro;sleep 2;docker exec flaskpro bash -c "sleep 5;rm -rf /app/*;cd /app;git clone https://github.com/bignellrp/footyapp.git .;pip3 install -r requirements.txt";docker restart flaskpro
Tokens(Custom Folder): Container Path: /tokens
```

The score page allows the user to update the score from that weeks game.

In the latest version of the app a Discord helper bot is included that is integrated with the Flask webapp.

A guide for creating the bot can be found [here](https://discordpy.readthedocs.io/en/stable/discord.html)

Save the token in the tokens.json file in the services folder.