#!/bin/sh

until cd /app/; do
  echo "Waiting for server volume..."
done

celery -A redmine_telegram_bot beat --loglevel=INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
