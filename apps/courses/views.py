# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json, urlparse, re

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q

from operation.models import UserFavorite, CourseComment, UserCourse
from MyUser.models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Course, Lesson, CourseResource

from pure_pagination import Paginator, PageNotAnInteger
# Create your views here.


class CourseView(View):
    def get(self, request):
        all_courses = Course.objects.all()
        hot_courses = Course.objects.all()[:3]
        # 根据搜索结果进行筛选
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = Course.objects.filter(
                Q(name__icontains=keywords) |
                Q(category__icontains=keywords) |
                Q(desc__icontains=keywords) |
                Q(tag__icontains=keywords) |
                Q(detail__icontains=keywords)
            )

        # 根据发表时间，收藏数，学生数进行排序
        sort = request.GET.get('sort','')
        if sort == 'add_time':
            all_courses = all_courses.order_by('-add_time')
        elif sort == 'hot':
            all_courses = all_courses.order_by('-fav_num')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        all_courses = p.page(page)
        context = {
            'all_courses': all_courses,
            'hot_courses': hot_courses,
            'sort': sort,
        }
        return render(request, 'course-list.html', context)


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user = request.user
        course_is_fav = ''
        org_is_fav = ''
        # 课程点击数
        course.click_num += 1
        course.save()

        # 相关课程
        related_courses = Course.objects.filter(tag=course.tag).exclude(id=course.id)

        # 课程和机构收藏
        if user.is_authenticated():
            course_fav = UserFavorite.objects.filter(fav_type=1).filter(fav_id=course.id).filter(user=request.user)
            if course_fav:
                course_is_fav = True
            else:
                course_is_fav = False
            org_fav = UserFavorite.objects.filter(fav_type=2).filter(fav_id=course.id).filter(user=request.user)
            if org_fav:
                org_is_fav = True
            else:
                org_is_fav = False

        context = {
            'course': course,
            'course_is_fav': course_is_fav,
            'org_is_fav': org_is_fav,
            'related_courses': related_courses,
        }
        return render(request, 'course-detail.html', context)


class LessonDetailView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user = request.user
        lessons = Lesson.objects.filter(course=course)

        # 学习该课程的还学习了的课程
        course_resources = CourseResource.objects.filter(course=course)
        all_user_courses = UserCourse.objects.filter(course_id=course.id)
        learned_other_courses = UserCourse.objects.filter(
            user_id__in=[all_user_course.user_id for all_user_course in all_user_courses]).\
            exclude(course_id=course.id)[:5]

        # 关联用户和该课程，增加课程学习人数
        user_course = UserCourse.objects.filter(course_id=course.id).filter(user_id=user.id)
        if not user_course.exists():
            new_user_course = UserCourse(course=course, user=user)
            new_user_course.save()
            course.students += 1
            course.save()

        lesson_or_comment = 'lesson'
        context = {
            'course': course,
            'lessons': lessons,
            'course_resources': course_resources,
            'lesson_or_comment': lesson_or_comment,
            'learned_other_courses': learned_other_courses,
        }
        return render(request, 'course-video.html', context)


class LessonCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
        except Course.DoesNotExist:
            return render(request, '404.html')
        comments = CourseComment.objects.filter(course=course).order_by('-add_time')
        lesson_or_comment = 'comment'
        context = {
            'course': course,
            'comments': comments,
            'lesson_or_comment': lesson_or_comment,
        }
        return render(request, 'course-comment.html', context)

    def post(self, request, course_id):
        user = request.user
        try:
            course = Course.objects.get(id=int(course_id))
        except Course.DoesNotExist:
            return render(request, '404.html')
        if user.is_authenticated():
            comment = request.POST.get('comments', '')
            data = {
                "status": "success",
                }
            course_comment = CourseComment(user=user, course=course, comment=comment)
            course_comment.save()
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {
                "status": "fail",
                "msg": u"用户未登陆"}
            return HttpResponse(json.dumps(data), content_type="application/json")



