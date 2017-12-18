# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.conf import settings
from .models import *

# Register your models here.


class LessonInline(InlineModelAdmin):
    model = Lesson
    extra = 0


class CourseResourceInline(InlineModelAdmin):
    model = CourseResource
    extra = 0


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['name', 'degree', 'is_banner', 'get_lesson_num', 'go_to', 'learn_time', 'students',
                    'fav_num', 'image', 'click_num', 'add_time']
    list_display_links = ['name']
    list_editable = ['degree', 'is_banner']

    search_fields = ['name', 'desc', 'detail']
    list_filter = ['degree', 'is_banner', 'learn_time', 'students', 'fav_num', 'click_num', 'add_time']

    ordering = ['-click_num']
    readonly_fields = ['click_num', 'students', 'fav_num', 'add_time']

    actions = ['make_banner']

    # exclude = ['click_num']
    inlines = [LessonInline, CourseResourceInline]

    def make_banner(self, request, queryset):
        banner_update = queryset.update(is_banner=True)
        self.message_user(request,u'%s 个课程已成功加入到了轮播展示栏！' % banner_update)

    make_banner.short_description = u'加入轮播栏'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['add_time']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['add_time']


@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['name']
    list_filter = ['add_time']

