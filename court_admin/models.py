import datetime as dt
import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


class Invite(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    redeemed = models.BooleanField()

    @property
    def expired(self):
        return self.created >= dt.datetime.now()

    def is_valid(self):
        return not self.expired and not self.redeemed

    def send_invitation_email(self):
        pass


# class User(AbstractUser):
#
#     require_change_password = models.BooleanField(
#         default=False,
#         help_text="Require that the user change their password on next logon")
#
#     class Meta:
#         db_table = "auth_user"
#
#     def assign_temporary_password(self):
#
#         password_length = 12
#         chars = string.ascii_letters + string.digits + string.punctuation
#
#         password = "".join(map(lambda x: random.choice(chars), [0] * password_length))
#
#         self.user.require_change_password = 1
#         self.user.set_password(password)
#         self.user.save()
#
#         return password


# class CourtAdminProfile(models.Model):
#
#     user = models.ForeignKey("auth.User")
#
#     court = models.ForeignKey(
#         "apps.plea.Court", blank=True, null=True,
#         help_text="The court region associated with this user")


