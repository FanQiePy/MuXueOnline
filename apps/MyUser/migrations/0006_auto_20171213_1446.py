# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-13 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyUser', '0005_auto_20171204_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[('register', '\u6ce8\u518c'), ('forget', '\u627e\u56de\u5bc6\u7801'), ('change_email', '\u4fee\u6539\u90ae\u7bb1')], max_length=20, verbose_name='\u9a8c\u8bc1\u7801'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(default='avatar/default.png', upload_to='avatar/%Y/%m'),
        ),
    ]
