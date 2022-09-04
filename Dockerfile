FROM tiangolo/meinheld-gunicorn-flask

# set environment variables
ENV WEB_CONCURRENCY 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app
RUN mkdir /tokens
RUN /start.sh