import random
import string

from django import forms
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import (AuthenticationForm,
                                       PasswordResetForm,
                                       PasswordChangeForm,
                                       SetPasswordForm)
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from apps.forms.forms import reorder_fields
from apps.plea.models import Court
from models import CourtAdminProfile
from token import token_generator
from messages import ERROR_MESSAGES
from validators import is_email_hmcts, is_username_available


new_password_field = forms.CharField(widget=forms.PasswordInput,
                                     label=_("Password"),
                                     help_text=_("Your password must have at least 6 characters."),
                                     min_length=6,
                                     error_messages={"required": ERROR_MESSAGES["NEW_PASSWORD_REQUIRED"],
                                                     "min_length": ERROR_MESSAGES["PASSWORD_MIN_LENGTH"]})

password_confirm_field = forms.CharField(widget=forms.PasswordInput,
                                         label=_("Re-type your password"),
                                         error_messages={"required": ERROR_MESSAGES["NEW_PASSWORD_CONFIRM_REQUIRED"]})


class EmailNotAvailable(Exception):
    pass


class UsernameNotAvailable(Exception):
    pass


class CourtAdminAuthenticationForm(AuthenticationForm):

    username = forms.CharField(label=_("Username"),
                               max_length=254,
                               error_messages={"required": ERROR_MESSAGES["USERNAME_REQUIRED"]})

    password = forms.CharField(widget=forms.PasswordInput,
                               label=_("Password"),
                               error_messages={"required": ERROR_MESSAGES["PASSWORD_REQUIRED"]})

    error_messages = {
        "invalid_login": "INVALID_LOGIN",
        "inactive": "INACTIVE_USER"
    }


class CourtAdminPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(label=_("Email address"),
                             help_text=_("Your HMCTS email address."),
                             max_length=254,
                             validators=[is_email_hmcts],
                             error_messages={"required": ERROR_MESSAGES["EMAIL_REQUIRED"],
                                             "invalid": ERROR_MESSAGES["EMAIL_INVALID"],
                                             "is_email_hmcts": ERROR_MESSAGES["EMAIL_HMCTS_INVALID"]})


class CourtAdminSetPasswordForm(SetPasswordForm):

    new_password1 = new_password_field

    new_password2 = password_confirm_field

    error_messages = {
        "password_mismatch": ERROR_MESSAGES["PASSWORD_MISMATCH"]
    }


class InviteUserForm(forms.Form):

    email = forms.EmailField(label=_("Email address"),
                             help_text=_("Enter the user's registered HMCTS email address."),
                             max_length=254,
                             validators=[is_email_hmcts],
                             error_messages={"required": ERROR_MESSAGES["INVITE_EMAIL_REQUIRED"],
                                             "invalid": ERROR_MESSAGES["EMAIL_INVALID"],
                                             "is_email_hmcts": ERROR_MESSAGES["EMAIL_HMCTS_INVALID"]})

    first_name = forms.CharField(label=_("First name"),
                                 error_messages={"required": ERROR_MESSAGES["INVITE_FIRST_NAME_REQUIRED"]})

    last_name = forms.CharField(label=_("Last name"),
                                error_messages={"required": ERROR_MESSAGES["INVITE_LAST_NAME_REQUIRED"]})

    court = forms.ModelChoiceField(label=_("Court"),
                                   queryset=Court.objects.all(),
                                   error_messages={"required": ERROR_MESSAGES["COURT_REQUIRED"]})

    @staticmethod
    def get_random_username():

        def _make_username():
            return "INVITE_" + "".join(random.choice(string.ascii_letters) for _ in range(23))

        random_username = _make_username()

        while User.objects.filter(username=random_username).exists():
            random_username = _make_username()

        return random_username

    def create_user(self, email, first_name, last_name, court):

        court_perm = Permission.objects.get(codename="court_staff_user")

        if User.objects.filter(email=email).exists():
            raise EmailNotAvailable

        try:
            user = User()
            user.username = self.get_random_username()
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()

            user.user_permissions.add(court_perm)
            user.save()
        except IntegrityError:
            raise UsernameNotAvailable

        CourtAdminProfile.objects.create(user=user, court=court)

        return user

    def create_user_from_form(self, form):
        return self.create_user(
            form.cleaned_data["email"],
            form.cleaned_data["first_name"],
            form.cleaned_data["last_name"],
            form.cleaned_data["court"])

    @staticmethod
    def send_invite_email(user, **extra_context):

        token = token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        context = {
            "invite_url": reverse("register", kwargs={"uidb64": uid, "token": token}),
            "name": user.first_name
        }

        context.update(extra_context)

        message = render_to_string("emails/invite_user_email.txt", context)
        subject = render_to_string("emails/invite_user_email_subject.txt", context)

        user.email_user(subject, message, from_email="lyndon.garvey@digital.justice.gov.uk", fail_silently=False)


class RegistrationForm(forms.Form):

    username = forms.CharField(label=_("Username"),
                               max_length=254,
                               validators=[is_username_available],
                               error_messages={"required": ERROR_MESSAGES["NEW_USERNAME_REQUIRED"],
                                               "is_username_available": ERROR_MESSAGES["NEW_USERNAME_TAKEN"]})

    first_name = forms.CharField(label=_("First name"),
                                 error_messages={"required": ERROR_MESSAGES["FIRST_NAME_REQUIRED"]})

    last_name = forms.CharField(label=_("Last name"),
                                 error_messages={"required": ERROR_MESSAGES["LAST_NAME_REQUIRED"]})

    password1 = new_password_field
    password2 = password_confirm_field

    @staticmethod
    def verify_token(uidb64, token):

        uid = force_text(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(pk=uid)
        except User.DoesNotExist:
            return False, None

        return token_generator.check_token(user, token), user

    def activate_user(self, user):

        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.set_password(self.cleaned_data["password1"])
        user.is_active = True
        user.save()


class PersonalDetailsForm(forms.ModelForm):

    username = forms.CharField(label=_("Username"),
                               max_length=254,
                               validators=[is_username_available],
                               error_messages={"required": ERROR_MESSAGES["NEW_USERNAME_REQUIRED"],
                                               "is_username_available": ERROR_MESSAGES["NEW_USERNAME_TAKEN"]})

    first_name = forms.CharField(label=_("First name"),
                                 error_messages={"required": ERROR_MESSAGES["FIRST_NAME_REQUIRED"]})

    last_name = forms.CharField(label=_("Last name"),
                                 error_messages={"required": ERROR_MESSAGES["LAST_NAME_REQUIRED"]})

    email = forms.EmailField(label=_("Email"),
                             help_text=_("Your HMCTS email address."),
                             max_length=254,
                             validators=[is_email_hmcts],
                             error_messages={"required": ERROR_MESSAGES["INVITE_EMAIL_REQUIRED"],
                                             "invalid": ERROR_MESSAGES["EMAIL_INVALID"],
                                             "is_email_hmcts": ERROR_MESSAGES["EMAIL_HMCTS_INVALID"]})

    class Meta:
        model = CourtAdminProfile
        fields = ["first_name", "last_name", "email", "username"]


class CourtAdminPasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label=_("Current password"),
                                   widget=forms.PasswordInput,
                                   error_messages={"required": ERROR_MESSAGES["OLD_PASSWORD_REQUIRED"]})

    new_password1 = new_password_field

    new_password2 = password_confirm_field

    error_messages = {
        "password_incorrect": ERROR_MESSAGES["OLD_PASSWORD_INCORRECT"],
        "password_mismatch": ERROR_MESSAGES["PASSWORD_MISMATCH"]
    }

    def __init__(self, *args, **kwargs):
        super(CourtAdminPasswordChangeForm, self).__init__(*args, **kwargs)
        fields_order = ["old_password", "new_password1", "new_password2"]
        self.fields = reorder_fields(self.fields, fields_order)
