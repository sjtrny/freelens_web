#!/bin/bash

# Collect static files
echo "Collecting static files"
uv run python manage.py collectstatic --noinput

# Check and set SECRET_KEY
export $(uv run python scripts/env.py)

# Apply database migrations
echo "Applying database migrations"
uv run python manage.py migrate

# Set super user
echo "Setting superuser"
uv run python manage.py create_superuser

echo "Starting server"
uv run gunicorn -b 0.0.0.0:80 web.wsgi