
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-(#8(&6_-6ur%&^s2ycdc_^%*ffbgjdnnh##lkn-k!43@4_hdd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_WHITELIST = (

)

CORS_ORIGIN_ALLOW_ALL = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'warehouse.kapas',
    'corsheaders',
    'django_filters'
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
    'django.middleware.common.CommonMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    )
}


ROOT_URLCONF = 'warehouse.urls'

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

WSGI_APPLICATION = 'warehouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'warehouse',
        'USER' : 'aviconn',
        'PASSWORD' : 'avc123',
        'HOST' : '127.0.0.1',
        'POST' : '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'kapas.User'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

#Django error log to admin email account
MAILER_LIST = ['subhash.kumar@aviconn.in']
CRISPY_TEMPLATE_PACK = 'bootstrap3'
ADMIN_SITE_HEADER = "Aviconn Solutions"
EMAIL_USE_TLS=True
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='no.reply@aviconn.in'
EMAIL_HOST_PASSWORD='j*>aj3An'
EMAIL_PORT=587
DEFAULT_FROM_EMAIL ='no.reply@aviconn.in'
ADMINS = [('subhash', 'subhash.kumar@aviconn.in')]


# Celery log setup
CELERY_BROKER_URL = 'redis://avi.anuvratparashar.com:6379'
#CELERY_RESULT_BACKEND = 'redis://localhost:6379'
BROKER_TRANSPORT = 'redis'
#CELERY_ACCEPT_CONTENT = ['application/json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

CELERYD_HIJACK_ROOT_LOGGER = False
#Local log files setup
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
     'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
	},
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
	'mail_admins':{
	     'level': 'ERROR',
	     'filters': ['require_debug_false'],
	     'class': 'django.utils.log.AdminEmailHandler',
	},
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/Users/aviconn/Desktop/subhash/djangologfiles/celery.log',
            'formatter': 'verbose',
            #'maxBytes': 1024 * 1024 * 100, # 100 MB
            #'backupCount': 10,
        },

        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            #'maxytes': 1024 * 1024 * 100, # 100 mb
        },
        'django_error': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/Users/aviconn/Desktop/subhash/djangologfiles/error.log',
            'formatter': 'verbose'
        },
        'django_runserver': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/Users/aviconn/Desktop/subhash/djangologfiles/django_runserver.log',
            'formatter': 'verbose'
        },

    },
    'loggers': {
        'django.request': {
            'handlers':['mail_admins', 'django_error'],
            'propagate': True,
            'level':'ERROR',
        },
        'celery': {
            'handlers': ['console', 'file',],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console', 'django_runserver'],
            'level': 'INFO',
            'propagate': True,
        },

    }
}
