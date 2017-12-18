# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-08 13:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0004_auto_20171206_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='user',
            field=models.ManyToManyField(related_name='course', related_query_name='course', to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]
