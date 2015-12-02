from make_a_plea.settings.base import *

ROOT_URLCONF = 'court_admin.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB',''),
        'USER': os.environ.get('POSTGRES_USER', ''),
        'PASSWORD': os.environ.get('POSTGRES_PASS', ''),
        'HOST': os.environ.get('POSTGRES_HOST', ''),
        'PORT': os.environ.get('POSTGRES_PORT', ''),
    }
}

# for court-admin - may need to be moved to its own settings file when we figure out whwere the app will live
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

VALID_HMCTS_EMAIL_DOMAINS = []

PASSWORD_MIN_LENGTH = 8

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass

# importing test settings file if necessary (TODO could be done better)
if len(sys.argv) > 1 and 'test' or 'harvest' in sys.argv[1]:
    from .testing import *
