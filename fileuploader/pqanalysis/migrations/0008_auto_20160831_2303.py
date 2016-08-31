# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0007_auto_20160831_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pqattachment',
            name='pqresults',
        ),
        migrations.AddField(
            model_name='pqattachment',
            name='pq_file_dir',
            field=models.FileField(max_length=1000, null=True, upload_to=None, blank=True),
        ),
        migrations.AddField(
            model_name='pqattachment',
            name='pq_file_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='PqResults',
        ),
    ]
