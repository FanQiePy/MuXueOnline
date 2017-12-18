# -*- coding: utf-8 -*-

from django.conf.urls import url


from organization.views import TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),
]
