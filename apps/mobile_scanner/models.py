#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from users.models import UserProfile

__author__ = "Elvin Zeng"


class OnlineHistory(models.Model):
    """
    mobile online history
    """

    mac = models.CharField(null=False, verbose_name="MAC地址", max_length=17)
    ip = models.CharField(null=True, verbose_name="在线时的ip地址", max_length=15)
    date = models.DateField(null=False, verbose_name=u"在线记录的日期")
    time = models.TimeField(null=False, verbose_name=u"在线记录的时间")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u"在线记录"
        verbose_name_plural = verbose_name
