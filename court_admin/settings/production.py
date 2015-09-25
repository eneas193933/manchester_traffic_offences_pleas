from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += ('raven.contrib.django.raven_compat', )

ALLOWED_HOSTS = ["admin.makeaplea.justice.gov.uk", ]
