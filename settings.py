DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ratazana_db',
        'USER': 'ratazana',
        'PASSWORD': 'eminem31',
        'HOST': 'localhost',
        'PORT': '5432',  # Default PostgreSQL port
    }
}

INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework', 

    # Your apps
    'core',  # Add your app here
]
