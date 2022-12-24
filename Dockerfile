#Dev container
FROM tiangolo/meinheld-gunicorn-flask AS devcontainer

ENV WEB_CONCURRENCY 1
ENV PYTHONUNBUFFERED 1

COPY poststart.sh /tmp/poststart.sh
RUN chmod +x  /tmp/poststart.sh

RUN mkdir -p /workspaces/tokens

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt




#Build step
FROM devcontainer AS build

RUN rm -rf /workspaces && mkdir /tokens
COPY . /app
WORKDIR /app
ENTRYPOINT /tmp/poststart.sh