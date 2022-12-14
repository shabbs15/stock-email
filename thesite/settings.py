import os
import django
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', False) == False #whole thing returns false
DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
    

ALLOWED_HOSTS = [
    '127.0.0.1',
    '0.0.0.0',
    'https://emailstocks.herokuapp.com/',
    'http://www.stockpricedelta.xyz/',
    'www.stockpricedelta.xyz/',
    'www.stockpricedelta.xyz',
    'stockpricedelta.xyz/',
    'stockpricedelta.xyz',
    'emailstocks.herokuapp.com/',
    'emailstocks.herokuapp.com',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'AKIAWNW7NNQXGC5YLP3E' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = 'BH0GwASXf4K07IH+68OidkIDbfBLBUDArlyukzBJ3FOa'


SESSION_EXPIRE_AT_BROWSER_CLOSE=True


# Application definition

INSTALLED_APPS = [
#    'stocks.apps.StocksConfig',
    'stocks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'thesite.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'thesite.wsgi.application'


<<<<<<< HEAD
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default":{
<<<<<<< HEAD
        "ENGINE": "djongo",
        "NAME": "stocks",
    }
}

"""
=======
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "database",
    }
}

>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))
if "DATABASE_URL" in os.environ:
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': "database",
            "USER": "mydatabaseuser",
            "PASSWORD": "p",
            "HOST": "localhost",
            "PORT": "",
        }
    }
<<<<<<< HEAD
"""
=======
>>>>>>> parent of c300606 (trying db in pymongo (doesn't work))


=======
>>>>>>> parent of 91ad9b3 (Revert "trying db in pymongo (doesn't work)")
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#celery
CELERY_TIMEZONE = 'UTC'

if os.getenv("DEBUG", False):
    CELERY_BROKER_URL = 'redis://localhost:6379'
else:
    CELERY_BROKER_URL = os.environ["REDIS_URL"]
