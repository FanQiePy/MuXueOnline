# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from .views import *


urlpatterns = [
    url(r'^profile/', include([
        url(r'^$', UserProfileView.as_view(), name='profile'),
        url(r'^avatar$', UserProfileAvatarView.as_view(), name='avatar'),
        url(r'^password$', UserProfilePasswordView.as_view(), name='password'),
        url(r'^email$', UserProfileEmailView.as_view(), name='email'),
        url(r'^email_code$', UserprofileEmailCodeView.as_view(), name='email_code'),
    ])),

    url(r'^message/$', UserMessageView.as_view(), name='message'),

    url(r'^course/$', UserCourseView.as_view(), name='course'),

    url(r'^fav/', include([
        url(r'^$', UserFavCourseView.as_view(), name='fav'),
        url(r'^course$', UserFavCourseView.as_view(), name='fav_course'),
        url(r'^org$', UserFavOrgView.as_view(), name='fav_org'),
        url(r'^teacher$', UserFavTeacherView.as_view(), name='fav_teacher'),
    ]))
]
