# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0004_auto_20160831_1954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pqresults',
            name='pqresults',
        ),
        migrations.AddField(
            model_name='pqattachment',
            name='pq_results',
            field=models.ForeignKey(default=0, to='pqanalysis.PqResults'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pqresults',
            name='file_dir',
            field=models.FileField(max_length=1000, upload_to=None),
        ),
    ]
