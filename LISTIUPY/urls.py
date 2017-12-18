# -*- coding: utf-8 -*-
"""LISTIUPY URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# import xadmin

from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from LISTIUPY.settings import MEDIA_ROOT
from django.views.static import serve

from MyUser.views import *
from OnlineVideo.views import *

from organization import urls as org_urls
from organization import urls_teacher as teacher_urls
from courses import urls as course_urls
from operation import urls as operation_urls
from MyUser import urls as user_urls


urlpatterns = [
    url(r'^admin', admin.site.urls),
    # url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='homepage'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^captcha', include('captcha.urls')),
    url(r'^active(?P<random_string>.*)', ActiveUserView.as_view(), name='active'),
    url(r'^forget$', ForgetPasswordView.as_view(), name='forget'),
    url(r'^reset/(?P<random_string>.*)', ResetPasswordView.as_view(), name='reset_password'),
    url(r'^modify_password$', ModifyPasswordView.as_view(), name='modify_password'),
    # url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    # 配置上线静态文件
    # url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),

    # 课程机构url配置
    url(r'^org/', include(org_urls, namespace='org')),

    # 课程相关url配置
    url(r'^course/', include(course_urls, namespace='course')),

    # 用户操作url配置
    url(r'^operation/', include(operation_urls, namespace='operation')),

    # 授课教师url配置
    url(r'teacher/', include(teacher_urls, namespace='teacher')),

    # 用户url配置
    url(r'user/', include(user_urls, namespace='user')),

    # ueditor urls配置
    url(r'ueditor/', include('DjangoUeditor.urls')),

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found
handler500 = page_error

