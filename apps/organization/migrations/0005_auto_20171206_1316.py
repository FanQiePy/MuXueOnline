# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-06 13:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20171206_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='students',
            new_name='student_num',
        ),
    ]
