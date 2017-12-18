# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(CityDict)
class CityDictAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc', 'course_name']
    list_filter = ['add_time']


@admin.register(CourseOrg)
class CourseOrgAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'address', 'city']
    list_filter = ['city', 'add_time']
    # relfield_style = 'fk_ajax'


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['org', 'name', 'avatar', 'work_years', 'work_company', 'work_position', 'points', 'click_num',
                    'fav_num', 'add_time']
    search_fields = ['org', 'name', 'points']
    list_filter = ['org','work_years', 'add_time']

