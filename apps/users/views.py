#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
import os
import re

from users.models import UserProfile

__author__ = "Elvin Zeng"


class LoginView(View):
    """
    login view
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            # do login here
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
                output = os.popen('arp ' + ip).readlines()
                for line in output:
                    matched_list = re.findall(r"([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})", line)
                    if len(matched_list) > 0:
                        matched_tuple = matched_list[0]
                        if len(matched_tuple) > 0:
                            mac = matched_tuple[0]
                            break
                user_list = UserProfile.objects.filter(username=mac)
                if len(user_list) > 0:
                    #  登录并重定向
                    return redirect("/")
                else:
                    return render(request, "join.html", locals())
