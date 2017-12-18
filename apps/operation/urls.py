# -*- coding: utf-8 -*-

from django.conf.urls import url


from .views import *


urlpatterns = [
    url(r'^add_fav$', UserFavouriteView.as_view(), name='add_fav'),
]