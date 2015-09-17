import random
import string

from django import forms
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User, Permission
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from apps.plea.models import Court
from models import CourtAdminProfile
from token import token_generator


class EmailNotAvailable(Exception):
    pass

class UsernameNotAvailable(Exception):
    pass


class InviteUserForm(forms.Form):

    email = forms.EmailField()
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    court = forms.ModelChoiceField(queryset=Court.objects.all())

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
    def send_invite_email(user):

        token = token_generator.make_token(user)

        uid = urlsafe_base64_encode(force_bytes(user.pk))

        context = {
            "invite_url": reverse("register", kwargs={"uidb64": uid, "token": token}),
            "name": user.first_name
        }

        message = render_to_string("court_registration/invite_user_email.txt", context)
        subject = render_to_string("court_registration/invite_user_email_subject.txt", context)

        user.email_user(subject, message, from_email="lyndon.garvey@digital.justice.gov.uk", fail_silently=False)


class RegistrationForm(forms.Form):

    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password = cleaned_data.get("password", None)
        password2 = cleaned_data.get("password2", None)

        if password and password2 and password != password2:
            raise forms.ValidationError("Entered passwords do not match")

        username = cleaned_data["username"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")

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
        user.set_password(self.cleaned_data["password"])
        user.is_active = True
        user.save()
