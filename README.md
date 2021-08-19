# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Quart using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by installing this docker image and cloning this repo to
replace the contents of the /app folder

tiangolo/uwsgi-nginx-flask

```bash
docker pull tiangolo/uwsgi-nginx-flask
docker run -t -i -p 80:80 tiangolo/uwsgi-nginx-flask
docker exec -it flask /bin/bash
apt-get update; apt-get install ca-certificates
rm -rf /app
mkdir app
cd app
git clone https://github.com/bignellrp/footyapp.git .
python3 services/generate_pass.py > config.py
pip3 install -r requirements.txt
```

This branch adds google sheets support to have the player list generated from a
google sheet. Submit allows the user to push the results back to google sheets. The score page allows the user to update the score from that weeks game.

To test the google sheet function you need to follow this
[guide](https://www.youtube.com/watch?v=4ssigWmExak)
to work with the google sheets api. For this you need to have the credentials (keys)
json.

You can use [this](https://github.com/bignellrp/footyapp/blob/main/Player%20Stats.xlsx) Excel file as
a template for the stats.

If you prefer not to use google for the data checkout the [static branch](https://github.com/bignellrp/footyapp/tree/static)

Or for testing hash the googleapi get commands and import the panda raw data from player_data.py and results_data.py