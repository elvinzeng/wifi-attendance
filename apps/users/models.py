#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


__author__ = "Elvin Zeng"


class UserProfile(AbstractUser):
    is_hr = models.BooleanField(default=False, null=False, verbose_name=u'帐号是否属于HR')

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name
