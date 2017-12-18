# -*- coding: utf-8 -*-

from django.conf.urls import url


from organization.views import *
from operation.views import UserAskView


urlpatterns = [
    url(r'^list$', OrgListView.as_view(), name='org_list'),
    url(r'^user_ask$', UserAskView.as_view(), name='user_ask'),
    url(r'^home/(?P<org_id>\d+)$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name='org_teacher'),


]