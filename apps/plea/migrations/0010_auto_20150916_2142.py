# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plea', '0009_auto_20150916_1345'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='court',
            options={'permissions': (('court_staff_user', 'Court staff user'), ('court_staff_admin', 'Court staff admin user'))},
        ),
    ]
