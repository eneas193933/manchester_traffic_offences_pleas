# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('court_admin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courtadminprofile',
            name='court',
            field=models.OneToOneField(null=True, blank=True, to='plea.Court', help_text=b'The court region associated with this user'),
        ),
    ]
