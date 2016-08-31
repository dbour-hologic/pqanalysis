# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0005_auto_20160831_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pqattachment',
            name='pq_results',
        ),
        migrations.AddField(
            model_name='pqattachment',
            name='pq_file_dir',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
        migrations.AddField(
            model_name='pqattachment',
            name='pq_file_name',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='PqResults',
        ),
    ]
