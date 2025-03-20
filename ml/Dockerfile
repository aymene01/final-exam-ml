FROM python:3.9-slim

WORKDIR /app

# Install cron
RUN apt-get update && apt-get -y install cron

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add crontab file
COPY crontab /etc/cron.d/ml-cron
RUN chmod 0644 /etc/cron.d/ml-cron
RUN crontab /etc/cron.d/ml-cron

# Script to run cron and keep container alive
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]