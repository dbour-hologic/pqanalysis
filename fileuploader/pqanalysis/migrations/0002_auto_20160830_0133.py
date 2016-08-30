# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pqattachment',
            name='submitter',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pqresults',
            name='file_dir',
            field=models.FileField(default='', upload_to=None),
            preserve_default=False,
        ),
    ]
