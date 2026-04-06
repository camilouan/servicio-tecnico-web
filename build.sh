#!/bin/bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if it doesn't exist..."
python manage.py createsu

echo "Build completed successfully!"
