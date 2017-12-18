# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'城市')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    category = models.CharField(max_length=20, choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')),
                                default='pxjg', verbose_name=u'机构类别')
    desc = models.TextField(verbose_name=u'机构描述')
    student_num = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_num = models.IntegerField(default=0, verbose_name=u'课程数')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name=u'封面')
    address = models.CharField(max_length=150, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def get_course_num(self):
        return self.course_set.all().count()

    def get_classic_course(self):
        from courses.models import Course
        classic_course = Course.objects.filter(org_id=self.id).order_by('-students')[:2]
        return classic_course

    def get_teacher_num(self):
        return self.teacher_org.all().count()

    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, related_name='teacher_org', verbose_name=u'所属机构')
    name = models.CharField(max_length=20, verbose_name=u'教师名')
    age = models.IntegerField(default=22, verbose_name=u'年龄', validators=[
        MinValueValidator(22, message='年龄必须在22岁以上'),
        MaxValueValidator(60, message='年龄必须在60岁以下')
    ])
    avatar = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='教师头像', default='teacher/2017/12/default.png')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'公司职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_num = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_num = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_teacher_course_num(self):
        return self.teacher_course.all().count()

    def __unicode__(self):
        return self.name


