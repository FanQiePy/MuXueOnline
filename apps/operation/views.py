# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from .forms import UserAskForm
from .models import UserFavorite
from .models import UserAsk

from organization.models import CourseOrg, Teacher
from courses.models import Course
# Create your views here.


class UserAskView(View):

    def post(self, request):
        form = UserAskForm(request.POST)
        if form.is_valid():
            user_ask = form.save()
            user_ask_data = {"status": "success"}
            return HttpResponse(json.dumps(user_ask_data), content_type='application/json')
        else:
            user_ask_data = {"status": "fail", "msg": u"提交出错"}
            return HttpResponse(json.dumps(user_ask_data),
                                content_type='application/json')


class UserFavouriteView(View):
    def post(self, request):
        if request.user.is_authenticated():
            user = request.user
            fav_id = int(request.POST.get('fav_id', 0))
            fav_type = int(request.POST.get('fav_type', 0))
            user_fav = UserFavorite.objects.filter(fav_type=fav_type).filter(fav_id=fav_id).filter(user=user)
            if not user_fav.exists():
                user_fav = UserFavorite(user=user, fav_id=fav_id,
                                        fav_type=fav_type)
                user_fav.save()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num += 1
                    course.save()
                elif fav_type== 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_num += 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_num += 1
                    teacher.save()
                json_data = {"status": "success", "msg": u'收藏成功'}
                return HttpResponse(json.dumps(json_data), content_type='application/json')
            elif user_fav.exists():
                user_fav.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_num -= 1
                    course.save()
                elif fav_type== 2:
                    org = CourseOrg.objects.get(id=fav_id)
                    org.fav_num -= 1
                    org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_num -= 1
                    teacher.save()
                json_data = {"status": "success", "msg": u'取消成功'}
                return HttpResponse(json.dumps(json_data), content_type='application/json')
            else:
                json_data = {"status": "fail", "msg": u'收藏出错'}
                return HttpResponse(json.dumps(json_data), content_type='application/json')
        else:
            json_data = {"status": "fail", "msg": u'用户未登录'}
            return HttpResponse(json.dumps(json_data), content_type='application/json')

