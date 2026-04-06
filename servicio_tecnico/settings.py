from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-local-dev-key')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']


# -------------------------
# APPS
# -------------------------

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
    'login_logo': 'img/logo.png',
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


# -------------------------
# MIDDLEWARE
# -------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'servicio_tecnico.urls'


# -------------------------
# TEMPLATES
# -------------------------

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
            ],
        },
    },
]


WSGI_APPLICATION = 'servicio_tecnico.wsgi.application'


# -------------------------
# DATABASE
# -------------------------

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
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
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# -------------------------
# PASSWORD VALIDATION
# -------------------------

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


# -------------------------
# INTERNATIONALIZATION
# -------------------------

LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'

USE_I18N = True
USE_TZ = True


# -------------------------
# STATIC FILES
# -------------------------

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_USE_FINDERS = True


# -------------------------
# MEDIA FILES (LOCAL DEV)
# -------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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