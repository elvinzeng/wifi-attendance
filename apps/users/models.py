#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


__author__ = "Elvin Zeng"


class UserProfile(AbstractUser):
    """
    user profile model
    """

    is_hr = models.BooleanField(default=False, null=False, verbose_name=u'帐号是否属于HR')

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name


class VerificationToken(models.Model):
    """
    verification token model
    """

    token = models.CharField(null=False, verbose_name="verification token", max_length=40)
    expire_time = models.DateTimeField(null=False, verbose_name=u"token失效时间")
    is_used = models.BooleanField(default=False, null=False, verbose_name=u'token是否已经被使用过')
    is_verified = models.BooleanField(default=False, null=False, verbose_name=u'token是否已经被标记为验证通过')
    mobile_ip = models.CharField(null=True, verbose_name="授权时的手机ip地址", max_length=15)

    class Meta:
        verbose_name = u"verification token"
        verbose_name_plural = verbose_name
