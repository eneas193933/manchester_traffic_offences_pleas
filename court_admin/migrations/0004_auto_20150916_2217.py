# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('court_admin', '0003_auto_20150916_1548'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Invite',
        ),
        migrations.AlterField(
            model_name='courtadminprofile',
            name='court',
            field=models.ForeignKey(blank=True, to='plea.Court', help_text=b'The court region associated with this user', null=True),
        ),
    ]
