# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponse
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from courses.models import Course
from operation.models import UserFavorite
from .models import CourseOrg, CityDict, Teacher


from pure_pagination import Paginator, PageNotAnInteger

import json
# Create your views here.


class OrgListView(View):
    def get(self, request):
        all_org = CourseOrg.objects.all()
        all_cities = CityDict.objects.all()
        # 根据搜索结果进行筛选
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_org = CourseOrg.objects.filter(
                Q(name__icontains=keywords) |
                Q(desc__icontains=keywords) |
                Q(address__icontains=keywords)
            )

        # 列出最受欢迎课程
        hot_org = all_org.order_by('click_num')[:3]

        # 根据机构类别和城市筛选课程
        city_id = request.GET.get('city', '')
        category = request.GET.get('category', '')
        if city_id and category:
            all_org = CourseOrg.objects.filter(city_id=int(city_id)).filter(category=category)
        elif city_id:
            all_org = CourseOrg.objects.filter(city_id=int(city_id))
        elif category:
            all_org = CourseOrg.objects.filter(category=category)

        # 对筛选出的结果根据学习人数和课次数排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_org = all_org.order_by('-student_num')
            elif sort == 'course_num':
                all_org = all_org.order_by('-course_num')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_org, 2, request=request)
        org = p.page(page)

        all_counts = all_org.count()
        context = {
            'all_org': org,
            'all_cities': all_cities,
            'all_counts': all_counts,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort': sort,
        }
        return render(request, 'org-list.html', context)


class OrgHomeView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            raise Http404(u'没有相应的机构')
        # 增加一次机构点击数
        org.click_num += 1
        org.save()

        current = 'home'
        fav_id = org.id
        fav_type = 2
        has_fav = False
        if request.user.is_authenticated():
            fav = UserFavorite.objects.filter(fav_type=2).filter(fav_id=fav_id).filter(user=request.user)
            if fav:
                has_fav = True

        all_course = Course.objects.filter(org=org)
        all_teacher = Teacher.objects.filter(org=org)
        context = {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'org': org,
            'current': current,
            'fav_id': fav_id,
            'fav_type': fav_type,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-homepage.html', context)


class OrgCourseView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            raise Http404(u'没有相应的机构')
        current = 'course'
        all_course = Course.objects.filter(org=org)
        all_teacher = Teacher.objects.filter(org=org)
        fav_id = org.id
        fav_type = 2
        has_fav = False
        if request.user.is_authenticated():
            fav = UserFavorite.objects.filter(fav_type=2).filter(fav_id=fav_id).filter(user=request.user)
            if fav:
                has_fav = True
        context = {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'org': org,
            'current': current,
            'fav_id': fav_id,
            'fav_type': fav_type,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-course.html', context)


class OrgDescView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            raise Http404(u'没有相应的机构')
        current = 'desc'
        all_course = Course.objects.filter(org=org)
        all_teacher = Teacher.objects.filter(org=org)
        fav_id = org.id
        fav_type = 2
        has_fav = False
        if request.user.is_authenticated():
            fav = UserFavorite.objects.filter(fav_type=2).filter(fav_id=fav_id).filter(user=request.user)
            if fav:
                has_fav = True

        context = {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'org': org,
            'current': current,
            'fav_id': fav_id,
            'fav_type': fav_type,
            'has_fav': has_fav
        }
        return render(request, 'org-detail-desc.html', context)


class OrgTeacherView(View):
    def get(self, request, org_id):
        try:
            org = CourseOrg.objects.get(id=org_id)
        except CourseOrg.DoesNotExist:
            raise Http404(u'没有相应的机构')
        current = 'teacher'
        all_course = Course.objects.filter(org=org)
        all_teacher = Teacher.objects.filter(org=org)
        course_num = all_course.count()
        fav_id = org.id
        fav_type = 2
        has_fav = False
        if request.user.is_authenticated():
            fav = UserFavorite.objects.filter(fav_type=2).filter(fav_id=fav_id).filter(user=request.user)
            if fav:
                has_fav = True
        context = {
            'all_course': all_course,
            'all_teacher': all_teacher,
            'org': org,
            'current': current,
            'course_num': course_num,
            'fav_id': fav_id,
            'fav_type': fav_type,
            'has_fav': has_fav,
        }
        return render(request, 'org-detail-teachers.html', context)


class TeacherListView(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        # 对搜索结果进行筛选
        keywords = request.GET.get('keywords', '')
        if keywords:
            teachers = Teacher.objects.filter(name__icontains=keywords)
        # 教师排行榜
        teacher_sort = teachers.order_by('-fav_num')[:3]
        # 对教师进行排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_num')

        # 对教师机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 9, request=request)
        all_teachers = p.page(page)

        context = {
            'teacher_sort': teacher_sort,
            'all_teachers': all_teachers,
            'sort': sort,
        }
        return render(request, 'teachers-list.html', context)


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        user = request.user
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            return render(request, '404.html')
        courses = Course.objects.filter(teacher_id=teacher.id)
        teacher_sort = Teacher.objects.all().order_by('-fav_num')[:3]
        # 增加一次该教师的点击数
        teacher.click_num += 1
        teacher.save()

        # 判断用户是否已收藏该教师和教师所在的机构
        teacher_hav_fav = False
        org_has_fav = False
        if user.is_authenticated():
            teacher_fav = UserFavorite.objects.filter(fav_id=teacher.id).filter(fav_type=3).filter(user_id=user.id)
            if teacher_fav.exists():
                teacher_hav_fav = True
            try:
                org = CourseOrg.objects.get(id=teacher.org_id)
                org_fav = UserFavorite.objects.filter(fav_id=org.id).filter(fav_type=2).filter(user_id=user.id)
                if org_fav.exists():
                    org_has_fav = True
            except CourseOrg.DoesNotExist:
                pass

        context = {
            'teacher': teacher,
            'teacher_sort': teacher_sort,
            'courses': courses,
            'teacher_has_fav': teacher_hav_fav,
            'org_has_fav': org_has_fav,
        }
        return render(request, 'teacher-detail.html', context)
