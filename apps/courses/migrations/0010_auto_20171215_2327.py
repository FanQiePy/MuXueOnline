# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 23:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=100, verbose_name='\u8bfe\u7a0b\u516c\u544a'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_course', to='organization.Teacher'),
        ),
    ]
