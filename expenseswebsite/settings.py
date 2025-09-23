"""
Django settings for expenseswebsite project.
"""

from pathlib import Path
from django.contrib import messages
import django_heroku
import os
from dotenv import load_dotenv

# ✅ BASE_DIR as a Path object (fixes the error)
BASE_DIR = Path(__file__).resolve().parent.parent
# ✅ Load .env file from project root (same folder as manage.py)
load_dotenv(BASE_DIR / '.env')
print("DEBUG:", os.environ.get("EMAIL_HOST_USER"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')l0nv5udi#-6w(kes8pb$e!sp(c!)_6ffg4n=_k5zf8c!^vrec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expenses',
    'userpreferences',
    'userincome',
    'authentication',
    'tailwind',
    'theme',
    'income',


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

ROOT_URLCONF = 'expenseswebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ cleaner with Path
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'expenseswebsite.wsgi.application'

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "incomeexpensesdb",
        "USER": "postgres",
        "PASSWORD": "1968",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'expenseswebsite' / 'static']
STATIC_ROOT = BASE_DIR / 'static'

django_heroku.settings(locals())

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

# ✅ Email Configuration (uses .env values)
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ✅ Use console backend for development, real SMTP in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
TAILWIND_APP_NAME = 'theme'
LOGOUT_REDIRECT_URL = 'login'  # or your homepage
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
