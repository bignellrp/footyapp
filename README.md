# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Flask using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by installing this docker image and cloning this repo to
replace the contents of the /app folder

tiangolo/uwsgi-nginx-flask

```bash
docker pull tiangolo/uwsgi-nginx-flask
docker run -t -i -p 80:80 tiangolo/uwsgi-nginx-flask
docker exec -it flask /bin/bash
rm -rf /app
mkdir app
cd app
git clone https://github.com/bignellrp/footyapp.git .
```

This branch adds google sheets support to have the player list generated from a
google sheet. The output from the script (if admin only checkbox is checked
sends the output to another google sheet.

To test the google sheet function you need to follow this
[guide](https://developers.google.com/sheets/api/quickstart/python)
to work with the google sheets api For this you need to have the credentials
json and on the first run generate the token.pickle.

You can use [this](https://github.com/bignellrp/footyapp/blob/main/Player%20Stats.xlsx) Excel file as
a template for the stats.

Json is also required for generating the date for the closest upcoming
Wednesday (the football day)

```bash
docker exec -it flask /bin/bash
pip install -r requirements.txt
```

If you prefer not to use google for the data checkout the [static branch](https://github.com/bignellrp/footyapp/tree/static)
