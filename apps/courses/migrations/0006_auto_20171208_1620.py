# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-08 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='user',
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u7c7b\u522b'),
        ),
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(default='', max_length=20, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]
