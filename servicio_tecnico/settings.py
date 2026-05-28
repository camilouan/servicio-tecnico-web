from pathlib import Path
import os


# Base del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key')

# En producción debe ir en False.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Dominios permitidos para el sitio.
ALLOWED_HOSTS = ['.onrender.com', '.onrenderer.com', 'localhost', '127.0.0.1']


# Apps instaladas.

INSTALLED_APPS = [
    'jazzmin',
    'inventario',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'cloudinary',
    'cloudinary_storage',
]

JAZZMIN_SETTINGS = {
    'site_title': 'Servicio Técnico Admin',
    'site_header': 'Servicio Técnico',
    'site_brand': 'Panel Administrativo',
    'site_logo': 'img/logo.png',
    'login_logo': None,
    'site_icon': 'img/logo.png',
    'welcome_sign': 'Bienvenido al panel administrativo de Servicio Técnico',
    'copyright': 'Servicio Técnico',
    'search_model': ['inventario.Producto', 'inventario.Categoria', 'inventario.Apartado', 'inventario.Usuario'],
    'topmenu_links': [
        {'name': 'Ver sitio', 'url': '/', 'new_window': True},
        {'model': 'inventario.Producto'},
        {'model': 'inventario.Apartado'},
        {'app': 'inventario'},
    ],
    'show_sidebar': True,
    'navigation_expanded': True,
    'related_modal_active': True,
    'changeform_format': 'horizontal_tabs',
    'order_with_respect_to': ['inventario', 'auth'],
    'icons': {
        'auth': 'fas fa-users-cog',
        'auth.Group': 'fas fa-user-shield',
        'inventario.Usuario': 'fas fa-user-circle',
        'inventario.Producto': 'fas fa-mobile-alt',
        'inventario.Categoria': 'fas fa-layer-group',
        'inventario.Apartado': 'fas fa-box-open',
        'inventario.HeroBanner': 'fas fa-image',
    },
}

JAZZMIN_UI_TWEAKS = {
    'theme': 'flatly',
    'dark_mode_theme': 'darkly',
    'navbar': 'navbar-primary navbar-dark',
    'accent': 'accent-info',
    'sidebar': 'sidebar-dark-primary',
    'brand_colour': 'navbar-primary',
    'button_classes': {
        'primary': 'btn-primary',
        'secondary': 'btn-outline-secondary',
        'info': 'btn-info',
        'warning': 'btn-warning',
        'danger': 'btn-danger',
        'success': 'btn-success',
    },
}


# Cadena de middlewares del proyecto.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'inventario.middleware.InactivityTimeoutMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'servicio_tecnico.urls'


# Configuración de plantillas HTML.

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'inventario' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'inventario.context_processors.admin_apartados_popup',
            ],
        },
    },
]


WSGI_APPLICATION = 'servicio_tecnico.wsgi.application'


# Base de datos.

DATABASE_URL = os.environ.get('DATABASE_URL')
DB_CONN_MAX_AGE = int(os.environ.get('DB_CONN_MAX_AGE', '0' if DATABASE_URL else '60'))
DB_CONNECT_TIMEOUT = int(os.environ.get('DB_CONNECT_TIMEOUT', '5'))
DB_STATEMENT_TIMEOUT_MS = int(os.environ.get('DB_STATEMENT_TIMEOUT_MS', '20000'))

if DATABASE_URL:
    # En Render uso PostgreSQL.
    import urllib.parse
    parsed_url = urllib.parse.urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': parsed_url.path[1:],
            'USER': parsed_url.username,
            'PASSWORD': parsed_url.password,
            'HOST': parsed_url.hostname,
            'PORT': parsed_url.port or '',
            'CONN_MAX_AGE': DB_CONN_MAX_AGE,
            'CONN_HEALTH_CHECKS': True,
            'OPTIONS': {
                'connect_timeout': DB_CONNECT_TIMEOUT,
                'sslmode': os.environ.get('DB_SSLMODE', 'require'),
                'options': f'-c statement_timeout={DB_STATEMENT_TIMEOUT_MS}',
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'CONN_MAX_AGE': DB_CONN_MAX_AGE,
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'servicio-tecnico-cache',
        'TIMEOUT': 300,
    }
}


# Reglas de contraseña.

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Seguridad de login y sesión.
LOGIN_MAX_FAILED_ATTEMPTS = int(os.environ.get('LOGIN_MAX_FAILED_ATTEMPTS', '5'))
LOGIN_LOCKOUT_SECONDS = int(os.environ.get('LOGIN_LOCKOUT_SECONDS', '900'))
SESSION_INACTIVITY_TIMEOUT = int(os.environ.get('SESSION_INACTIVITY_TIMEOUT', '1800'))
SESSION_COOKIE_AGE = SESSION_INACTIVITY_TIMEOUT
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False


# Correo para recuperación de contraseña.

EMAIL_BACKEND = os.environ.get(
    'EMAIL_BACKEND',
    'django.core.mail.backends.console.EmailBackend' if DEBUG else 'django.core.mail.backends.smtp.EmailBackend',
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or 'no-reply@servicio-tecnico.local')
PASSWORD_RESET_TIMEOUT = int(os.environ.get('PASSWORD_RESET_TIMEOUT', '3600'))


# Idioma y zona horaria.

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'

USE_I18N = True
USE_TZ = True


# Archivos estáticos.

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True


# Archivos subidos por usuarios en local.

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Creo las carpetas si no existen para evitar errores en local.
os.makedirs(MEDIA_ROOT, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)


# -------------------------
# AUTH USER
# -------------------------

AUTH_USER_MODEL = 'inventario.Usuario'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# -------------------------
# CLOUDINARY
# -------------------------

import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', ''),
}

if CLOUDINARY_STORAGE['CLOUD_NAME'] and CLOUDINARY_STORAGE['API_KEY'] and CLOUDINARY_STORAGE['API_SECRET']:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'