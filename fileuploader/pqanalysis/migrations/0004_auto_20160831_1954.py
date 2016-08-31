# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pqanalysis.models


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0003_pqattachment_date_submitted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pqattachment',
            name='attachment',
            field=models.FileField(max_length=1000, upload_to=pqanalysis.models.upload_to),
        ),
    ]
