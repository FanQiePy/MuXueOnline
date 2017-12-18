# -*- coding: utf-8 -*-

import re
from django import forms

from .models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        pattern = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(pattern)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'请输入有效的电话号码', code='mobile invalid')
