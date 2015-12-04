from django.conf import settings
from django.contrib.auth.models import User
from django.core import exceptions

def is_email_hmcts(email):
    valid_domains = getattr(settings, "VALID_HMCTS_EMAIL_DOMAINS", [])

    if len(valid_domains) == 0:
        return True

    email_domain = email.split('@')

    try:
        if email_domain[1] not in valid_domains:
            raise exceptions.ValidationError("The email must be a valid HMCTS address", code="is_email_hmcts")
    except IndexError:
        pass

    return True


def is_username_available(username):
    if User.objects.filter(username=username).exists():
        raise exceptions.ValidationError("Username already exists", code="is_username_available")

    return True
