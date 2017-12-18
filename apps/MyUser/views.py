# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from smtplib import SMTPException
import json

from django.shortcuts import render, HttpResponse, redirect, reverse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from django.db.models import Q

from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import *

from courses.models import Course
from operation.models import UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from utils.email_send import send_email

from pure_pagination import Paginator, PageNotAnInteger
# Create your views here.


class ForgetPasswordView(View):
    def get(self, request):
        banners = Banner.objects.all()[:3]
        form = ForgetPasswordForm()
        context = {
            'banners': banners,
            'forget_form': form
        }
        return render(request, 'forgetpwd.html', context)

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            try:
                email_obj = UserProfile.objects.get(email=form.data.get('email'))
                email = email_obj.email
                send_email(email, 'forget')
                return HttpResponse(u'邮件已发送至你的邮箱，请前往邮箱查看')
            except UserProfile.DoesNotExist:
                return render(request, 'forgetpwd.html', {'forget_form': form, 'msg': u'用户未注册'})
        return render(request, 'forgetpwd.html', {'forget_form': form})


class ActiveUserView(View):
    def get(self, request, random_string):
        try:
            email_obj = EmailVerifyRecord.objects.get(code=random_string)
            email = email_obj.email
        except EmailVerifyRecord.DoesNotExist:
            return render(request, 'active_fail.html')
        user = UserProfile.objects.get(email=email)
        user.is_active = True
        user.save()
        message = UserMessage(user=user, message=u'你的账户已激活成功,现在开始学习吧!')
        message.save()
        return render(request, 'login.html')


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def get(self, request):
        banners = Banner.objects.all()[:3]
        context = {
            'banners': banners
        }
        return render(request, 'login.html', context)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
            else:
                return render(request, 'login.html', {'msg': u'用户名或密码错误'})
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'login.html', {'login_form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('homepage'))


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'register_form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.data.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, 'register.html', {'msg': u'用户已存在'})
            new_user = UserProfile.objects.create_user(username=form.data.get('email'),
                                                       email=form.data.get('email'),
                                                       password=form.data.get('password'),
                                                       is_active=False)
            new_user.save()
            message = UserMessage(user=new_user, message=u'你已注册成功,欢迎来到友为在线学习网!')
            message.save()
            send_email(new_user.email, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': form})


class ResetPasswordView(View):
    def get(self, request, random_string):
        try:
            email_obj = EmailVerifyRecord.objects.get(code=random_string)
            email = email_obj.email
        except EmailVerifyRecord.DoesNotExist:
            return render(request, 'active_fail.html')
        return render(request, 'password_reset.html', {'email': email})


class ModifyPasswordView(View):
    def post(self, request):
        form = ResetPasswordForm(request.POST)
        email = request.POST.get('email', '')
        if form.is_valid():
            password1 = form.data.get('password1')
            password2 = form.data.get('password2')
            if password1 and password2:
                if password1 == password2:
                    user = UserProfile.objects.get(email=email)
                    user.password = make_password(password2)
                    user.save()
                    return redirect('/login/')
                else:
                    return render(request, 'password_reset.html', {'email': email, 'msg': u'密码不一致'})
        else:
            return render(request, 'password_reset.html', {'email': email, 'reset_form': form})


class UserProfileView(LoginRequiredMixin, View):
    """
    用户个人中心
    """
    login_url = '/login'

    def get(self, request):
        form = UserProfileForm()
        context = {
            "form": form,
        }
        return render(request, 'usercenter-info.html', context)

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        data = {}
        if form.is_valid():
            form.save()
            data = {
                "status": "success",
            }
        else:
            return HttpResponse(json.dumps(form.errors), content_type='application/json')
        return HttpResponse(json.dumps(data), content_type='application/json')


class UserProfileAvatarView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request):
        form = UserProfileAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        return render(request, 'usercenter-info.html')


class UserProfilePasswordView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        user = request.user
        email = request.user.email
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 and password2:
                if password1 == password2:
                    user.password = make_password(password2)
                    user.save()
                    date = {
                        "status": "success"
                    }
                    return HttpResponse(json.dumps(date), content_type="application/json")
                else:
                    date = {
                        "msg": u"密码不一致",
                        "status": "fail"
                    }
                    return HttpResponse(json.dumps(date), content_type="application/json")
        else:
            return HttpResponse(json.dumps(form.errors), content_type="application/json")


class UserProfileEmailView(LoginRequiredMixin, View):
    login_url = '/login'

    def post(self, request):
        form = UserProfileEmailCodeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            code = form.cleaned_data.get('code')
            try:
                EmailVerifyRecord.objects.filter(email=email).filter(send_type='change_email').get(code=code)
                request.user.email = email
                request.user.save()
            except EmailVerifyRecord.DoesNotExist:
                date = {
                    "email": u"验证码错误，请重新输入！",
                    "status": "fail",
                }
                return HttpResponse(json.dumps(date), content_type="application/json")
            date = {
                "status": "success",
            }
            return HttpResponse(json.dumps(date), content_type="application/json")


class UserprofileEmailCodeView(LoginRequiredMixin, View):
    login_url = '/login'

    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email).exists():
            date = {
                "status": "failure",
                "email": u"邮箱已被注册，请选择其他邮箱！"
            }
            return HttpResponse(json.dumps(date), content_type="application/json")
        try:
            send_email(email, send_type='change_email')
            date = {
                "status": "success",
            }
        except SMTPException:
            date = {
                "status": "failure",
            }
            return HttpResponse(json.dumps(date), content_type="application/json")
        return HttpResponse(json.dumps(date), content_type="application/json")


class UserCourseView(LoginRequiredMixin, View):
    """
    用户中心--课程信息
    """
    login_url = '/login'

    def get(self, request):
        user_courses = Course.objects.filter(user_course__user_id=request.user.id)
        context = {
            'user_courses': user_courses,
        }
        return render(request, 'usercenter-mycourse.html', context)


class UserFavCourseView(LoginRequiredMixin, View):
    """
    用户中心--收藏课程
    """
    login_url = '/login'

    def get(self, request):
        user_fav = UserFavorite.objects.filter(fav_type=1).filter(user_id=request.user.id)
        user_fav_courses = Course.objects.filter(id__in=[fav.fav_id for fav in user_fav])
        context = {
            'user_fav_courses': user_fav_courses,
        }
        return render(request, 'usercenter-fav-course.html', context)


class UserFavOrgView(LoginRequiredMixin, View):
    """
    用户中心-收藏机构
    """
    def get(self, request):
        user_fav = UserFavorite.objects.filter(fav_type=2).filter(user_id=request.user.id)
        user_fav_org = CourseOrg.objects.filter(id__in=[fav.fav_id for fav in user_fav])
        context = {
            'user_fav_org': user_fav_org,
        }
        return render(request, 'usercenter-fav-org.html', context)


class UserFavTeacherView(LoginRequiredMixin, View):
    """
    用户中心-收藏教师
    """
    def get(self, request):
        user_fav = UserFavorite.objects.filter(fav_type=3).filter(user_id=request.user.id)
        user_fav_teachers = Teacher.objects.filter(id__in=[fav.fav_id for fav in user_fav])
        context = {
            'user_fav_teachers': user_fav_teachers,
        }
        return render(request, 'usercenter-fav-teacher.html', context)


class UserMessageView(LoginRequiredMixin, View):
    """
    用户中心--消息信息
    """
    login_url = '/login'

    def get(self, request):
        message = UserMessage.objects.filter(user_id=request.user.id)

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(message, 10, request=request)
        user_message = p.page(page)
        if user_message:
            for mes in user_message.object_list:
                mes.has_read = True
                mes.save()
        context = {
            'user_message': user_message,
            'message': message,
        }
        return render(request, 'usercenter-message.html', context)


class IndexView(View):
    def get(self, request):
        banners = Banner.objects.all()[:5]
        course_list = Course.objects.all().order_by('-add_time')[:6]
        course_banners = Course.objects.filter(is_banner=True)[:5]
        course_org = CourseOrg.objects.all().order_by('-add_time')[:5]

        context = {
            'banners': banners,
            'course_list': course_list,
            'course_banners': course_banners,
            'course_org': course_org
        }
        return render(request, 'index.html', context)

