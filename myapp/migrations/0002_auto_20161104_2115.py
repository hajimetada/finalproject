# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-11-04 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='input',
            old_name='r',
            new_name='communityarea',
        ),
        migrations.AddField(
            model_name='input',
            name='name',
            field=models.CharField(default='PA', max_length=50),
            preserve_default=False,
        ),
    ]
