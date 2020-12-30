# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team for each side.

Coded using Python, HTML and Flask. (HTML taken from https://startbootstrap.com/theme/grayscale)

You can test this by installing this docker image and cloning this repo to replace the contents of the /app folder

https://hub.docker.com/r/that1guy15/flask-demo

docker pull that1guy15/flask-demo
docker run -t -i -p 80:80 thatguy15/flask-demo
docker exec -it flask /bin/bash
cd /app
rm -rf *
git clone https://github.com/bignellrp/footyapp.git .

Future Plans for the app:

- Add a menu to the app for selecting different fuctions
- Make a new fuction for adding, editing or removing player stats
- Match teams with a while loop