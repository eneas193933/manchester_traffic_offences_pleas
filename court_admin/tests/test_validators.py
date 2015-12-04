from django.contrib.auth.models import User
from django.forms import ValidationError
from django.test import TestCase, override_settings

from ..validators import *

valid_domains = ["digital.justice.gov.uk",
                 "hmcts.gsi.gov.uk",
                 "justice.gsi.gov.uk"]

class TestValidators(TestCase):

    def test_email_is_hmcts_when_no_setting(self):
        all_emails = ["email@digital.justice.gov.uk",
                        "email@hmcts.gsi.gov.uk",
                        "email@justice.gsi.gov.uk",
                        "email@hotmail.com",
                        "email@gmail.com",
                        "email@example.com"]

        for email in all_emails:
            self.assertTrue(is_email_hmcts(email))

    @override_settings(VALID_HMCTS_EMAIL_DOMAINS=valid_domains)
    def test_email_is_hmcts(self):
        valid_emails = ["email@digital.justice.gov.uk",
                        "email@hmcts.gsi.gov.uk",
                        "email@justice.gsi.gov.uk"]

        for email in valid_emails:
            self.assertTrue(is_email_hmcts(email))

    @override_settings(VALID_HMCTS_EMAIL_DOMAINS=valid_domains)
    def test_email_is_not_hmcts(self):
        invalid_emails = ["email@hotmail.com",
                          "email@gmail.com",
                          "email@example.com"]

        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                is_email_hmcts(email)

    def test_username_is_available(self):
        self.assertTrue(is_username_available("frank.marsh1"))

    def test_username_is_not_available(self):
        User.objects.create(username="frank.marsh")

        with self.assertRaises(ValidationError):
            is_username_available("frank.marsh")
