# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.shortcuts import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import UserProfile, EmailVerifyRecord, Banner
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group


from DjangoUeditor.widgets import UEditorWidget
# Register your models here.
User = get_user_model()


class DecadeBornListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('出生年代')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('80s', _('80后')),
            ('90s', _('90后')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '80s':
            return queryset.filter(birthday__gte=datetime.date(1980, 1, 1),
                                   birthday__lte=datetime.date(1989, 12, 31))
        if self.value() == '90s':
            return queryset.filter(birthday__gte=datetime.date(1990, 1, 1),
                                   birthday__lte=datetime.date(1999, 12, 31))


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'birthday'  # 日期类型会显示下拉框
    # fields = ('username', 'nick_name', 'email', 'gender', 'mobile', 'address', 'is_superuser', 'is_staff')
    #  和exlcude相同效果，只包含model中的字段
    # exclude = ('password', 'first_name', 'last_name')
    fieldsets = (
        (None, {
            'fields': (('username', 'nick_name'), ('email', 'gender'), 'user_permissions', 'groups', 'password')
        }),
        (u'高级选项',{
            'classes': ('collapse',),
            'fields': ('birthday', 'mobile', 'avatar', 'address', 'is_superuser', 'is_staff')
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': UEditorWidget},
    }
    # 修改页面显示和过滤设置
    list_display = ('username', 'nick_name', 'email', 'gender', 'mobile', 'address', 'is_superuser',
                    'is_staff', 'get_unread_message_num')  # 显示在修改页面中，可接受对象实例的可调用对象

    list_display_links = ('username',)  # 显示列表字段
    list_editable = ('gender', 'is_superuser', 'is_staff')  # 显示表中可编辑字段

    list_filter = ('gender', DecadeBornListFilter, ('is_superuser', admin.BooleanFieldListFilter),
                   ('is_staff', admin.BooleanFieldListFilter))  # 激活过滤栏

    # readonly_fields = ('username', 'nick_name', 'email', 'gender', 'birthday', 'mobile', 'avatar', 'address')

    search_fields = ('username', 'nick_name', 'email')

    filter_horizontal = ('groups', 'user_permissions',)


@admin.register(EmailVerifyRecord)
class EmailVerifyRecordAdmin(admin.ModelAdmin):
    # date_hierarchy = 'send_time'

    list_display = ['email', 'code', 'send_type', 'send_time']
    list_display_links = ('email',)

    readonly_fields = ('email', 'code', 'send_type', 'send_time')

    search_fields = ['email']
    list_filter = ['send_type', 'send_time']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    date_hierarchy = 'add_time'

    list_display = ['index', 'title', 'image', 'url', 'add_time']
    list_display_links = ('index',)
    list_editable = ('title', 'image',)

    ordering = ['index']
    search_fields = ['title', ]
    list_filter = ['index', 'add_time']


class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['name']


admin.site.register(Permission, PermissionAdmin)
admin.site.unregister(Group)

