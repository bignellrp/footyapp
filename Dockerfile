FROM tiangolo/meinheld-gunicorn-flask

# set environment variables
ENV WEB_CONCURRENCY 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY . /app
RUN mkdir /tokens
COPY poststart.sh /tmp/poststart.sh
RUN chmod +x  /tmp/poststart.sh
#RUN /tmp/poststart.sh