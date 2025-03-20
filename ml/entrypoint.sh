#!/bin/bash
set -e

# Export environment variables to a file that cron can source
env | grep -v "PATH\|HOME\|TERM" > /etc/environment

# Start cron daemon
cron

# Create log file
touch /var/log/cron.log

# Run the training script once at startup (optional)
# Comment out the next line if you don't want to run training immediately
python train.py >> /var/log/cron.log 2>&1

# Output message
echo "ML container started. Training will run weekly on Sunday at 1:00 AM." >> /var/log/cron.log

# Tail the log file to keep the container running
tail -f /var/log/cron.log