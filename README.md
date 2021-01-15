# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Flask using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by installing this docker image and cloning this repo to
replace the contents of the /app folder

https://hub.docker.com/r/that1guy15/flask-demo

```bash
docker pull that1guy15/flask-demo
docker run -t -i -p 80:80 thatguy15/flask-demo
docker exec -it flask /bin/bash
rm -rf /app
mkdir app
cd app
git clone https://github.com/bignellrp/footyapp.git .
```

```bash
docker exec -it flask /bin/bash
pip install -r requirements.txt
```