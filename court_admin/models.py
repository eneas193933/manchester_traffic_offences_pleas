import datetime as dt

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


class User(AbstractUser):

    court = models.ForeignKey(
        "apps.plea.Court", blank=True, null=True,
        help_text="The court region associated with this user")

    class Meta:
        db_table = "auth_user"
