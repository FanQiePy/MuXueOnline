# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-18 02:50
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_is_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerCourse',
            fields=[
            ],
            options={
                'verbose_name': '\u8f6e\u64ad\u8bfe\u7a0b',
                'proxy': True,
                'verbose_name_plural': '\u8f6e\u64ad\u8bfe\u7a0b',
                'indexes': [],
            },
            bases=('courses.course',),
        ),
        migrations.AlterField(
            model_name='course',
            name='desc',
            field=DjangoUeditor.models.UEditorField(default='', verbose_name='\u8bfe\u7a0b\u63cf\u8ff0'),
        ),
    ]
