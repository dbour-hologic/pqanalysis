# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pqanalysis', '0006_auto_20160831_2249'),
    ]

    operations = [
        migrations.CreateModel(
            name='PqResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pq_file_name', models.CharField(max_length=100)),
                ('file_dir', models.FileField(max_length=1000, upload_to=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='pqattachment',
            name='pq_file_dir',
        ),
        migrations.RemoveField(
            model_name='pqattachment',
            name='pq_file_name',
        ),
        migrations.AddField(
            model_name='pqattachment',
            name='pqresults',
            field=models.ForeignKey(to='pqanalysis.PqResults', null=True),
        ),
    ]
