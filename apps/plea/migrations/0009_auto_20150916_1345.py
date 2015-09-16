# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plea', '0008_auto_20150910_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='court',
            name='live_date',
            field=models.DateField(help_text=b'The date the court went live', null=True, blank=True),
        ),
    ]
