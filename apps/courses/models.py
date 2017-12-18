# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
import operator
from itertools import chain

from django.db import models

from organization.models import CourseOrg, Teacher

from DjangoUeditor.models import UEditorField

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    category = models.CharField(default='', max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=20, verbose_name=u'课程标签')
    desc = UEditorField(width=600, height=300, toolbars="full",
                        imagePath="course/images/%(basename)s_%(date)s.%(extname)s",
                        filePath="course/files/%(basename)s_%(date)s.%(extname)s",
                        upload_settings={"imageMaxSize": 1204000}, default='', verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=5, verbose_name=u'难度')
    periods = models.IntegerField(default=0, verbose_name=u'课时')
    learn_time = models.IntegerField(default=0, verbose_name=u'学习时常')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'课程封面')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    org = models.ForeignKey(CourseOrg, default=1, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='teacher_course', default=1, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=100, default='', verbose_name=u'课程提示')
    teacher_tell = models.CharField(max_length=100, default='', verbose_name=u'学会什么')
    notice = models.CharField(max_length=100, default='', verbose_name=u'课程公告')
    is_banner = models.BooleanField(default=False, verbose_name=u'课程是否轮播')

    class Meta:
        verbose_name = u'课程表'
        verbose_name_plural = verbose_name

    def get_lesson_num(self):
        lesson_num = self.lesson_set.all().count()
        return lesson_num

    get_lesson_num.short_description = u'章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/course/{0}' target='_blank'>{1}</a>".format(self.id, self.name))
    go_to.short_description = u'跳转'

    def get_user_courses(self):
        from operation.models import UserCourse
        user_courses = UserCourse.objects.filter(course_id=self.id)[:5]
        return user_courses

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, related_name='video', verbose_name=u'章节')
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.URLField(default='', verbose_name=u'视频地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=100, verbose_name=u'名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'课程资源')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


