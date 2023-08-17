# Use a base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY cogs/ /app/cogs
COPY routes/ /app/routes
COPY services/ /app/services
COPY static/ /app/static
COPY templates/ /app/templates
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY gunicorn_conf.py /app/gunicorn_conf.py
COPY bot.py /app/bot.py

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variables
ENV WEB_CONCURRENCY=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 80

# Command to run the application
CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:80", "main:app"]