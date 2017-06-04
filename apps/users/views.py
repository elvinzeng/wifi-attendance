#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.hashers import make_password
from django.contrib import auth
import os
import re
import datetime
import json

from users.form import JoinForm
from users.models import UserProfile
from users.models import VerificationToken

from users import users_util

__author__ = "Elvin Zeng"


class LoginView(View):
    """
    login view
    """

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            # 检查用户操作是否已经经过了授权
            token = request.session.get("verification_token", "null")
            if "null" == token:
                error_message = "token不存在"
                return render(request, "error.html", locals())
            token = VerificationToken.objects.filter(token=token)
            if len(token) != 1:
                error_message = "指定token不存在"
                return render(request, "error.html", locals())
            token = token[0]
            if not token.is_verified:
                error_message = "当前操作尚未被授权"
                return render(request, "error.html", locals())

            # 继续下一步操作
            ip = token.mobile_ip
            output = os.popen('arp ' + ip).readlines()
            for line in output:
                matched_list = re.findall(r"([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})", line)
                if len(matched_list) > 0:
                    matched_tuple = matched_list[0]
                    if len(matched_tuple) > 0:
                        mac = matched_tuple[0]
                        request.session["mobile_ip"] = ip
                        request.session["mobile_mac"] = mac
                        break

            if 'mac' not in locals().keys():
                error_message = "获取手机mac地址失败"
                return render(request, "error.html", locals())

            user_list = UserProfile.objects.filter(username=mac)
            if len(user_list) > 0:
                #  登录并重定向
                user = auth.authenticate(username=mac, password=mac)
                auth.login(request, user)
                return redirect("/")
            else:
                return render(request, "join.html", locals())


class LogoutView(View):
    """
    logout view
    """

    def get(self, request):
        if request.user.is_authenticated:
            auth.logout(request)
            return redirect("/")


class JoinView(View):
    """
    join view
    """

    def post(self, request):
        form = JoinForm(request.POST)
        if form.is_valid():
            # 检查用户操作是否已经经过了授权
            token = request.session.get("verification_token", "null")
            if "null" == token:
                error_message = "token不存在"
                return render(request, "error.html", locals())
            token = VerificationToken.objects.filter(token=token)
            if len(token) != 1:
                error_message = "指定token不存在"
                return render(request, "error.html", locals())
            token = token[0]
            if not token.is_verified:
                error_message = "当前操作尚未被授权"
                return render(request, "error.html", locals())

            user_profile = UserProfile()
            user_profile.first_name = form.data["first_name"]
            user_profile.last_name = form.data["last_name"]
            user_profile.email = form.data["email"]
            user_profile.username = request.session["mobile_mac"]
            user_profile.password = make_password(request.session["mobile_mac"])
            user_profile.save()

            if users_util.is_hr_account_created():
                user_profile.groups.add(users_util.staff_group())
            else:
                #  第一个登记的用户将默认被设置为hr
                user_profile.groups.add(users_util.staff_group())
                user_profile.groups.add(users_util.hr_group())

            # user = auth.authenticate(username=mac, password=mac)
            auth.login(request, user_profile)

            msg = "手机登记成功！3秒后将自动跳转到个人考勤记录页面。"
            timeout = 3000
            redirect_target = "/"
            return render(request, "msg.html", locals())
        else:
            return render(request, "join.html", locals())


class AuthorizeView(View):
    def get(self, request):
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        token = request.GET.get("token", "null")
        if "null" == token:
            error_message = "参数token不存在"
            return render(request, "error.html", locals())
        else:
            token = VerificationToken.objects.filter(token=token)
            if len(token) != 1:
                error_message = "指定的token不存在"
                return render(request, "error.html", locals())
            token = token[0]
            if token.is_used:
                error_message = "指定的token已经用过了，操作无效"
                return render(request, "error.html", locals())
            if datetime.datetime.now() - token.expire_time > datetime.timedelta(seconds=0):
                error_message = "token已过期，操作无效"
                return render(request, "error.html", locals())
            token.is_used = True
            token.is_verified = True
            token.mobile_ip = ip
            token.save()
            return render(request, "authorize-result.html")


class AuthorizationCheckView(View):
    def get(self, request):
        token = request.GET.get("token", "null")
        response_data = {}
        if "null" == token:
            response_data['status'] = 5
            response_data['message'] = 'parameter token not found'
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            token = VerificationToken.objects.filter(token=token)
            if len(token) != 1:
                response_data['status'] = 5
                response_data['message'] = 'token does not exists'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            token = token[0]
            if token.is_verified:
                response_data['status'] = 2
                response_data['message'] = 'success'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else:
                response_data['status'] = 5
                response_data['message'] = 'not verified'
                return HttpResponse(json.dumps(response_data), content_type="application/json")
