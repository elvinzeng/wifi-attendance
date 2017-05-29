#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser


__author__ = "Elvin Zeng"


class UserProfile(AbstractUser):
    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name