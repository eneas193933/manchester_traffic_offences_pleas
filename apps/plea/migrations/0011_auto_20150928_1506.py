# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plea', '0010_auto_20150916_2142'),
    ]

    operations = [
        migrations.AddField(
            model_name='usagestats',
            name='postal_guilty_pleas',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='usagestats',
            name='postal_not_guilty_pleas',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
