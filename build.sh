#!/bin/bash
set -o errexit

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

if [ "${RUN_SEED_ON_BUILD:-False}" = "True" ]; then
	echo "Seeding initial data..."
	python manage.py seed
else
	echo "Skipping seed (set RUN_SEED_ON_BUILD=True to enable)."
fi

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "${RUN_CREATESU_ON_BUILD:-False}" = "True" ]; then
	echo "Creating superuser if it doesn't exist..."
	python manage.py createsu
else
	echo "Skipping superuser creation (set RUN_CREATESU_ON_BUILD=True to enable)."
fi

echo "Build completed successfully!"
