#!/bin/bash
set -o errexit

# Script de build: lo uso para dejar la app lista.
# En orden hace: instala dependencias, aplica migraciones, (opcional)
# carga datos iniciales, junta archivos estáticos y crea superusuario.

echo "Installing dependencies..."
# Aquí instalamos lo que está en requirements.txt. Si algo falla,
# el `set -o errexit` hace que el script pare de una vez.
pip install -r requirements.txt

echo "Running migrations..."
# Aplica cambios en la base de datos según los modelos actuales.
# Básicamente actualiza las tablas para que coincidan con el código.
python manage.py migrate

if [ "${RUN_SEED_ON_BUILD:-False}" = "True" ]; then
	# Si la variable de entorno está a True, corremos el comando de seed.
	# Esto mete datos iniciales (útil para pruebas o demos).
	echo "Seeding initial data..."
	python manage.py seed
else
	# Si no está activado, lo saltamos para no pisar datos reales.
	echo "Skipping seed (set RUN_SEED_ON_BUILD=True to enable)."
fi

echo "Collecting static files..."
# Junta todos los archivos estáticos (CSS, JS, imágenes) en una carpeta
# lista para servir en producción o pruebas.
python manage.py collectstatic --noinput

if [ "${RUN_CREATESU_ON_BUILD:-False}" = "True" ]; then
	# Crea un superusuario automatizado si hace falta. Útil en entornos
	# de prueba donde quieres acceder al admin sin crear cuentas manuales.
	echo "Creating superuser if it doesn't exist..."
	python manage.py createsu
else
	# Lo saltamos por defecto para no crear usuarios por accidente.
	echo "Skipping superuser creation (set RUN_CREATESU_ON_BUILD=True to enable)."
fi

echo "Build completed successfully!"
