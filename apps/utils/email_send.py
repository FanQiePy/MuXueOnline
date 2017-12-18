# -*- coding: utf-8 -*-

from random import Random

from django.core.mail import send_mail
from django.conf import settings
from MyUser.models import EmailVerifyRecord


def random_str(random_length=8):
    string = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        string += chars[random.randint(0, length)]
    return string


def send_email(email, send_type='register'):
    random_string = random_str(16)
    if send_type == 'change_email':
        random_string = random_str(6)
    email_record = EmailVerifyRecord(code=random_string,
                                     email=email,
                                     send_type=send_type)
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = u'友为在线网注册激活链接'
        email_body = u'请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(random_string)

        email_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, ['343960327@qq.com'])
        if email_status:
            pass
    elif send_type == 'forget':
        email_title = u'友为在线网重置密码链接'
        email_body = u'请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(random_string)

        email_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, ['343960327@qq.com'])
        if email_status:
            pass

    elif send_type == 'change_email':
        email_title = u'友为在线网验证码'
        email_body = u'验证码：{0}'.format(random_string)

        email_status = send_mail(email_title, email_body, settings.DEFAULT_FROM_EMAIL, ['343960327@qq.com'])
        if email_status:
            pass





