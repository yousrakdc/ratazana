from pathlib import Path
from datetime import timedelta
import os
import smtplib
import google.auth
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = 'django-insecure-h*xn@&1y0z&37k0=matdxg^p*ano4m7rl-jpqseg$d-6!w(^m%'
DEBUG = True
ALLOWED_HOSTS = ['c347-77-136-104-119.ngrok-free.app', '127.0.0.1', 'localhost']  # Localhost

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'debug_toolbar',
    'signup',
    'rest_framework_simplejwt',
    'django.contrib.sites',
    'dj_rest_auth',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',  # Updated line
        'rest_framework_simplejwt.tokens.RefreshToken',  # Keep refresh token if you need it
    ),
    'AUTH_USER_MODEL': 'core.CustomUser',
}


ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

# Use cookies for session management
SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = 'Lax' 

ROOT_URLCONF = 'urls'
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend/')],
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

WSGI_APPLICATION = 'wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'core.auth_backends.EmailBackend',
]

# Configure email verification settings
ACCOUNT_EMAIL_VERIFICATION = "none"  # Options: 'mandatory', 'optional', 'none'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = True  # Or False if you don't want username field
ACCOUNT_AUTHENTICATION_METHOD = "email"  # To use email for login instead of username
ACCOUNT_FORMS = {'signup': 'path.to.CustomSignupForm'}

# Redirects
LOGIN_REDIRECT_URL = "/"  # Where to redirect after login
ACCOUNT_LOGOUT_REDIRECT_URL = "/accounts/login/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/"

# Optional but recommended
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USER_MODEL_EMAIL_FIELD = 'email'

# Use Django's password validators
ACCOUNT_PASSWORD_MIN_LENGTH = 8

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ratazana.staff@gmail.com'
EMAIL_HOST_PASSWORD = 'RatRat3184!'
DEFAULT_FROM_EMAIL = 'ratazana.staff@gmail.com'

EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
ANYMAIL = {}
DEFAULT_FROM_EMAIL = 'ratazana.staff@gmail.com'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ratazana_db',
        'USER': 'ratazana',
        'PASSWORD': 'eminem31',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Media files (uploaded by users or scraped)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'backend/media')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/staticfiles'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.CustomUser'

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = ['http://localhost:5173'] 

INTERNAL_IPS = [
    '0.0.0.1',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
  
        'ratazana': { 
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis as the broker
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
ELERY_TIMEZONE = 'UTC'
CELERY_IMPORTS = ('backend.core.tasks',)


# Optional: This will enable periodic tasks with the celery beat
CELERY_BEAT_SCHEDULE = {
    'scrape-jerseys-every-hour': {
        'task': 'core.tasks.scrape_jerseys',
        'schedule': 3600.0,  # Schedule the task to run every hour (3600 seconds)
    },
}