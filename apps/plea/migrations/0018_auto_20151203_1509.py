# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plea', '0017_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='datavalidation',
            options={'ordering': ['-date_entered']},
        ),
    ]
