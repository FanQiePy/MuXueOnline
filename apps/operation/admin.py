# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(UserAsk)
class UserAskAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['add_time']


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['add_time']


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['fav_type', 'add_time']


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message']
    list_filter = ['has_read', 'add_time']


@admin.register(UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['add_time']

