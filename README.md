# footyapp

A web app for managing a 5 a side footy team.

Select the players using the checkboxes and it should output a balanced team
for each side.

Coded using Python, HTML and Flask using
[grayscale bootstrap template](https://startbootstrap.com/theme/grayscale)

You can test this by cloning this repo and modifying the docker-compose.yml

IPV4_ADDR = Edit the network accordingly

```
version: '3'
services:
  footyapp:
    image: ghcr.io/bignellrp/footyapp:static
    container_name: footyapp-static
    networks:
      br0:
        ipv4_address: ${IPV4_ADDR}
    ports:
      - "80:80"
    restart: always
    environment:
      - WEB_CONCURRENCY=1
      - PYTHONUNBUFFERED=1
networks:
  br0:
    external: true
    name: br0
```