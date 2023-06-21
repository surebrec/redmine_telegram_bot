#!/bin/sh

until cd /app/; do
  echo "Waiting for server volume..."
done

# Apply database migrations
echo "Applying database migrations ..."
python manage.py makemigrations

until python manage.py migrate; do
  echo "Waiting for db to be ready..."
  sleep 2
done

# Collecting static
until python manage.py collectstatic --noinput; do
  echo "Collecting static ..."
  sleep 2
done

python manage.py initadmin

# Start server
echo "Starting server ..."
gunicorn redmine_telegram_bot.wsgi:application --bind 0.0.0.0:8000  #python manage.py runpolling
