from django.db import models
from django.conf import settings


class CourtAdminProfile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL)

    court = models.ForeignKey(
        "plea.Court", blank=True, null=True,
        help_text="The court region associated with this user")
