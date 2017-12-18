# -*- coding: utf-8 -*-

from django import forms
from captcha.fields import CaptchaField

from .models import UserProfile, EmailVerifyRecord

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=16, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, max_length=16, min_length=8, widget=forms.PasswordInput)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(required=True, max_length=16, min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, max_length=16, min_length=8, widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'birthday', 'gender', 'address', 'mobile']


class UserProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']


class UserProfileEmailCodeForm(forms.ModelForm):
    class Meta:
        model = EmailVerifyRecord
        fields = ['code', 'email']