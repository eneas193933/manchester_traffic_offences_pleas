from make_a_plea.settings.base import *

ROOT_URLCONF = 'court_admin.urls'

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    'django.core.context_processors.request',
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.contrib.auth.context_processors.auth",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'waffle',
    'govuk_template',
    'apps.forms',
    'apps.plea',
    'widget_tweaks',
    'court_admin',
]

# for court-admin - may need to be moved to its own settings file when we figure out whwere the app will live
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/sign-in/"

VALID_HMCTS_EMAIL_DOMAINS = ["hmcts.gsi.gov.uk",
                             "digital.justice.gov.uk"]

COURT_ADMIN_EMAIL_FROM = "makeaplea@digital.justice.gov.uk"

PASSWORD_MIN_LENGTH = 8

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass

# importing test settings file if necessary (TODO could be done better)
if len(sys.argv) > 1 and 'test' or 'harvest' in sys.argv[1]:
    from .testing import *
