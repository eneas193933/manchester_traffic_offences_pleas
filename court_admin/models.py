import datetime as dt

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