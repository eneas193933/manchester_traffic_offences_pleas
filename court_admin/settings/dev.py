from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += ('raven.contrib.django.raven_compat', )

RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_DSN', '')
}

ALLOWED_HOSTS = ["admin.dev.makeaplea.dsd.io", ]