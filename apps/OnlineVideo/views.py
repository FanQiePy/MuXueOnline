# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response

# Create your views here.


def page_not_found(request):
    return render_to_response('404.html', status=404)


def page_error(request):
    return render_to_response('500.html', status=500)

