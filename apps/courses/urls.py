# -*- coding: utf-8 -*-

from django.conf.urls import url


from .views import *
from operation.views import UserAskView


urlpatterns = [
    url(r'^list$', CourseView.as_view(), name='course_list'),
    url(r'^course/(?P<course_id>\d+)$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^(?P<course_id>\d+)/lesson$', LessonDetailView.as_view(), name='course_lesson'),
    url(r'^(?P<course_id>\d+)/comment$', LessonCommentView.as_view(), name='course_comment'),
]