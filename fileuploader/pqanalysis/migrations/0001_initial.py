# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pqanalysis.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CombineResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('combine_file_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PqAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('analysis_id', models.CharField(max_length=100)),
                ('file_name', models.CharField(max_length=100)),
                ('attachment', models.FileField(upload_to=pqanalysis.models.upload_to)),
            ],
        ),
        migrations.CreateModel(
            name='PqResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pq_file_name', models.CharField(max_length=100)),
                ('pqresults', models.ForeignKey(to='pqanalysis.PqAttachment')),
            ],
        ),
        migrations.AddField(
            model_name='combineresults',
            name='combine_results',
            field=models.ForeignKey(to='pqanalysis.PqAttachment'),
        ),
    ]
