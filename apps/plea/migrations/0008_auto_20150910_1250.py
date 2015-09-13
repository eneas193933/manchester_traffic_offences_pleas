# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plea', '0007_auto_20150902_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='court',
            name='live_date',
            field=models.DateTimeField(help_text=b'The date the court is/was made live', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='usagestats',
            name='court',
            field=models.ForeignKey(default=1, to='plea.Court'),
            preserve_default=False,
        ),
    ]
