#!/bin/sh

until cd /app/; do
  echo "Waiting for server volume..."
done

celery -A redmine_telegram_bot worker --loglevel=DEBUG
