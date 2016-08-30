# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0002_auto_20160830_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='pqattachment',
            name='date_submitted',
            field=models.DateField(default=datetime.datetime(2016, 8, 30, 19, 23, 39, 764719, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
