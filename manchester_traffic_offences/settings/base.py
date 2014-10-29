import sys
import os
from os.path import join, abspath, dirname


# PATH vars
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

DEBUG = True
template_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'manchester_traffic_offences',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

RAVEN_CONFIG = {
    'dsn': 'https://bec1584e479a4bc0b694b7fbcb4c632d:4ef91764e1ea4d2cbbd50a4d4bdcf4a5@app.getsentry.com/28000',
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = root('assets', 'uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = root('static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    root('assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'CHANGE THIS!!!'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'manchester_traffic_offences.urls'

SESSION_SERIALIZER = 'apps.govuk_utils.serializers.DateAwareSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'manchester_traffic_offences.wsgi.application'

TEMPLATE_DIRS = (
    "templates",
    root('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.contrib.auth.context_processors.auth",
    'manchester_traffic_offences.context_processors.globals',
    'apps.feedback.context_processors.feedback',
)

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.formtools',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'south',
    'django_extensions',
)

PROJECT_APPS = (
    'apps.govuk_utils',
    'moj_template',
    'apps.plea',
    'apps.feedback',
    'apps.receipt'
)

INSTALLED_APPS += PROJECT_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Django-rest-framework throttling config

REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
    }
}

INTERNAL_IPS = ['127.0.0.1']


# EMAILS
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "")

SMTP_ROUTES = {"GSI": {"HOST": "localhost",
                       "PORT": 25},
               "GMP": {"HOST": "localhost",
                       "PORT": 25}}

PLEA_EMAIL_FROM = "plea_from@example.org"
PLEA_EMAIL_ATTACHMENT_NAME = "plea.html"
PLEA_EMAIL_TEMPLATE = "plea/plea_email_attachment.html"
PLEA_EMAIL_TO = ["plea_to@example.org", ]
PLEA_EMAIL_SUBJECT = "ONLINE PLEA: {case[urn]} DOH: {email_date_of_hearing} {email_name}"
PLEA_EMAIL_BODY = ""

PLP_EMAIL_TO = ["plp_to@example.org", ]
PLP_EMAIL_TEMPLATE = "plea/plp_email_attachment.html"
PLP_EMAIL_SUBJECT = "POLICE %s" % PLEA_EMAIL_SUBJECT

FEEDBACK_EMAIL_FROM = "makeaplea@digital.justice.gov.uk"
FEEDBACK_EMAIL_TO = ("ian.george@digital.justice.gov.uk", )

PLEA_CONFIRMATION_EMAIL_FROM = os.environ.get("PLEA_CONFIRMATION_EMAIL_FROM", "")
PLEA_CONFIRMATION_EMAIL_SUBJECT = "Online plea submission confirmation"
PLEA_CONFIRMATION_EMAIL_BCC = []
SEND_PLEA_CONFIRMATION_EMAIL = True

RECEIPT_INBOX_FROM_EMAIL = os.environ.get("RECEIPT_INBOX_FROM_EMAIL", "")
RECEIPT_INBOX_USERNAME = os.environ.get("RECEIPT_INBOX_USERNAME", "")
RECEIPT_INBOX_PASSWORD = os.environ.get('RECEIPT_GMAIL_PASSWORD', '')
RECEIPT_INBOX_OAUTH_API_KEY = ""
RECEIPT_ADMIN_EMAIL_ENABLED = True
RECEIPT_ADMIN_EMAIL_SUBJECT = "Makeaplea receipt processing script"

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass


# importing test settings file if necessary (TODO could be done better)
if len(sys.argv) > 1 and 'test' or 'harvest' in sys.argv[1]:
    from .testing import *
