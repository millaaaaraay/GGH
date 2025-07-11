from pathlib import Path
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Claves para producción, mejor usar variables de entorno en Render
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dm%$(n(*z7044i68z1d_*n(o$(%)zk@kfkv$tm5fxv4en6iqlf')
DEBUG = os.environ.get('DEBUG', '') != 'False'
ALLOWED_HOSTS = ['*']  # Cambia en producción si tienes dominio propio

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuarios',  # Tu app personalizada
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gghweb.urls'

WSGI_APPLICATION = 'gghweb.wsgi.application'

# Configuración de base de datos para Render/PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    )
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'usuarios.context_processors.redes_sociales',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-cl'  # O 'en-us' según prefieras
TIME_ZONE = 'America/Santiago'  # Cambia a tu zona si es necesario
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'usuarios' / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de email (solo para pruebas, cambia en producción)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Puedes agregar otras configuraciones extra según tu proyecto

